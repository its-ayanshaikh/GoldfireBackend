import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from task.models import Task, TaskSubmission


class Command(BaseCommand):
    help = (
        "Fake TaskSubmission objects create karta hai testing ke liye. "
        "Task ki frequency (days) ke hisab se pichle N dino ke submissions banata hai, "
        "randomly 'submitted' ya 'pending' status ke saath."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Aaj se kitne pichle din ke liye fake submissions banane hain (default: 30)",
        )
        parser.add_argument(
            "--done-ratio",
            type=float,
            default=0.7,
            help="Kitne percent submissions 'submitted/done' honge, 0.0 - 1.0 (default: 0.7)",
        )
        parser.add_argument(
            "--task-id",
            type=int,
            default=None,
            help="Sirf ek specific task ke liye banao (optional)",
        )

    def _day_number(self, date_obj):
        """Sun=1 ... Sat=7 (project format)."""
        python_day = date_obj.isoweekday()  # Mon=1 ... Sun=7
        day = python_day + 1
        if day == 8:
            day = 1
        return day

    def handle(self, *args, **options):
        days = options["days"]
        done_ratio = max(0.0, min(1.0, options["done_ratio"]))
        task_id = options["task_id"]

        tasks = Task.objects.all()
        if task_id:
            tasks = tasks.filter(id=task_id)

        if not tasks.exists():
            self.stdout.write(self.style.WARNING("Koi task nahi mila."))
            return

        today = timezone.now().date()

        created_count = 0
        skipped_count = 0

        for task in tasks:
            frequency = task.task_frequency or {}
            scheduled_days = frequency.get("days", []) if isinstance(frequency, dict) else []

            # agar frequency hi nahi set hai to har din maan lo
            if not scheduled_days:
                scheduled_days = [1, 2, 3, 4, 5, 6, 7]

            assigned_employees = list(task.assigned_to.all())
            if not assigned_employees:
                self.stdout.write(
                    self.style.WARNING(
                        f"Task '{task.task_name}' (id={task.id}) me koi employee assigned nahi, skip."
                    )
                )
                continue

            for offset in range(days):
                date_obj = today - timedelta(days=offset)

                # sirf un dino jab task scheduled tha
                if self._day_number(date_obj) not in scheduled_days:
                    continue

                for emp in assigned_employees:
                    is_done = random.random() < done_ratio
                    status_value = "submitted" if is_done else "pending"

                    obj, created = TaskSubmission.objects.get_or_create(
                        task=task,
                        submitted_by=emp,
                        submission_date=date_obj,
                        defaults={
                            "notes": "Fake submission (testing)" if is_done else "",
                            "status": status_value,
                            "submitted_at": timezone.now(),
                        },
                    )

                    if created:
                        created_count += 1
                    else:
                        skipped_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done! Created: {created_count}, Already existed (skipped): {skipped_count}"
            )
        )
