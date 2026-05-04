import pandas as pd
import re
from itertools import product

INPUT_FILES = [
    "enhancer_main.txt",
    "enhancer_gene.txt",
    "enhancer_TF.txt",
]

OUTPUT_FILE = "endb_human_clean.csv"


def clean_text(value):
    if pd.isna(value):
        return ""
    value = str(value).strip()
    if value in {"--", "—", "无", "None", "nan", "NaN"}:
        return ""
    return value


def normalize_list_field(value):
    value = clean_text(value)
    if not value:
        return []

    value = value.replace(";", ",")
    value = value.replace("，", ",")
    value = value.replace("|", ",")
    parts = [p.strip() for p in value.split(",")]

    cleaned = []
    for p in parts:
        p = re.sub(r"\s+", " ", p).strip()
        if not p or p in {"--", "—", "无"}:
            continue
        cleaned.append(p)

    # quitar duplicados preservando orden
    seen = set()
    result = []
    for item in cleaned:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            result.append(item)
    return result


def species_is_human(value):
    value = clean_text(value).lower()
    return "human" in value


def build_tissue_context(tissue, cell):
    tissue = clean_text(tissue)
    cell = clean_text(cell)

    if tissue and cell:
        return f"{tissue} | {cell}"
    if tissue:
        return tissue
    if cell:
        return cell
    return ""


def read_source_file(path):
    # ENdb descargado suele venir tabulado
    return pd.read_csv(path, sep="\t", dtype=str, encoding="utf-8", keep_default_na=False)


def main():
    frames = []
    for file in INPUT_FILES:
        df = read_source_file(file)
        df["source_file"] = file
        frames.append(df)

    df = pd.concat(frames, ignore_index=True)

    # Filtrar a registros humanos o human,mouse
    df = df[df["Species"].apply(species_is_human)].copy()

    records = []

    for _, row in df.iterrows():
        enhancer_id = clean_text(row.get("Enhancer_id", ""))
        chromosome = clean_text(row.get("Chromosome", ""))
        start_position = clean_text(row.get("Start_position", ""))
        end_position = clean_text(row.get("End_position", ""))
        enhancer_type = clean_text(row.get("Enhancer_type", ""))
        disease_name = clean_text(row.get("Disease", ""))
        tissue_context = build_tissue_context(
            row.get("Tissue_class", ""),
            row.get("Cell_class", "")
        )

        target_genes = normalize_list_field(row.get("Target_gene", ""))
        tfs = normalize_list_field(row.get("TF_name", ""))

        # Si no hay genes o TFs, mantenemos fila igualmente
        if not target_genes:
            target_genes = [""]
        if not tfs:
            tfs = [""]

        for target_gene, tf in product(target_genes, tfs):
            records.append({
                "enhancer_id": enhancer_id,
                "chromosome": chromosome,
                "start_position": start_position,
                "end_position": end_position,
                "enhancer_type": enhancer_type,
                "tissue_context": tissue_context,
                "disease_name": disease_name,
                "target_gene": target_gene,
                "transcription_factor": tf,
            })

    out = pd.DataFrame(records)

    # limpiar filas totalmente vacías en los nodos relacionales
    out = out[
        out["enhancer_id"].astype(str).str.strip().ne("")
        & out["chromosome"].astype(str).str.strip().ne("")
        & out["start_position"].astype(str).str.strip().ne("")
        & out["end_position"].astype(str).str.strip().ne("")
    ].copy()

    # normalizar posiciones
    out["start_position"] = pd.to_numeric(out["start_position"], errors="coerce")
    out["end_position"] = pd.to_numeric(out["end_position"], errors="coerce")
    out = out.dropna(subset=["start_position", "end_position"])

    out["start_position"] = out["start_position"].astype(int)
    out["end_position"] = out["end_position"].astype(int)

    # quitar duplicados
    out = out.drop_duplicates().reset_index(drop=True)

    out.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"Archivo generado: {OUTPUT_FILE}")
    print(f"Filas finales: {len(out)}")
    print("Columnas:")
    print(list(out.columns))


if __name__ == "__main__":
    main()
