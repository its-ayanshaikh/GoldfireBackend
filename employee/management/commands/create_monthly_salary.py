from django.core.management.base import BaseCommand
from django.utils import timezone
from employee.models import Employee, Salary, SalesCommission  # update as per your app
import pytz

class Command(BaseCommand):
    help = 'Create blank Salary and SalesCommission objects for each active employee on 1st of every month'

    def handle(self, *args, **options):
        ist = pytz.timezone('Asia/Kolkata')
        today = timezone.now().astimezone(ist)
        current_month = today.month
        current_year = today.year
        month_str = f"{current_year}-{str(current_month).zfill(2)}"

        employees = Employee.objects.filter(status='active')
        created_salary = 0
        created_commission = 0

        for emp in employees:
            # -------------------------
            # Salary Object
            # -------------------------
            if not Salary.objects.filter(employee=emp, month=current_month, year=current_year).exists():
                Salary.objects.create(
                    employee=emp,
                    month=current_month,
                    year=current_year,
                    base_salary=0,          # blank default
                    overtime_salary=0,
                    commission=0,
                    deduction=0,
                    status='pending'
                )
                created_salary += 1

            # -------------------------
            # Sales Commission Object
            # -------------------------
            if not SalesCommission.objects.filter(salesperson=emp, month=month_str).exists():
                SalesCommission.objects.create(
                    salesperson=emp,
                    month=month_str,
                    total_sales=0,
                    total_commission=0,
                )
                created_commission += 1

        self.stdout.write(self.style.SUCCESS(
            f"Created {created_salary} Salary & {created_commission} SalesCommission records for {month_str}"
        ))


# For Windows Run
# python manage.py create_monthly_salary

# For 3AM at Each months first date
# 0 3 1 * * /path/to/venv/bin/python /path/to/project/manage.py create_monthly_salary_commission >> /path/to/logs/monthly_job.log 2>&1
