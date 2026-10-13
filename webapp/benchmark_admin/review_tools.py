from pathlib import Path
import os
import pandas as pd
import tempfile
import openpyxl
import pingouin as pg
try:
    from .submission_storage import load_submission
except ImportError:
    from submission_storage import load_submission

# Common functions

def open_submission_csv(model_name):

    submissions_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
        / "submissions"
    )

    csv_path = submissions_folder / f"{model_name}.csv"

    os.startfile(csv_path)

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

#----------------
# Image functions
#----------------

def load_image_benchmark():

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
        sep=";"
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

        # Numeric values for statistics
        'FL Reference':
            merged_df['AVG_FL'],

        'MT Reference':
            merged_df['AVG_MT'],

        'PA Reference':
            merged_df['AVG_PA'],

        # Formatted values for display
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
        sep=";"
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

        display_df[f"{model_name} FL Error"] = (
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

        display_df[f"{model_name} MT Error"] = (
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

        display_df[f"{model_name} PA Error"] = (
            (model_df["pa_deg"] - benchmark_df["AVG_PA"])
            .abs()
            .round(2)
            .fillna("-")
        )

    return display_df

def build_summary_dataframe(comparison_df, model_name):
    fl_reference = comparison_df["FL Reference"]
    fl_prediction = comparison_df[f"{model_name} FL"]

    mt_reference = comparison_df["MT Reference"]
    mt_prediction = comparison_df[f"{model_name} MT"]

    pa_reference = comparison_df["PA Reference"]
    pa_prediction = comparison_df[f"{model_name} PA"]

    fl_valid = pd.DataFrame({
        "Reference": fl_reference,
        "Prediction": fl_prediction
    }).dropna()

    mt_valid = pd.DataFrame({
        "Reference": mt_reference,
        "Prediction": mt_prediction
    }).dropna()

    pa_valid = pd.DataFrame({
        "Reference": pa_reference,
        "Prediction": pa_prediction
    }).dropna()

    fl_reference = fl_valid["Reference"]
    fl_prediction = fl_valid["Prediction"]

    mt_reference = mt_valid["Reference"]
    mt_prediction = mt_valid["Prediction"]

    pa_reference = pa_valid["Reference"]
    pa_prediction = pa_valid["Prediction"]

    # Bias - Mean signed difference between model predictions and expert reference values.

    fl_bias = (fl_prediction - fl_reference).mean()

    mt_bias = (mt_prediction - mt_reference).mean()

    pa_bias = (pa_prediction - pa_reference).mean()

    # CV (Coefficient of Variation) - Standard deviation of the prediction differences, normalized by the mean reference value (%).

    fl_difference = fl_prediction - fl_reference

    mt_difference = mt_prediction - mt_reference

    pa_difference = pa_prediction - pa_reference

    fl_cv = (
        fl_difference.std(ddof=1)
        / fl_reference.mean()
    ) * 100

    mt_cv = (
        mt_difference.std(ddof=1)
        / mt_reference.mean()
    ) * 100

    pa_cv = (
        pa_difference.std(ddof=1)
        / pa_reference.mean()
    ) * 100

    # ICC (Intraclass Correlation Coefficient) - ICC(2,1): two-way random-effects, absolute agreement, single measurement. Quantifies how consistently the model reproduces the expert reference measurements.

    ## FL ICC

    fl_icc_df = pd.DataFrame({
        "Image": list(fl_valid.index) * 2,
        "Rater": (
            ["Reference"] * len(fl_valid)
            + [model_name] * len(fl_valid)
        ),
        "Score": pd.concat(
            [
                fl_reference,
                fl_prediction
            ],
            ignore_index=True
        )
    })

    fl_icc_results = pg.intraclass_corr(
        data=fl_icc_df,
        targets="Image",
        raters="Rater",
        ratings="Score"
    )

    fl_icc = (
        fl_icc_results.loc[
            fl_icc_results["Type"] == "ICC2",
            "ICC"
        ].iloc[0]
    )

    # MT ICC

    mt_icc_df = pd.DataFrame({
        "Image": list(mt_valid.index) * 2,
        "Rater": (
            ["Reference"] * len(mt_valid)
            + [model_name] * len(mt_valid)
        ),
        "Score": pd.concat(
            [
                mt_reference,
                mt_prediction
            ],
            ignore_index=True
        )
    })

    mt_icc_results = pg.intraclass_corr(
        data=mt_icc_df,
        targets="Image",
        raters="Rater",
        ratings="Score"
    )

    mt_icc = (
        mt_icc_results.loc[
            mt_icc_results["Type"] == "ICC2",
            "ICC"
        ].iloc[0]
    )

    # PA ICC

    pa_icc_df = pd.DataFrame({
        "Image": list(pa_valid.index) * 2,
        "Rater": (
            ["Reference"] * len(pa_valid)
            + [model_name] * len(pa_valid)
        ),
        "Score": pd.concat(
            [
                pa_reference,
                pa_prediction
            ],
            ignore_index=True
        )
    })

    pa_icc_results = pg.intraclass_corr(
        data=pa_icc_df,
        targets="Image",
        raters="Rater",
        ratings="Score"
    )

    pa_icc = (
        pa_icc_results.loc[
            pa_icc_results["Type"] == "ICC2",
            "ICC"
        ].iloc[0]
    )

    summary_df = pd.DataFrame({
        "Model": [
            model_name
        ],

        # Fascicle Length

        "FL MAE (mm)": [
            (fl_prediction - fl_reference).abs().mean()
        ],

        "FL ICC": [
            fl_icc
        ],

        "FL CV (%)": [
            fl_cv
        ],

        "FL Bias (mm)": [
            fl_bias
        ],

        # Muscle Thickness

        "MT MAE (mm)": [
            (mt_prediction - mt_reference).abs().mean()
        ],

        "MT ICC": [
            mt_icc
        ],

        "MT CV (%)": [
            mt_cv
        ],

        "MT Bias (mm)": [
            mt_bias
        ],

        # Pennation Angle

        "PA MAE (°)": [
            (pa_prediction - pa_reference).abs().mean()
        ],

        "PA ICC": [
            pa_icc
        ],

        "PA CV (%)": [
            pa_cv
        ],

        "PA Bias (°)": [
            pa_bias
        ],
    })

    return summary_df

def build_image_global_summary():

    approved_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
        / "approved_submissions"
    )

    model_files = list(
        approved_folder.glob("*.csv")
    )

    benchmark_df = load_image_benchmark()

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

#----------------
# Video functions
#----------------

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

        # Numeric values for statistics

        "FL Reference":
            merged_df["mean_fl_gm"],

        "PA Reference":
            merged_df["mean_pa_gm"],

        # Formatted values for display

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

        display_df[f"{model_name} FL Error"] = (
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

        display_df[f"{model_name} PA Error"] = (
            (model_df["pa_deg"] - benchmark_df["mean_pa_gm"])
            .abs()
            .round(2)
            .fillna("-")
        )

    return display_df

def build_video_summary_dataframe(
    comparison_df,
    model_name
):

    fl_reference = comparison_df["FL Reference"]
    fl_prediction = comparison_df[f"{model_name} FL"]

    pa_reference = comparison_df["PA Reference"]
    pa_prediction = comparison_df[f"{model_name} PA"]

    fl_valid = pd.DataFrame({
        "Reference": fl_reference,
        "Prediction": fl_prediction
    }).dropna()

    pa_valid = pd.DataFrame({
        "Reference": pa_reference,
        "Prediction": pa_prediction
    }).dropna()

    fl_reference = fl_valid["Reference"]
    fl_prediction = fl_valid["Prediction"]

    pa_reference = pa_valid["Reference"]
    pa_prediction = pa_valid["Prediction"]

    # Bias - Mean signed difference between model predictions and expert reference values.

    fl_bias = (fl_prediction - fl_reference).mean()

    pa_bias = (pa_prediction - pa_reference).mean()

    # CV (Coefficient of Variation) - Standard deviation of the prediction differences, normalized by the mean reference value (%).

    fl_difference = fl_prediction - fl_reference

    pa_difference = pa_prediction - pa_reference

    fl_cv = (
        fl_difference.std(ddof=1)
        / fl_reference.mean()
    ) * 100

    pa_cv = (
        pa_difference.std(ddof=1)
        / pa_reference.mean()
    ) * 100

    # ICC (Intraclass Correlation Coefficient) - ICC(2,1): two-way random-effects, absolute agreement, single measurement. Quantifies how consistently the model reproduces the expert reference measurements.

    # FL ICC

    fl_icc_df = pd.DataFrame({
        "Image": list(fl_valid.index) * 2,
        "Rater": (
            ["Reference"] * len(fl_valid)
            + [model_name] * len(fl_valid)
        ),
        "Score": pd.concat(
            [
                fl_reference,
                fl_prediction
            ],
            ignore_index=True
        )
    })

    fl_icc_results = pg.intraclass_corr(
        data=fl_icc_df,
        targets="Image",
        raters="Rater",
        ratings="Score"
    )

    fl_icc = (
        fl_icc_results.loc[
            fl_icc_results["Type"] == "ICC2",
            "ICC"
        ].iloc[0]
    )

    # PA ICC

    pa_icc_df = pd.DataFrame({
        "Image": list(pa_valid.index) * 2,
        "Rater": (
            ["Reference"] * len(pa_valid)
            + [model_name] * len(pa_valid)
        ),
        "Score": pd.concat(
            [
                pa_reference,
                pa_prediction
            ],
            ignore_index=True
        )
    })

    pa_icc_results = pg.intraclass_corr(
        data=pa_icc_df,
        targets="Image",
        raters="Rater",
        ratings="Score"
    )

    pa_icc = (
        pa_icc_results.loc[
            pa_icc_results["Type"] == "ICC2",
            "ICC"
        ].iloc[0]
    )

    summary_df = pd.DataFrame({
        "Model": [
            model_name
        ],

        # Fascicle Length

        "FL MAE (mm)": [
            (fl_prediction - fl_reference).abs().mean()
        ],

        "FL ICC": [
            fl_icc
        ],

        "FL CV (%)": [
            fl_cv
        ],

        "FL Bias (mm)": [
            fl_bias
        ],

        # Pennation Angle

        "PA MAE (°)": [
            (pa_prediction - pa_reference).abs().mean()
        ],

        "PA ICC": [
            pa_icc
        ],

        "PA CV (%)": [
            pa_cv
        ],

        "PA Bias (°)": [
            pa_bias
        ],
    })

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

                # Fascicle Length

                "FL MAE (mm)",
                "FL ICC",
                "FL CV (%)",
                "FL Bias (mm)",

                # Pennation Angle

                "PA MAE (°)",
                "PA ICC",
                "PA CV (%)",
                "PA Bias (°)"
            ]
        )

    summary_df = pd.concat(
        summary_rows,
        ignore_index=True
    )

    summary_df = summary_df.round(2)

    return summary_df

