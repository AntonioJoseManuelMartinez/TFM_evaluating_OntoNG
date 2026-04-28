import csv
from pathlib import Path

INPUT_FILE = "enh2disease-1.0.2.txt"
OUTPUT_FILE = "enh2disease_clean.csv"


def normalize_chromosome(value: str) -> str:
    if not value:
        return ""
    v = value.strip()
    if v.lower() == "na":
        return "NA"
    if v.lower().startswith("chr"):
        suffix = v[3:]
        if suffix.lower() == "x":
            return "chrX"
        if suffix.lower() == "y":
            return "chrY"
        return f"chr{suffix}"
    return v


def main():
    input_path = Path(INPUT_FILE)
    if not input_path.exists():
        raise FileNotFoundError(f"No se encuentra {INPUT_FILE}")

    rows = []

    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue

            parts = line.split("\t")
            if len(parts) != 6:
                continue

            enhancer_id, chromosome, start_pos, end_pos, associated_gene, disease_name = parts

            rows.append({
                "enhancer_id": enhancer_id.strip(),
                "chromosome": normalize_chromosome(chromosome),
                "start_position": start_pos.strip(),
                "end_position": end_pos.strip(),
                "associated_gene": associated_gene.strip(),
                "disease_name": disease_name.strip()
            })

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "enhancer_id",
                "chromosome",
                "start_position",
                "end_position",
                "associated_gene",
                "disease_name"
            ],
            delimiter=","
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Archivo generado: {OUTPUT_FILE} | filas: {len(rows)}")


if __name__ == "__main__":
    main()
