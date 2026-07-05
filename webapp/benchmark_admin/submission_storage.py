from pathlib import Path
import json
import pandas as pd
import shutil

def list_pending_submissions():
    submissions_folder = (
        Path(__file__).parent.parent
        / 'benchmark_data'
        / 'submissions'
    )

    metadata_files = submissions_folder.glob('*_metadata.json')

    pending_submissions = []

    for metadata_file in metadata_files:
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)

        if metadata.get('status') == 'pending':
            pending_submissions.append(metadata)

    return pending_submissions

def load_submission(model_name, folder='submissions'):
    submissions_folder = (
        Path(__file__).parent.parent
        / 'benchmark_data'
        / folder
    )

    csv_path = submissions_folder / f'{model_name}.csv'

    metadata_path = (
        submissions_folder
        / f'{model_name}_metadata.json'
    )

    predictions = pd.read_csv(csv_path, sep=',')

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    submission = {
        'metadata': metadata,
        'predictions': predictions,
        "model_name": model_name
    }

    return submission

def approve_submission(model_name):
    submissions_folder = (
        Path(__file__).parent.parent
        / 'benchmark_data'
        / 'submissions'
    )

    approved_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
        / "approved_submissions"
    )

    approved_folder.mkdir(exist_ok=True)

    metadata_path = (
        submissions_folder
        / f'{model_name}_metadata.json'
    )

    with open(metadata_path, 'r') as f:
        metadata = json.load(f)

    metadata['status'] = 'approved'

    with open(metadata_path, 'w') as f:
        json.dump(
            metadata,
            f,
            indent=4
        )

    source_csv = (
        submissions_folder
        / f"{model_name}.csv"
    )

    destination_csv = (
        approved_folder
        / f"{model_name}.csv"
    )

    shutil.move(
        source_csv,
        destination_csv
    )

    destination_metadata = (
        approved_folder
        / f"{model_name}_metadata.json"
    )

    shutil.move(
        metadata_path,
        destination_metadata
    )

def reject_submission(model_name):

    submissions_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
        / "submissions"
    )

    rejected_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
        / "rejected_submissions"
    )

    rejected_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    metadata_path = (
        submissions_folder
        / f"{model_name}_metadata.json"
    )

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    metadata["status"] = "rejected"

    with open(metadata_path, "w") as f:
        json.dump(
            metadata,
            f,
            indent=4
        )

    source_csv = (
        submissions_folder
        / f"{model_name}.csv"
    )

    destination_csv = (
        rejected_folder
        / f"{model_name}.csv"
    )

    shutil.move(
        source_csv,
        destination_csv
    )

    destination_metadata = (
        rejected_folder
        / f"{model_name}_metadata.json"
    )

    shutil.move(
        metadata_path,
        destination_metadata
    )

