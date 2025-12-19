import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from apps.auths.models import User, Role
from apps.companies.models import Company
from apps.attendance.models import Attendance


class Command(BaseCommand):
    help = "Generate dummy employees and attendance for all companies"

    def handle(self, *args, **options):
        num_employees_per_company = 5
        num_days = 20
        start_date = date(2025, 12, 1)

        employee_role, _ = Role.objects.get_or_create(role_name="Employee")

        for company in Company.objects.all():
            self.stdout.write(f"Processing company: {company.company_name}")

            for i in range(1, num_employees_per_company + 1):
                full_name = f"{company.company_name} Employee {i}"
                email = f"{company.company_name.lower().replace(' ','')}_emp{i}@example.com"

                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        "full_name": full_name,
                        "password": make_password("TestPass123"),
                        "company": company,
                        "role": employee_role
                    }
                )

                if created:
                    self.stdout.write(f"  Created user: {user.full_name} ({user.email})")
                else:
                    self.stdout.write(f"  User already exists: {user.email}")

                # Generate attendance
                for day_offset in range(num_days):
                    record_date = start_date + timedelta(days=day_offset)
                    try:
                        Attendance.objects.create(
                            user=user,
                            is_nfc=random.choice([True, False]),
                            is_qr=random.choice([True, False]),
                            code="NFC" if random.random() > 0.5 else "QR",
                            date=record_date
                        )
                    except IntegrityError:
                        continue
