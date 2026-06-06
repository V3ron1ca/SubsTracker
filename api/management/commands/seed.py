from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.conf import settings

from api.models import Platform, PaymentMethod

User = get_user_model()

PLATFORMS = [
    "Netflix",
    "Spotify",
    "HBO Max",
    "Disney+",
    "YouTube Premium",
    "Amazon Prime",
    "Canal+",
    "Hulu",
    "Apple TV+",
    "SkyShowtime",
    "Viaplay",
    "Tidal",
    "Deezer",
    "Xbox Game Pass",
    "PlayStation Plus",
    "EA Play",
    "Nintendo Switch Online",
    "Steam",
    "ChatGPT Plus",
    "Claude Pro",
    "Midjourney",
    "Adobe Creative Cloud",
    "Canva Pro",
    "Figma Professional",
    "Notion Plus",
    "Google One",
    "Dropbox",
    "iCloud+",
    "Microsoft 365",
    "LinkedIn Premium",
    "GitHub Copilot",
    "Udemy",
    "Coursera",
    "Duolingo Plus",
    "Empik Go",
    "BookBeat",
    "Legimi",
    "Audioteka",
    "Crunchyroll",
    "Twitch Turbo",
    "Patreon",
    "Bolt",
    "Uber One",
    "Pyszne.pl",
    "Revolut Premium",
    "mBank Premium",
    "Medicover",
    "LuxMed",
    "Gym Membership",
    "McFit",
    "CityFit",
    "FitFabric",
    "Zdrofit",
    "Cinema City Unlimited",
    "Multisport",
    "Other",
]

PAYMENT_METHODS = [
    "BLIK",
    "Karta",
    "Przelew",
    "Gotówka"
]


class Command(BaseCommand):
    help = "Seed initial data (platforms + superuser)"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Creating platforms...")

        created_platforms = 0

        for name in PLATFORMS:
            _, created = Platform.objects.get_or_create(name=name)

            if created:
                created_platforms += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {created_platforms} new platforms"
            )
        )

        created_payments = 0

        for name in PAYMENT_METHODS:
            _, created = PaymentMethod.objects.get_or_create(name=name)

            if created:
                created_payments += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Created {created_payments} new payments"
            )
        )

        self.stdout.write("Checking superuser...")

        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@test.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        if created:
            if settings.DEBUG:
                admin_user.set_password("admin123")
                admin_user.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        "Development superuser created (admin/admin123)"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "Superuser created without password. "
                        "Set password manually."
                    )
                )
        else:
            self.stdout.write("Superuser already exists")

        self.stdout.write(
            self.style.SUCCESS("Seeding completed!")
        )