from django.core.management.base import BaseCommand
from django.utils import timezone
from employee.models import Employee, Attendance, Leave, Salary
import pytz
from decimal import Decimal
import calendar

class Command(BaseCommand):
    help = "Create absent or leave records for today"

    def handle(self, *args, **options):
        ist = pytz.timezone("Asia/Kolkata")
        today = timezone.now().astimezone(ist).date()

        employees = Employee.objects.filter(status="active")

        for emp in employees:
            if Attendance.objects.filter(employee=emp, date=today).exists():
                continue

            # 🔹 Check leave
            if Leave.objects.filter(employee=emp, leave_date=today).exists():

                # ---- Attendance ----
                Attendance.objects.create(
                    employee=emp,
                    date=today,
                    status="leave",
                    total_hours=emp.working_hours
                )

                # ---- Salary Calculation ----
                days_in_month = calendar.monthrange(today.year, today.month)[1]
                per_day_salary = emp.base_salary / Decimal(days_in_month)

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

                salary_obj.base_salary += per_day_salary
                salary_obj.save(update_fields=['base_salary'])

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Paid leave marked for {emp.name}, salary credited: {per_day_salary}"
                    )
                )

            else:
                Attendance.objects.create(
                    employee=emp,
                    date=today,
                    status="absent"
                )
                self.stdout.write(
                    self.style.WARNING(f"Absent marked for {emp.name}")
                )
