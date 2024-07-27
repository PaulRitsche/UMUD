import unittest
import pandas as pd
import streamlit as st
from unittest.mock import patch, MagicMock
from webapp.webapp import (
    clean_dataframe,
    get_categorical_columns,
    read_newsfeed,
    load_scoreboard,
    filter_dataframe,
    create_email_link,
)


class TestWebAppFunctions(unittest.TestCase):

    def test_clean_dataframe(self):
        df = pd.DataFrame({"col1": ["test", "data", "with", "unicode", "🚀"]})
        cleaned_df = clean_dataframe(df)
        self.assertEqual(
            list(cleaned_df["col1"]), ["test", "data", "with", "unicode", ""]
        )

    def test_get_categorical_columns(self):
        df = pd.DataFrame(
            {"cat1": ["a", "b", "c"], "num1": [1, 2, 3], "cat2": ["x", "y", "z"]}
        )
        cat_cols = get_categorical_columns(df)
        self.assertEqual(set(cat_cols), {"cat1", "cat2"})

    def test_read_newsfeed(self):
        with patch(
            "builtins.open",
            unittest.mock.mock_open(read_data="News item 1\nNews item 2\nNews item 3"),
        ):
            news_items = read_newsfeed("dummy_path.txt")
        self.assertEqual(news_items, ["News item 1", "News item 2", "News item 3"])

    def test_load_scoreboard(self):
        scoreboard = load_scoreboard()
        self.assertIsInstance(scoreboard, pd.DataFrame)
        self.assertEqual(
            list(scoreboard.columns),
            [
                "Name",
                "SEM Fascicle Length (cm)",
                "SEM Pennation Angle (cm)",
                "SEM Muscle Thickness (cm)",
            ],
        )

    @patch("webapp.AgGrid")
    def test_filter_dataframe(self, mock_aggrid):
        mock_aggrid.return_value = {"data": pd.DataFrame({"col1": [1, 2, 3]})}
        df = pd.DataFrame({"col1": [1, 2, 3, 4, 5]})
        result = filter_dataframe(df)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 3)

    def test_create_email_link(self):
        link = create_email_link(
            "Test Subject", "Test Body", "test@example.com", ["file1.txt", "file2.txt"]
        )
        self.assertIn("mailto:", link)
        self.assertIn("subject=Test%20Subject", link)
        self.assertIn("body=Test%20Body", link)
        self.assertIn("to=test%40example.com", link)


if __name__ == "__main__":
    unittest.main()
