from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
from employee.models import Attendance, Salary
import pytz
import calendar


def align_tz(target_dt, reference_dt):
    """
    target_dt ko reference_dt ke timezone-awareness ke hisab se adjust karta hai.
    - reference aware hai  -> target ko aware bana do (current timezone me)
    - reference naive hai   -> target ko naive rakho
    Isse USE_TZ True/False dono pe naive vs aware ka TypeError nahi aata.
    """
    ref_aware = timezone.is_aware(reference_dt)
    tgt_aware = timezone.is_aware(target_dt)

    if ref_aware and not tgt_aware:
        return timezone.make_aware(target_dt, timezone.get_current_timezone())
    if not ref_aware and tgt_aware:
        return timezone.make_naive(target_dt, timezone.get_current_timezone())
    return target_dt


def get_today():
    """USE_TZ True/False dono pe aaj ki local date deta hai (localtime error se bachne ke liye)."""
    current = timezone.now()
    if timezone.is_aware(current):
        return timezone.localdate()
    return current.date()


class Command(BaseCommand):
    help = "Auto checkout + calculate total, overtime hours & salary"

    def handle(self, *args, **options):
        # 🔥 IMPORTANT FIX
        target_date = get_today() - timedelta(days=1)

        attendances = Attendance.objects.select_related("employee").filter(
            date=target_date,
            status="present",
            login_time__isnull=False,
            logout_time__isnull=True
        )

        processed = 0
        failed = 0

        for att in attendances:
            try:
                emp = att.employee
                login_time = att.login_time

                # ✅ Decide logout time
                if emp.shift_out:
                    logout_time = datetime.combine(target_date, emp.shift_out)
                    # 🔧 login_time ke awareness ke saath align karo (naive/aware mismatch fix)
                    logout_time = align_tz(logout_time, login_time)

                    # Night shift safety
                    if logout_time <= login_time:
                        logout_time += timedelta(days=1)
                else:
                    logout_time = login_time + timedelta(
                        hours=float(emp.working_hours)
                    )

                # 🔹 Calculate total hours
                total_seconds = (logout_time - login_time).total_seconds()
                total_hours = round(Decimal(total_seconds) / Decimal(3600), 2)

                # 🔹 Overtime hours
                overtime_hours = max(
                    Decimal(0),
                    total_hours - Decimal(emp.working_hours)
                )

                # =============================
                # 💰 SALARY CALCULATION
                # =============================
                days_in_month = calendar.monthrange(target_date.year, target_date.month)[1]

                per_day_salary = emp.base_salary / Decimal(days_in_month)
                per_hour_salary = per_day_salary / Decimal(emp.working_hours)

                normal_salary = per_day_salary

                overtime_salary = (
                    per_hour_salary
                    * overtime_hours
                    * emp.overtime_multiplier
                )

                salary_obj, _ = Salary.objects.get_or_create(
                    employee=emp,
                    month=target_date.month,
                    year=target_date.year,
                    defaults={
                        'base_salary': Decimal('0'),
                        'overtime_salary': Decimal('0'),
                        'commission': Decimal('0'),
                        'deduction': Decimal('0'),
                    }
                )

                salary_obj.base_salary += normal_salary
                salary_obj.overtime_salary += overtime_salary
                salary_obj.save(update_fields=[
                    'base_salary',
                    'overtime_salary'
                ])

                # =============================
                # 🔹 Save attendance
                # =============================
                att.logout_time = logout_time
                att.total_hours = total_hours
                att.overtime_hours = overtime_hours
                att.save(update_fields=[
                    "logout_time",
                    "total_hours",
                    "overtime_hours"
                ])

                processed += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{emp.name} | Salary +{normal_salary} | OT +{overtime_salary}"
                    )
                )

            except Exception as e:
                failed += 1
                self.stdout.write(
                    self.style.ERROR(
                        f"Failed for attendance id={att.id} "
                        f"({getattr(att.employee, 'name', 'unknown')}): {e}"
                    )
                )

        self.stdout.write(self.style.SUCCESS(
            f"Processed {processed} employees, Failed {failed}"
        ))
