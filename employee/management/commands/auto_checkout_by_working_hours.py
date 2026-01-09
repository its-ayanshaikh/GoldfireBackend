from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from employee.models import Attendance
import pytz

class Command(BaseCommand):
    help = "Auto checkout using login_time + working_hours"

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

            # ✅ Auto checkout = login + working hours
            checkout_time = login_time + timedelta(
                hours=float(emp.working_hours)
            )

            # 🔹 Calculate total hours
            total_seconds = (checkout_time - login_time).total_seconds()
            total_hours = round(total_seconds / 3600, 2)

            # 🔹 Overtime (if any)
            overtime_hours = max(
                0,
                total_hours - float(emp.working_hours)
            )

            # 🔹 Save attendance
            att.logout_time = checkout_time
            att.total_hours = total_hours
            att.overtime_hours = round(overtime_hours, 2)
            att.save(update_fields=[
                "logout_time",
                "total_hours",
                "overtime_hours"
            ])

            processed += 1
            self.stdout.write(f"Auto checkout done: {emp.name}")

        self.stdout.write(self.style.SUCCESS(
            f"Auto checkout completed for {processed} employees"
        ))
