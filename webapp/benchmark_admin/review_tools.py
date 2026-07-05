from pathlib import Path
import os
import pandas as pd
import tempfile
import openpyxl
try:
    from .submission_storage import load_submission
except ImportError:
    from submission_storage import load_submission

# Option 1 from the menu: open de submission's CSV
def open_submission_csv(model_name):

    submissions_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
        / "submissions"
    )

    csv_path = submissions_folder / f"{model_name}.csv"

    os.startfile(csv_path)

# Option 2 from the menu: generate the benchmark comparison report

def load_benchmark():

    benchmark_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
    )

    benchmark_path = (
        benchmark_folder
        / "35_images_benchmark_summary.csv"
    )

    benchmark_df = pd.read_csv(
        benchmark_path,
        sep=","
    )

    return benchmark_df

def load_video_benchmark():

    benchmark_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
    )

    benchmark_path = (
        benchmark_folder
        / "benchmark_architecture_GM_calf_raise_v0.1.0.csv"
    )

    benchmark_df = pd.read_csv(
        benchmark_path,
        sep=","
    )

    return benchmark_df

def build_imagewise_comparison(
    submission_df,
    benchmark_df,
    model_name
):

    merged_df = pd.merge(submission_df, benchmark_df, on = 'image_id', how = 'left')

    comparison_df = pd.DataFrame({
        'Image': merged_df['image_id'],
        'FL Experts': 
            merged_df['AVG_FL'].round(1).astype(str)
            + ' ± '
            + merged_df['SD_FL'].round(1).astype(str),
        f'{model_name} FL':
            merged_df['fl_mm'].round(1),
        f'{model_name} FL Error':
            (merged_df['AVG_FL'] - merged_df['fl_mm']).abs().round(1),
        'MT Experts':
            merged_df['AVG_MT'].round(1).astype(str)
            + ' ± '
            + merged_df['SD_MT'].round(1).astype(str),
        f'{model_name} MT':
            merged_df['mt_mm'].round(1),
        f'{model_name} MT Error':
            (merged_df['AVG_MT'] - merged_df['mt_mm']).abs().round(1),
        'PA Experts':
            merged_df['AVG_PA'].round(1).astype(str)
            + ' ± '
            + merged_df['SD_PA'].round(1).astype(str),
        f'{model_name} PA':
            merged_df['pa_deg'].round(1),
        f'{model_name} PA Error':
            (merged_df['AVG_PA'] - merged_df['pa_deg']).abs().round(1)
    })

    return comparison_df

def build_video_framewise_comparison(
    submission_df,
    benchmark_df,
    model_name
):

    merged_df = pd.merge(
        submission_df,
        benchmark_df,
        on="frame",
        how="left"
    )

    comparison_df = pd.DataFrame({

        "Frame":
            merged_df["frame"],

        "FL Experts":
            merged_df["mean_fl_gm"].round(1).astype(str)
            + " ± "
            + merged_df["std_fl_gm"].round(1).astype(str),

        f"{model_name} FL":
            merged_df["fl_mm"].round(1),

        f"{model_name} FL Error":
            (
                merged_df["mean_fl_gm"]
                - merged_df["fl_mm"]
            ).abs().round(1),

        "PA Experts":
            merged_df["mean_pa_gm"].round(1).astype(str)
            + " ± "
            + merged_df["std_pa_gm"].round(1).astype(str),

        f"{model_name} PA":
            merged_df["pa_deg"].round(1),

        f"{model_name} PA Error":
            (
                merged_df["mean_pa_gm"]
                - merged_df["pa_deg"]
            ).abs().round(1)

    })

    return comparison_df