#------------------------------
# ACSA Quantification functions
#------------------------------

def load_acsa_benchmark():
    benchmark_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
    )

    benchmark_path = (
        benchmark_folder
        / "benchmark_acsa_ei.csv"
    )

    benchmark_df = pd.read_csv(
        benchmark_path,
        sep=","
    )

    return benchmark_df

def build_acsa_imagewise_comparison(
    submission_df,
    benchmark_df,
    model_name
):

    merged_df = pd.merge(submission_df, benchmark_df, on = 'image_id', how = 'left')

    comparison_df = pd.DataFrame({
        'Image': merged_df['image_id'],

        # Numeric values for statistics
        'ACSA Reference':
            merged_df['Mean_Manual_ACSA'],

        'EI Reference':
            merged_df['Mean_EI_Manual'],

        # Formatted values for display
        'ACSA Experts': 
            merged_df['Mean_Manual_ACSA'].round(1).astype(str)
            + ' ± '
            + merged_df['SD_ACSA'].round(1).astype(str),
        f'{model_name} ACSA':
            merged_df['ACSA'].round(1),
        f'{model_name} ACSA Error':
            (merged_df['Mean_Manual_ACSA'] - merged_df['ACSA']).abs().round(1),
        'EI Experts':
            merged_df['Mean_EI_Manual'].round(1).astype(str)
            + ' ± '
            + merged_df['SD_EI'].round(1).astype(str),
        f'{model_name} EI':
            merged_df['EI'].round(1),
        f'{model_name} EI Error':
            (merged_df['Mean_EI_Manual'] - merged_df['EI']).abs().round(1),
    })

    return comparison_df

