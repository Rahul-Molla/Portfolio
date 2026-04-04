import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from portfolio.models import UGCNetPYQ


REQUIRED_COLUMNS = [
    "paper",
    "subject",
    "year",
    "question_text",
    "option_a",
    "option_b",
    "option_c",
    "option_d",
    "correct_option",
    "solution",
    "explanation",
]


class Command(BaseCommand):
    help = "Bulk import UGC NET PYQ questions from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str, help="Path to CSV file")
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Delete existing PYQs before import",
        )

    def handle(self, *args, **options):
        csv_path = Path(options["csv_path"]).expanduser()
        if not csv_path.exists() or not csv_path.is_file():
            raise CommandError(f"CSV file not found: {csv_path}")

        if options["replace"]:
            deleted, _ = UGCNetPYQ.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted existing entries: {deleted}"))

        created_count = 0
        updated_count = 0
        skipped_count = 0

        with csv_path.open("r", encoding="utf-8-sig", newline="") as fp:
            reader = csv.DictReader(fp)
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in (reader.fieldnames or [])]
            if missing_cols:
                raise CommandError("Missing required CSV columns: " + ", ".join(missing_cols))

            for row_index, row in enumerate(reader, start=2):
                try:
                    paper = (row.get("paper") or "").strip().lower()
                    if paper not in {"paper-1", "paper-2"}:
                        raise ValueError("paper must be paper-1 or paper-2")

                    correct_option = (row.get("correct_option") or "").strip().upper()
                    if correct_option not in {"A", "B", "C", "D"}:
                        raise ValueError("correct_option must be one of A, B, C, D")

                    question_text = (row.get("question_text") or "").strip()
                    subject = (row.get("subject") or "").strip()
                    if not question_text or not subject:
                        raise ValueError("subject and question_text are required")

                    year_value = int((row.get("year") or "").strip())

                    defaults = {
                        "subject": subject,
                        "year": year_value,
                        "option_a": (row.get("option_a") or "").strip(),
                        "option_b": (row.get("option_b") or "").strip(),
                        "option_c": (row.get("option_c") or "").strip(),
                        "option_d": (row.get("option_d") or "").strip(),
                        "correct_option": correct_option,
                        "solution": (row.get("solution") or "").strip(),
                        "explanation": (row.get("explanation") or "").strip(),
                        "is_active": (row.get("is_active") or "true").strip().lower() != "false",
                        "order": int((row.get("order") or "1").strip()),
                    }

                    obj, created = UGCNetPYQ.objects.update_or_create(
                        paper=paper,
                        question_text=question_text,
                        defaults=defaults,
                    )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1

                except Exception as exc:
                    skipped_count += 1
                    self.stdout.write(self.style.WARNING(f"Row {row_index} skipped: {exc}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Import complete. Created: {created_count}, Updated: {updated_count}, Skipped: {skipped_count}"
            )
        )
