import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
from backend.research import researcher


class TestResearchFunction(unittest.TestCase):
    @patch("backend.researcher.generate")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_research_successful_run(
        self, mock_exists, mock_makedirs, mock_open, mock_generate
    ):
        # Mocking os.path.exists to return False, so the directory is created
        mock_exists.return_value = False

        # Mocking the generate function to return a specific response
        mock_generate.return_value = (
            "# Research Report\nThis is a mock research report."
        )

        # Call the function
        response = research(
            model_name="Max",
            prospect_name="John Doe",
            company_name="Acme Corp",
            additional_information="Acme recently expanded operations",
            additional_context="",
            temperature=1,
            streaming=False,
        )

        # Assertions

        # Check if os.makedirs was called to create the 'logs' directory
        mock_makedirs.assert_called_once_with("./logs")

        # Check if generate was called with correct arguments
        mock_generate.assert_called_once()

        # Validate the prompt structure passed to the generate method
        prompt_argument = mock_generate.call_args[0][1]
        self.assertIn("You are an experienced research expert", prompt_argument)
        self.assertIn("Prospect name: John Doe", prompt_argument)
        self.assertIn("Company name: Acme Corp", prompt_argument)
        self.assertIn("Acme recently expanded operations", prompt_argument)

        # Check if the response is written to the file
        mock_open.assert_called_once_with("./logs/research_report.md", "w")
        mock_open().write.assert_called_once_with(
            "# Research Report\nThis is a mock research report."
        )

        # Check if the response returned is the one from the generate function
        self.assertEqual(response, "# Research Report\nThis is a mock research report.")

    @patch("backend.researcher.generate")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_research_no_folder_creation_if_exists(
        self, mock_exists, mock_makedirs, mock_open, mock_generate
    ):
        # Mocking os.path.exists to return True, so no directory is created
        mock_exists.return_value = True

        # Mocking the generate function to return a specific response
        mock_generate.return_value = (
            "# Research Report\nThis is a mock research report."
        )

        # Call the function
        research(
            model_name="Max",
            prospect_name="Jane Doe",
            company_name="Beta Corp",
            additional_information="",
            additional_context="",
            temperature=0.7,
            streaming=False,
        )

        # Assertions

        # Check that os.makedirs was not called since the folder exists
        mock_makedirs.assert_not_called()

        # Check if the response is written to the file
        mock_open.assert_called_once_with("./logs/research_report.md", "w")
        mock_open().write.assert_called_once_with(
            "# Research Report\nThis is a mock research report."
        )

    @patch("backend.researcher.generate")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_research_generate_fails(
        self, mock_exists, mock_makedirs, mock_open, mock_generate
    ):
        # Mocking os.path.exists to return False, so the directory is created
        mock_exists.return_value = False

        # Mocking the generate function to raise an exception
        mock_generate.side_effect = Exception("Generation error")

        # Call the function and catch the exception
        with self.assertRaises(Exception) as context:
            research(
                model_name="Max",
                prospect_name="John Smith",
                company_name="Gamma Corp",
                additional_information="",
                additional_context="",
                temperature=1,
                streaming=False,
            )

        # Assertions

        # Ensure that the correct exception was raised
        self.assertTrue("Generation error" in str(context.exception))

    @patch("backend.researcher.generate")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_research_empty_prospect_and_company(
        self, mock_exists, mock_makedirs, mock_open, mock_generate
    ):
        # Mocking os.path.exists to return True, so no directory is created
        mock_exists.return_value = True

        # Mocking the generate function to return a specific response
        mock_generate.return_value = (
            "# Research Report\nThis is a mock research report."
        )

        # Call the function
        response = research(
            model_name="Max",
            prospect_name="",
            company_name="",
            additional_information="",
            additional_context="",
            temperature=0.7,
            streaming=False,
        )

        # Assertions

        # Check if generate was called with empty prospect and company name
        mock_generate.assert_called_once()
        prompt_argument = mock_generate.call_args[0][1]
        self.assertIn("Prospect name: ", prompt_argument)
        self.assertIn("Company name: ", prompt_argument)

        # Check if the response is written to the file
        mock_open.assert_called_once_with("./logs/research_report.md", "w")
        mock_open().write.assert_called_once_with(
            "# Research Report\nThis is a mock research report."
        )

        # Check if the response returned is the one from the generate function
        self.assertEqual(response, "# Research Report\nThis is a mock research report.")


if __name__ == "__main__":
    unittest.main()
