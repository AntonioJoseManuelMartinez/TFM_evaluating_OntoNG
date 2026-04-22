import argparse
import csv
import re
import tarfile
from pathlib import Path


def parse_filename(filename: str) -> dict:
    """
    Expected patterns such as:
    HiC_GM12878_DI_10kb.txt
    HiC_GM12878_GMAP_50kb.txt
    SPRITE_GM12878_IS_10kb.txt
    HiChIP_ES_GMAP_50kb.txt

    Parsed as:
    source_method, cell_type, calling_method, resolution
    """
    stem = Path(filename).stem
    parts = stem.split("_")

    source_method = parts[0] if len(parts) >= 1 else ""
    cell_type = parts[1] if len(parts) >= 2 else ""
    calling_method = parts[2] if len(parts) >= 3 else ""
    resolution = parts[3] if len(parts) >= 4 else ""

    return {
        "source_method": source_method,
        "cell_type": cell_type,
        "calling_method": calling_method,
        "resolution": resolution,
    }


def sanitize_id(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", text)


def main():
    parser = argparse.ArgumentParser(
        description="Extract all TAD .txt files from TAD_annotations.tar.gz and generate one CSV for OntoNG."
    )
    parser.add_argument(
        "--tar",
        required=True,
        help="Path to TAD_annotations.tar.gz"
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output CSV path"
    )
    args = parser.parse_args()

    tar_path = Path(args.tar)
    output_path = Path(args.output)

    rows = []

    with tarfile.open(tar_path, "r:gz") as tar:
        members = tar.getmembers()

        for member in members:
            if not member.isfile():
                continue

            base_name = Path(member.name).name

            # Only TAD text files
            if not base_name.endswith(".txt"):
                continue

            meta = parse_filename(base_name)

            extracted = tar.extractfile(member)
            if extracted is None:
                continue

            for raw_line in extracted:
                line = raw_line.decode("utf-8", errors="ignore").strip()
                if not line:
                    continue

                parts = line.split()
                if len(parts) < 3:
                    continue

                chromosome, start_pos, end_pos = parts[0], parts[1], parts[2]

                tad_id = sanitize_id(
                    f"{meta['source_method']}_{meta['cell_type']}_{meta['calling_method']}_{meta['resolution']}_{chromosome}_{start_pos}_{end_pos}"
                )

                rows.append({
                    "tad_id": tad_id,
                    "chromosome": chromosome,
                    "start_position": start_pos,
                    "end_position": end_pos,
                    "source_method": meta["source_method"],
                    "cell_type": meta["cell_type"],
                    "calling_method": meta["calling_method"],
                    "resolution": meta["resolution"],
                    "source_file": base_name,
                    "database_name": "TADKB"
                })

    if not rows:
        raise ValueError("No rows were generated. Check the tar.gz structure.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "tad_id",
                "chromosome",
                "start_position",
                "end_position",
                "source_method",
                "cell_type",
                "calling_method",
                "resolution",
                "source_file",
                "database_name",
            ],
            delimiter=";"
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV generated: {output_path}")
    print(f"Rows: {len(rows)}")


if __name__ == "__main__":
    main()
