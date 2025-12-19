from django.core.management.base import BaseCommand
import random
from datetime import date, timedelta
from apps.attendance.models import Attendance
from apps.auths.models import User
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Generate dummy attendance records"

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=20)

    def handle(self, *args, **options):
        num_days = options["days"]
        start_date = date.today() - timedelta(days=num_days)
        users = User.objects.all()
        count = 0

        for i in range(num_days):
            record_date = start_date + timedelta(days=i)
            for user in users:
                try:
                    Attendance.objects.create(
                        user=user,
                        is_nfc=random.choice([True, False]),
                        is_qr=random.choice([True, False]),
                        code="NFC" if random.random() > 0.5 else "QR",
                        date=record_date,
                    )
                    count += 1
                    print(f"Created record for {user.username} on {record_date}")

                except IntegrityError:
                    # Already exists, skip
                    continue

        self.stdout.write(self.style.SUCCESS(f"Created {count} records."))

    print("Done")
