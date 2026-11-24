from fileinput import filename
import random

from pathlib import Path


def breed_from_filename(filename: str) -> str:
    stem = Path(filename).stem
    breed, separator, image_number = stem.rpartition("_")

    if not separator or not breed or not image_number.isdecimal():
        raise ValueError(f"Unexpected pet image filename: {filename}")

    return breed


def parse_annotation_line(line: str) -> tuple[str, int]:
    image_id, class_id, _species_id, _bread_id = line.split()
    return image_id, int(class_id)


def load_annotations (file_path):
    records = [] 

    with open(file_path, encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            image_id, class_id = parse_annotation_line(line)
            breed = breed_from_filename(image_id)

            record = {
                "image_id": image_id,
                "class_id": class_id,
                "breed": breed,
            }

            records.append(record)

    return records



def split_trainval(records):
    records_by_breed = {}

    for record in records:
        breed = record["breed"]

        if breed not in records_by_breed:
            records_by_breed[breed] = []

        records_by_breed[breed].append(record)

    train_records = []
    val_records = []
    rng = random.Random(42)

    for breed_records in records_by_breed.values():
        rng.shuffle(breed_records)
        val_count = round(len(breed_records) * 0.2)

        val_records.extend(breed_records[:val_count])
        train_records.extend(breed_records[val_count:])

    return train_records, val_records


def find_missing_images(records, images_dir):
    """
    find image files that are missing from the dataset folder 
    """
    missing_images = []

    for record in records:
        filename = record["image_id"] + ".jpg"
        image_path = path(images_dir) / filename

        if not image_path.is_file():
            missing_images.append(filename)
    
    return missing_images