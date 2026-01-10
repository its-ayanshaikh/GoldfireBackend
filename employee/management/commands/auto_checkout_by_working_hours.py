from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
from employee.models import Attendance, Salary
import pytz
import calendar

class Command(BaseCommand):
    help = "Auto checkout + calculate total, overtime hours & salary"

    def handle(self, *args, **options):
        ist = pytz.timezone("Asia/Kolkata")
        now_ist = timezone.now().astimezone(ist)
        today = now_ist.date()

        attendances = Attendance.objects.select_related("employee").filter(
            date=today,
            status="present",
            login_time__isnull=False,
            logout_time__isnull=True
        )

        processed = 0

        for att in attendances:
            emp = att.employee
            login_time = att.login_time.astimezone(ist)

            # ✅ Decide logout time
            if emp.shift_out:
                logout_time = datetime.combine(today, emp.shift_out)
                logout_time = ist.localize(logout_time)

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
            days_in_month = calendar.monthrange(today.year, today.month)[1]

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
                month=today.month,
                year=today.year,
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

        self.stdout.write(self.style.SUCCESS(
            f"Processed {processed} employees"
        ))