def build_web_acsa_imagewise_comparison(selected_models):

    benchmark_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
    )

    benchmark_path = (
        benchmark_folder
        / "benchmark_acsa_ei.csv"
    )

    benchmark_df = pd.read_csv(
        benchmark_path,
        sep=","
    )

    benchmark_df["ACSA Experts"] = (
        benchmark_df["Mean_Manual_ACSA"].round(1).astype(str)
        + " ± "
        + benchmark_df["SD_ACSA"].round(1).astype(str)
    )

    benchmark_df["EI Experts"] = (
        benchmark_df["Mean_EI_Manual"].round(1).astype(str)
        + " ± "
        + benchmark_df["SD_EI"].round(1).astype(str)
    )

    display_df = pd.DataFrame()

    display_df["image_id"] = benchmark_df["image_id"]

    display_df["ACSA Experts"] = benchmark_df["ACSA Experts"]

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

        display_df[f"{model_name} ACSA"] = (
            model_df["ACSA"]
            .round(1)
            .fillna("-")
        )

        display_df[f"{model_name} ACSA Error"] = (
            (model_df["ACSA"] - benchmark_df["Mean_Manual_ACSA"])
            .abs()
            .round(2)
            .fillna("-")
        )

    display_df["EI Experts"] = benchmark_df["EI Experts"]

    for model_name in selected_models:

        model_path = approved_folder / f"{model_name}.csv"

        model_df = pd.read_csv(
            model_path,
            sep=","
        )

        display_df[f"{model_name} EI"] = (
            model_df["EI"]
            .round(1)
            .fillna("-")
        )

        display_df[f"{model_name} EI Error"] = (
            (model_df["EI"] - benchmark_df["Mean_EI_Manual"])
            .abs()
            .round(2)
            .fillna("-")
        )

    return display_df

