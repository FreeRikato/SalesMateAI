#!/usr/bin/env python
import sys
from salesmatecrew.crew import SalesmatecrewCrew

import os


def load_text_template():
    file_path = os.path.join(os.path.dirname(__file__), "config", "email_template.txt")
    with open(file_path, "r") as file:
        text_template = file.read()
    return text_template


def run():
    """
    Run the crew.
    """
    inputs = {
        "prospect_name": "Mike Mayes",
        "company_name": "Salesforce",
        "additional_information": "Mike Mayes is the Senior Vice President of Sales at Salesforce. He has been with the company for over 10 years and has extensive experience in enterprise software sales.",
        "email_template": load_text_template(),
        "company_catalog": """
        SalesIntel is a sales lead database with over 16 million companies and 275 million lead profiles. It assists sales teams in gaining insight into target prospects and reaching out to them. Key features include:
            Technographic data: Insights into the technology stack used by prospects
            Lead scoring: Prioritize leads based on engagement and fit
            CRM integration: Direct data export to CRM systems
            Buying intent insights: Identify prospects ready to purchase

        SalesIntel offers custom pricing based on the client's needs
        """,
    }
    SalesmatecrewCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        SalesmatecrewCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SalesmatecrewCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {"topic": "AI LLMs"}
    try:
        SalesmatecrewCrew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
