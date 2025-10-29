from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from apps.contact_messages.models import ContactMessage


def _anonymize(qs):
    # чистим PII, оставляем минимум для статистики
    return qs.update(
        first_name="",
        last_name="",
        email="",
        message="",
        user_agent="",
        referrer="",
        gdpr_consent=False,  # согласие больше неактуально
    )


class Command(BaseCommand):
    help = "Purge (delete) or anonymize contact messages older than N months."

    def add_arguments(self, parser):
        parser.add_argument("--months", type=int, default=24, help="Age in months (default: 24)")
        parser.add_argument("--dry-run", action="store_true", help="Only show what would be affected")
        parser.add_argument("--anonymize", action="store_true", help="Anonymize instead of delete")

    def handle(self, *args, **opts):
        months = opts["months"]
        dry = opts["dry_run"]
        anonymize = opts["anonymize"]

        cutoff = timezone.now() - timedelta(days=months * 30)
        qs = ContactMessage.objects.filter(created_at__lt=cutoff)
        count = qs.count()

        if dry:
            what = "anonymized" if anonymize else "deleted"
            self.stdout.write(self.style.WARNING(
                f"[DRY-RUN] Would be {what}: {count} messages older than ~{months} months (before {cutoff.date()})"
            ))
            return

        with transaction.atomic():
            if anonymize:
                affected = _anonymize(qs)
                self.stdout.write(self.style.SUCCESS(
                    f"Anonymized {affected} messages older than ~{months} months (before {cutoff.date()})"
                ))
            else:
                affected = qs.delete()[0]
                self.stdout.write(self.style.SUCCESS(
                    f"Deleted {affected} messages older than ~{months} months (before {cutoff.date()})"
                ))