def build_acsa_summary_dataframe(comparison_df, model_name):
    acsa_reference = comparison_df["ACSA Reference"]
    acsa_prediction = comparison_df[f"{model_name} ACSA"]

    ei_reference = comparison_df["EI Reference"]
    ei_prediction = comparison_df[f"{model_name} EI"]

    acsa_valid = pd.DataFrame({
        "Reference": acsa_reference,
        "Prediction": acsa_prediction
    }).dropna()

    ei_valid = pd.DataFrame({
        "Reference": ei_reference,
        "Prediction": ei_prediction
    }).dropna()

    acsa_reference = acsa_valid["Reference"]
    acsa_prediction = acsa_valid["Prediction"]

    ei_reference = ei_valid["Reference"]
    ei_prediction = ei_valid["Prediction"]

    # Bias - Mean signed difference between model predictions and expert reference values.

    acsa_bias = (acsa_prediction - acsa_reference).mean()

    ei_bias = (ei_prediction - ei_reference).mean()

    # CV (Coefficient of Variation) - Standard deviation of the prediction differences, normalized by the mean reference value (%).

    acsa_difference = acsa_prediction - acsa_reference

    ei_difference = ei_prediction - ei_reference

    acsa_cv = (
        acsa_difference.std(ddof=1)
        / acsa_reference.mean()
    ) * 100

    ei_cv = (
        ei_difference.std(ddof=1)
        / ei_reference.mean()
    ) * 100

    # ICC (Intraclass Correlation Coefficient) - ICC(2,1): two-way random-effects, absolute agreement, single measurement. Quantifies how consistently the model reproduces the expert reference measurements.

    ## ACSA ICC

    acsa_icc_df = pd.DataFrame({
        "Image": list(acsa_valid.index) * 2,
        "Rater": (
            ["Reference"] * len(acsa_valid)
            + [model_name] * len(acsa_valid)
        ),
        "Score": pd.concat(
            [
                acsa_reference,
                acsa_prediction
            ],
            ignore_index=True
        )
    })

    acsa_icc_results = pg.intraclass_corr(
        data=acsa_icc_df,
        targets="Image",
        raters="Rater",
        ratings="Score"
    )

    acsa_icc = (
        acsa_icc_results.loc[
            acsa_icc_results["Type"] == "ICC2",
            "ICC"
        ].iloc[0]
    )

    # EI ICC

    ei_icc_df = pd.DataFrame({
        "Image": list(ei_valid.index) * 2,
        "Rater": (
            ["Reference"] * len(ei_valid)
            + [model_name] * len(ei_valid)
        ),
        "Score": pd.concat(
            [
                ei_reference,
                ei_prediction
            ],
            ignore_index=True
        )
    })

    ei_icc_results = pg.intraclass_corr(
        data=ei_icc_df,
        targets="Image",
        raters="Rater",
        ratings="Score"
    )

    ei_icc = (
        ei_icc_results.loc[
            ei_icc_results["Type"] == "ICC2",
            "ICC"
        ].iloc[0]
    )

    summary_df = pd.DataFrame({
        "Model": [
            model_name
        ],

        "ACSA MAE (cm2)": [
            (acsa_prediction - acsa_reference).abs().mean()
        ],

        "ACSA ICC": [
            acsa_icc
        ],

        "ACSA CV (%)": [
            acsa_cv
        ],

        "ACSA Bias (cm2)": [
            acsa_bias
        ],

        "EI MAE": [
            (ei_prediction - ei_reference).abs().mean()
        ],

        "EI ICC": [
            ei_icc
        ],

        "EI CV (%)": [
            ei_cv
        ],

        "EI Bias": [
            ei_bias
        ],
    })

    return summary_df

def build_acsa_global_summary():

    approved_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
        / "approved_submissions"
    )

    model_files = list(
        approved_folder.glob("*.csv")
    )

    benchmark_df = load_acsa_benchmark()

    summary_rows = []

    for model_file in model_files:

        model_name = model_file.stem

        submission = load_submission(
            model_name,
            folder="approved_submissions"
        )

        if (
            submission["metadata"].get("benchmark_task")
            != "ACSA Quantification"
        ):
            continue

        comparison_df = build_acsa_imagewise_comparison(
            submission["predictions"],
            benchmark_df,
            model_name
        )

        summary_df = build_acsa_summary_dataframe(
            comparison_df,
            model_name
        )

        summary_rows.append(summary_df)

    if len(summary_rows) == 0:

        return pd.DataFrame(
            columns=[
                "Model",

                # Fascicle Length

                "ACSA MAE (cm2)",
                "ACSA ICC",
                "ACSA CV (%)",
                "ACSA Bias (cm2)",

                # Pennation Angle

                "EI MAE",
                "EI ICC",
                "EI CV (%)",
                "EI Bias"
            ]
        )

    summary_df = pd.concat(
        summary_rows,
        ignore_index=True
    )

    summary_df = summary_df.round(2)

    return summary_df