def build_web_imagewise_comparison(selected_models):

    benchmark_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
    )

    benchmark_path = (
        benchmark_folder
        / "35_images_benchmark_summary.csv"
    )

    benchmark_df = pd.read_csv(
        benchmark_path,
        sep=","
    )

    benchmark_df["FL Experts"] = (
        benchmark_df["AVG_FL"].round(1).astype(str)
        + " ± "
        + benchmark_df["SD_FL"].round(1).astype(str)
    )

    benchmark_df["MT Experts"] = (
        benchmark_df["AVG_MT"].round(1).astype(str)
        + " ± "
        + benchmark_df["SD_MT"].round(1).astype(str)
    )

    benchmark_df["PA Experts"] = (
        benchmark_df["AVG_PA"].round(1).astype(str)
        + " ± "
        + benchmark_df["SD_PA"].round(1).astype(str)
    )

    display_df = pd.DataFrame()

    display_df["image_id"] = benchmark_df["image_id"]

    display_df["FL Experts"] = benchmark_df["FL Experts"]

    approved_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
        / "approved_submissions"
    )

    for model_name in selected_models:

        model_path = approved_folder / f"{model_name}.csv"

        model_df = pd.read_csv(
            model_path,
            sep=","
        )

        display_df[f"{model_name} FL"] = (
            model_df["fl_mm"]
            .round(1)
            .fillna("-")
        )

        display_df[f"{model_name} FL MAE"] = (
            (model_df["fl_mm"] - benchmark_df["AVG_FL"])
            .abs()
            .round(2)
            .fillna("-")
        )

    display_df["MT Experts"] = benchmark_df["MT Experts"]

    for model_name in selected_models:

        model_path = approved_folder / f"{model_name}.csv"

        model_df = pd.read_csv(
            model_path,
            sep=","
        )

        display_df[f"{model_name} MT"] = (
            model_df["mt_mm"]
            .round(1)
            .fillna("-")
        )

        display_df[f"{model_name} MT MAE"] = (
            (model_df["mt_mm"] - benchmark_df["AVG_MT"])
            .abs()
            .round(2)
            .fillna("-")
        )

    display_df["PA Experts"] = benchmark_df["PA Experts"]

    for model_name in selected_models:

        model_path = approved_folder / f"{model_name}.csv"

        model_df = pd.read_csv(
            model_path,
            sep=","
        )

        display_df[f"{model_name} PA"] = (
            model_df["pa_deg"]
            .round(1)
            .fillna("-")
        )

        display_df[f"{model_name} PA MAE"] = (
            (model_df["pa_deg"] - benchmark_df["AVG_PA"])
            .abs()
            .round(2)
            .fillna("-")
        )

    return display_df

def build_web_video_framewise_comparison(selected_models):

    benchmark_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
    )

    benchmark_path = (
        benchmark_folder
        / "benchmark_architecture_GM_calf_raise_v0.1.0.csv"
    )

    benchmark_df = pd.read_csv(
        benchmark_path,
        sep=","
    )

    benchmark_df["FL Experts"] = (
        benchmark_df["mean_fl_gm"].round(1).astype(str)
        + " ± "
        + benchmark_df["std_fl_gm"].round(1).astype(str)
    )

    benchmark_df["PA Experts"] = (
        benchmark_df["mean_pa_gm"].round(1).astype(str)
        + " ± "
        + benchmark_df["std_pa_gm"].round(1).astype(str)
    )

    display_df = pd.DataFrame()

    display_df["Frame"] = benchmark_df["frame"]

    display_df["FL Experts"] = benchmark_df["FL Experts"]

    approved_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
        / "approved_submissions"
    )

    for model_name in selected_models:

        submission = load_submission(
            model_name,
            folder="approved_submissions"
        )

        if (
            submission["metadata"].get("benchmark_task")
            != "Muscle Architecture (Video)"
        ):
            continue

        model_df = submission["predictions"]

        display_df[f"{model_name} FL"] = (
            model_df["fl_mm"]
            .round(1)
            .fillna("-")
        )

        display_df[f"{model_name} FL MAE"] = (
            (model_df["fl_mm"] - benchmark_df["mean_fl_gm"])
            .abs()
            .round(2)
            .fillna("-")
        )

    display_df["PA Experts"] = benchmark_df["PA Experts"]

    for model_name in selected_models:

        submission = load_submission(
            model_name,
            folder="approved_submissions"
        )

        if (
            submission["metadata"].get("benchmark_task")
            != "Muscle Architecture (Video)"
        ):
            continue

        model_df = submission["predictions"]

        display_df[f"{model_name} PA"] = (
            model_df["pa_deg"]
            .round(1)
            .fillna("-")
        )

        display_df[f"{model_name} PA MAE"] = (
            (model_df["pa_deg"] - benchmark_df["mean_pa_gm"])
            .abs()
            .round(2)
            .fillna("-")
        )

    return display_df


