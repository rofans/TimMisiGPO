import sys
import csv

def detect_empty_cells(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)

        has_empty = False

        for row_num, row in enumerate(reader, start=1):
            for col_idx, value in enumerate(row):
                if value is None or value.strip() == "":
                    has_empty = True
                    print(
                        f"Empty cell detected -> "
                        f"Row {row_num}, Column {col_idx + 1}"
                    )

        if not has_empty:
            print("✅ No empty cells found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_empty_cells_noheader.py <file.csv>")
        sys.exit(1)

    detect_empty_cells(sys.argv[1])
