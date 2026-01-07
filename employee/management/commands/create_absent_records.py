from django.core.management.base import BaseCommand
from django.utils import timezone
from employee.models import Employee
from employee.models import Attendance
from django.core.management.base import BaseCommand
from django.utils import timezone
from employee.models import Employee
import pytz

class Command(BaseCommand):
    help = 'Create absent records for employees who did not check in today'

    def handle(self, *args, **options):
        # IST timezone
        ist = pytz.timezone('Asia/Kolkata')
        today = timezone.now().astimezone(ist).date()  # IST date

        employees = Employee.objects.filter(status='active')

        for emp in employees:
            if not Attendance.objects.filter(employee=emp, date=today).exists():
                Attendance.objects.create(employee=emp, date=today, status='absent')
                self.stdout.write(f"Absent record created for {emp.name} on {today}")

# To run this command, use:
# python manage.py create_absent_records
# In linux cron job or Windows Task Scheduler, you can schedule this command to run daily at a specific time.
# Example cron job entry to run at 00:01 AM daily:
# commands : 
# crontab -e
# 1 0 * * * cd /path/to/project && /path/to/venv/bin/python manage.py create_absent_records
