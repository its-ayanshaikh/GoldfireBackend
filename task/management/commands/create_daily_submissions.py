from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta
from task.models import Task, TaskSubmission
from employee.models import Employee


class Command(BaseCommand):
    help = "Create daily TaskSubmission objects for today's tasks for every employee"

    def handle(self, *args, **kwargs):
        try:
            # 1️⃣ Calculate today's day (your format: Sun=1 ... Sat=7)
            import datetime
            python_day = datetime.datetime.today().isoweekday()  # Mon=1 ... Sun=7
            today_day = python_day + 1
            if today_day == 8:
                today_day = 1

            self.stdout.write(self.style.SUCCESS(f"Today's day number: {today_day}"))

            # 2️⃣ Get today's tasks
            todays_tasks = Task.objects.filter(task_frequency__days__contains=[today_day])

            if not todays_tasks.exists():
                self.stdout.write(self.style.WARNING("No tasks found for today."))
                return

            self.stdout.write(self.style.SUCCESS(f"Found {todays_tasks.count()} tasks for today."))

            # 3️⃣ IST Time
            ist_time = now() + timedelta(hours=5, minutes=30)

            created_count = 0

            # 4️⃣ Create submissions for each employee assigned to each task
            for task in todays_tasks:
                assigned_employees = task.assigned_to.all()

                for emp in assigned_employees:
                    obj, created = TaskSubmission.objects.get_or_create(
                        task=task,
                        submitted_by=emp,
                        defaults={
                            "notes": "",
                            "submitted_at": ist_time,
                            "status": "pending"
                        }
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Created submission for Task ID {task.id} - Employee {emp.id}"
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Submission already exists for Task {task.id} - Employee {emp.id}"
                            )
                        )

            self.stdout.write(self.style.SUCCESS(f"Done! Total created: {created_count}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
