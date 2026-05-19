import json
from pathlib import Path


BASE_DIR = Path("remote_rag_results_ENdb")


FOLDER_NAME = "03_relations"
# FOLDER_NAME = "02_entities"

OUTPUT_FILE = FOLDER_NAME + "_combined.json"


def read_json(file_path):
    with open(file_path, "r", encoding="utf-8") as input_file:
        return json.load(input_file)


def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, indent=2, ensure_ascii=False)


def main():
    folder_path = BASE_DIR / FOLDER_NAME
    output_path = BASE_DIR / OUTPUT_FILE

    combined = {}

    for file_path in sorted(folder_path.glob("*.json")):
        combined[file_path.name] = read_json(file_path)

    save_json(output_path, combined)

    print("Combined file:", len(combined))
    print("Generated file:", output_path)


if __name__ == "__main__":
    main()
