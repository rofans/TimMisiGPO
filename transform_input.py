import sys
import csv
import re


def parse_money(value):
    """Return cleaned numeric string (e.g., '$1,000' -> '1000') or '' if empty/unparseable."""
    if value is None:
        return ""
    s = str(value).strip()
    if not s:
        return ""
    s = s.replace("$", "").replace(",", "").replace("SGD", "").strip()
    if not s:
        return ""
    try:
        f = float(s)
        return str(int(f)) if f.is_integer() else str(f)
    except:
        digits = re.sub(r"[^\d.]", "", s)
        if digits.endswith(".0"):
            digits = digits[:-2]
        return digits


def is_selected(cell_value):
    """Interpret Google Form export selections. Accept 'Y/Yes/True/1/Ya/Iya' or any non-empty text."""
    if cell_value is None:
        return False
    s = str(cell_value).strip()
    if not s:
        return False
    return True


def transform(input_file, output_file):
    daya_cols = [
        'Bergabung dengan Tim Misi - Community Development Barelang',
        'Bergabung dengan Tim Misi - Partners Coordinator',
        'Mengikuti Befriender Ministry (Pekerja Migran Indonesia)',
        'Mengikuti Kunjungan Misi: Love Batam',
        'Diperlengkapi dan Dilatih melalui Pelatihan Penginjilan',
    ]
    doa_cols = [
        'Mengikuti Mezbah Doa Misi setiap minggu',
        'Mengikuti Malam Puji dan Doa (MPD) setiap bulan'
    ]

    with open(input_file, newline="", encoding="utf-8") as infile, \
         open(output_file, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Read header row (so we can map columns reliably)
        header = next(reader)
        idx = {name: i for i, name in enumerate(header)}

        def get(row, colname):
            i = idx.get(colname)
            if i is None or i >= len(row):
                return ""
            return row[i]

        for row_num, row in enumerate(reader, start=2):
            # --- Requirement 1 & 2: filter by FIRST COLUMN (Column A) ---
            col_a = (row[0] if len(row) > 0 else "").strip()
            if not col_a:
                continue
            if col_a.strip().lower() == "lunas":
                continue

            full = str(get(row, "Nama Lengkap")).strip()
            first = full.split()[0] if full else ""

            # Payment: prefer Bulanan, else Sekaligus
            sekal = parse_money(get(row, 'Saya berkomitmen Dana "Sekaligus" sebesar:'))
            bul = parse_money(get(row, 'Saya berkomitmen Dana "Setiap Bulan" sebesar'))
            if bul:
                pay_type, amount = "Bulanan", bul
            elif sekal:
                pay_type, amount = "Sekaligus", sekal
            else:
                pay_type, amount = "", ""

            # Daya text
            daya_selected = []
            for c in daya_cols:
                v = get(row, c)
                if is_selected(v):
                    s = str(v).strip()
                    if s.lower() in ("y", "yes", "true", "1", "ya", "iya"):
                        daya_selected.append(c)
                    else:
                        # sometimes the cell already contains option text
                        daya_selected.append(s)

            # dedupe while preserving order
            seen = set()
            daya_selected = [x for x in daya_selected if not (x in seen or seen.add(x))]
            daya_text = " dan ".join(daya_selected)

            # Doa text
            doa_selected = []
            for c in doa_cols:
                v = get(row, c)
                if is_selected(v):
                    s = str(v).strip()
                    if s.lower() in ("y", "yes", "true", "1", "ya", "iya"):
                        doa_selected.append(c)
                    else:
                        doa_selected.append(s)

            seen = set()
            doa_selected = [x for x in doa_selected if not (x in seen or seen.add(x))]
            doa_text = " dan ".join(doa_selected)

            code = col_a  # Column A value becomes output col 6
            email = str(get(row, "Email Address")).strip()
            phone = re.sub(r"\D", "", str(get(row, "Nomor HP")).strip())

            out_row = [first, full, pay_type, amount, daya_text, doa_text, code, email, phone]

            # --- Requirement 3: replace empty output cells with N/A ---
            #out_row = [v if (isinstance(v, str) and v.strip()) or (not isinstance(v, str) and v is not None) else "N/A"
            #           for v in out_row]

            cleaned_row = []

            for v in out_row:
                if v is None:
                    cleaned_row.append("N/A")
                    continue

                s = str(v).strip()

                # Replace empty or "Nil" (any case) with N/A
                if not s or s.lower() == "nil":
                    cleaned_row.append("N/A")
                else:
                    cleaned_row.append(s)

            out_row = cleaned_row

            writer.writerow(out_row)

    print("Transformation complete.")
    print(f"Input:  {input_file}")
    print(f"Output: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python transform.py <input.csv> <output.csv>")
        sys.exit(1)

    transform(sys.argv[1], sys.argv[2])
