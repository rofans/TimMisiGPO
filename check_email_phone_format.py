import sys
import csv
import re

# Assumes your "2026-test1-style" CSV (NO HEADER) with fixed positions:
# 0: first name
# 1: full name
# 2: payment type
# 3: amount
# 4: daya
# 5: doa
# 6: code
# 7: email
# 8: phone (8 digits, e.g. 83188474)

EMAIL_COL_IDX = 7
PHONE_COL_IDX = 8

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_RE = re.compile(r"^\d{8}$")


def validate_csv(file_path: str) -> int:
    errors = []
    total_rows = 0

    with open(file_path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=",")
        for row_num, row in enumerate(reader, start=1):
            total_rows += 1

            # Basic length check
            if len(row) <= max(EMAIL_COL_IDX, PHONE_COL_IDX):
                errors.append(
                    f"Row {row_num}: Not enough columns (got {len(row)}), expected at least {max(EMAIL_COL_IDX, PHONE_COL_IDX) + 1}"
                )
                continue

            email = (row[EMAIL_COL_IDX] or "").strip()
            phone = (row[PHONE_COL_IDX] or "").strip()

            # Email validation
            if not email:
                errors.append(f"Row {row_num}: Email is empty (col {EMAIL_COL_IDX + 1})")
            elif not EMAIL_RE.match(email):
                errors.append(f"Row {row_num}: Invalid email '{email}' (col {EMAIL_COL_IDX + 1})")

            # Phone validation (must be exactly 8 digits)
            if not phone:
                errors.append(f"Row {row_num}: Phone is empty (col {PHONE_COL_IDX + 1})")
            elif not PHONE_RE.match(phone):
                errors.append(f"Row {row_num}: Invalid phone '{phone}' (expected 8 digits, col {PHONE_COL_IDX + 1})")

    if errors:
        print(f"❌ Found {len(errors)} issue(s) in {total_rows} row(s):\n")
        for e in errors:
            print(e)
        return 1

    print(f"✅ OK: All {total_rows} row(s) have valid email + 8-digit phone numbers.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_contacts.py <file.csv>")
        sys.exit(2)

    sys.exit(validate_csv(sys.argv[1]))