def build_summary_dataframe(comparison_df, model_name):
    summary_df = pd.DataFrame({
        'Model': [model_name],
        'FL MAE (mm)': [
            comparison_df[f'{model_name} FL Error'].mean()
        ],
        'MT MAE (mm)': [
            comparison_df[f'{model_name} MT Error'].mean()
        ],
        'PA MAE (°)': [
            comparison_df[f'{model_name} PA Error'].mean()
        ]
    })

    return summary_df

def build_video_summary_dataframe(
    comparison_df,
    model_name
):

    summary_df = pd.DataFrame({

        "Model":
            [model_name],

        "FL MAE (mm)":
            [
                comparison_df[
                    f"{model_name} FL Error"
                ].mean()
            ],

        "PA MAE (°)":
            [
                comparison_df[
                    f"{model_name} PA Error"
                ].mean()
            ]

    })

    return summary_df

def export_comparison(
    summary_df,
    comparison_df,
    model_name
):

    with tempfile.NamedTemporaryFile(
        suffix=".xlsx",
        prefix=f"{model_name}_",
        delete=False
    ) as tmp:

        report_path = tmp.name

    with pd.ExcelWriter(report_path) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        comparison_df.to_excel(
            writer,
            sheet_name="Image-wise Comparison",
            index=False
        )

    return report_path

def export_video_comparison(
    summary_df,
    comparison_df,
    model_name
):

    with tempfile.NamedTemporaryFile(
        suffix=".xlsx",
        prefix=f"{model_name}_",
        delete=False
    ) as tmp:

        report_path = tmp.name

    with pd.ExcelWriter(report_path) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        comparison_df.to_excel(
            writer,
            sheet_name="Frame-wise Comparison",
            index=False
        )

    return report_path

def build_global_summary():

    approved_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
        / "approved_submissions"
    )

    model_files = list(
        approved_folder.glob("*.csv")
    )

    benchmark_df = load_benchmark()

    summary_rows = []

    for model_file in model_files:

        model_name = model_file.stem

        submission = load_submission(
            model_name,
            folder="approved_submissions"
        )

        if (
            submission["metadata"].get("benchmark_task")
            != "Muscle Architecture (Images)"
        ):
            continue

        comparison_df = build_imagewise_comparison(
            submission["predictions"],
            benchmark_df,
            model_name
        )

        summary_df = build_summary_dataframe(
            comparison_df,
            model_name
        )

        summary_rows.append(summary_df)

    if len(summary_rows) == 0:

        return pd.DataFrame(
            columns=[
                "Model",
                "FL MAE (mm)",
                "MT MAE (mm)",
                "PA MAE (°)"
            ]
        )

    summary_df = pd.concat(
        summary_rows,
        ignore_index=True
    )

    summary_df = summary_df.round(2)

    return summary_df

def build_video_global_summary():

    approved_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
        / "approved_submissions"
    )

    model_files = list(
        approved_folder.glob("*.csv")
    )

    benchmark_df = load_video_benchmark()

    summary_rows = []

    for model_file in model_files:

        model_name = model_file.stem

        submission = load_submission(
            model_name,
            folder="approved_submissions"
        )

        if (
            submission["metadata"].get("benchmark_task")
            != "Muscle Architecture (Video)"
        ):
            continue

        comparison_df = build_video_framewise_comparison(
            submission["predictions"],
            benchmark_df,
            model_name
        )

        summary_df = build_video_summary_dataframe(
            comparison_df,
            model_name
        )

        summary_rows.append(summary_df)

    if len(summary_rows) == 0:

        return pd.DataFrame(
            columns=[
                "Model",
                "FL MAE (mm)",
                "PA MAE (°)"
            ]
        )

    summary_df = pd.concat(
        summary_rows,
        ignore_index=True
    )

    summary_df = summary_df.round(2)

    return summary_df