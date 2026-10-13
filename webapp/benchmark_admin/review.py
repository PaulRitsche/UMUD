import os
from pathlib import Path

from submission_storage import list_pending_submissions, load_submission, approve_submission, reject_submission
from review_tools import (
    open_submission_csv,
    load_image_benchmark,
    load_video_benchmark,
    build_imagewise_comparison,
    build_video_framewise_comparison,
    build_summary_dataframe,
    build_video_summary_dataframe,
    export_comparison,
    load_acsa_benchmark,
    build_acsa_imagewise_comparison,
    build_acsa_summary_dataframe,
    )

def main():

    while True:

        pending = list_pending_submissions()

        print()
        print('=' * 50)
        print("UMUD Benchmark Review")
        print('=' * 50)
        print()

        print(f"Pending submissions: {len(pending)}")
        print()

        if len(pending) == 0:
            print('No pending submissions for review')
            return

        for index, submission in enumerate(pending, start=1):
            print(f"{index}) {submission['model_name']}")
            print(f"Benchmark: {submission['benchmark_task']}")
            print(f"Submission Date: {submission['submission_date']}")
            print()

        print('0) Exit')
        print()

        selection = int(input('Select Submission: '))

        if selection == 0:
            break

        selected_submission = pending[selection - 1]

        print()
        print(
            f"You selected: Index {selection}, Model Name: {selected_submission['model_name']}"
        )

        while True:

            print()
            print('=' * 50)
            print('Available Actions')
            print('=' * 50)

            print(f'1) Open submission CSV')
            print(f'2) Generate benchmark comparison report')
            print(f'3) Approve submission')
            print(f'4) Reject submission')
            print(f'5) Go back')
            print()

            action = input("Select action: ")

            if action == '1':
                action_name = 'Open submission CSV'

                open_submission_csv(
                    selected_submission['model_name']
                )

            elif action == '2':
                action_name = ' Generate benchmark comparison report'

                submission = load_submission(
                selected_submission["model_name"]
            )

                if (
                    selected_submission["benchmark_task"]
                    == "Muscle Architecture (Images)"
                ):

                    benchmark = load_image_benchmark()

                    comparison_df = build_imagewise_comparison(
                        submission["predictions"],
                        benchmark,
                        selected_submission["model_name"]
                    )

                    summary_df = build_summary_dataframe(
                        comparison_df,
                        selected_submission["model_name"]
                    )

                elif (
                    selected_submission["benchmark_task"]
                    == "Muscle Architecture (Video)"
                ):

                    benchmark = load_video_benchmark()

                    comparison_df = build_video_framewise_comparison(
                        submission["predictions"],
                        benchmark,
                        selected_submission["model_name"]
                    )

                    summary_df = build_video_summary_dataframe(
                        comparison_df,
                        selected_submission["model_name"]
                    )

                elif (
                    selected_submission["benchmark_task"]
                    == "ACSA Quantification"
                ):

                    benchmark = load_acsa_benchmark()

                    comparison_df = build_acsa_imagewise_comparison(
                        submission["predictions"],
                        benchmark,
                        selected_submission["model_name"]
                    )

                    summary_df = build_acsa_summary_dataframe(
                        comparison_df,
                        selected_submission["model_name"]
                    )

                else:

                    print("Unsupported benchmark task.")
                    continue

                print(comparison_df)
                print()
                print(summary_df)

                if (
                    selected_submission["benchmark_task"]
                    == "Muscle Architecture (Images)"
                ):

                    report_path = export_comparison(
                        summary_df,
                        comparison_df,
                        selected_submission["model_name"]
                    )

                elif (
                    selected_submission["benchmark_task"]
                    == "Muscle Architecture (Video)"
                ):

                    report_path = export_comparison(
                        summary_df,
                        comparison_df,
                        selected_submission["model_name"]
                    )

                elif (
                    selected_submission["benchmark_task"]
                    == "ACSA Quantification"
                ):

                    report_path = export_comparison(
                        summary_df,
                        comparison_df,
                        selected_submission["model_name"]
                    )

            elif action == '3':
                action_name = 'Approve submission'

                approve_submission(
                    selected_submission['model_name']
                )

                print()
                print(f'{selected_submission["model_name"]} approved succesfully')
                
                input(
                    '\nPress ENTER to return to the submissions list...'
                )

                break

            elif action == '4':
                action_name = 'Reject submission'

                reject_submission(
                    selected_submission['model_name']
                )

                print()
                print(f'{selected_submission["model_name"]} rejected and moved to the rejected submissions folder')

                input(
                    '\nPress ENTER to return to the submissions list...'
                )

                break

            elif action == '5':
                break

            else:
                action_name = 'Unknown'

if __name__ == '__main__':
    main()