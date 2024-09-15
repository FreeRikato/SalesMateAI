import os
from dotenv import load_dotenv
from crewai import Crew
from tasks import SalesMateTasks
from agents import SalesCrew
from textwrap import dedent


def main():
    load_dotenv()

    prospect_name = "David Brown"

    company_name = "Amazon Web Services (AWS)"
    prospect_additional_information = "David is the Director of Cloud Solutions at AWS. He has been working there for over 8 years and is responsible for cloud infrastructure strategy and partner ecosystem."

    product_catalog = "HubSpot offers a full suite of CRM software, including marketing automation, sales enablement tools, and customer service management. The CRM is designed for businesses to better manage customer relationships, improve sales pipelines, and enhance marketing efforts through automation and AI-driven insights. HubSpot’s CRM integrates with multiple cloud providers, including AWS, to streamline sales and marketing processes for teams. The AI-powered automation can help AWS scale customer interactions and better track enterprise sales leads."

    sales_email_template = dedent(
        """
        [TITLE]
        [SUBJECT]
        Hi [First Name],

        I hope this message finds you well. I'm reaching out because I noticed [Prospect Company] is expanding in [Relevant Industry]. HubSpot's CRM platform can support this growth by offering real-time insights, AI-driven customer segmentation, and sales automation. Our platform helps companies like [Competitor Company] achieve seamless scaling of their customer engagement efforts.

        Let's set up a time to discuss how we can support your goals with our proven CRM technology.

        Best regards,
        [Your Name]
        [Your Title]
        """
    )

    tasks = SalesMateTasks()
    agents = SalesCrew()

    research_agent = agents.researcher()
    writer_agent = agents.writer()
    reviewer_agent = agents.reviewer()

    research_task = tasks.research_task(
        research_agent, prospect_name, company_name, prospect_additional_information
    )
    write_task = tasks.write_email_task(writer_agent, product_catalog)
    review_task = tasks.review_email_task(reviewer_agent, sales_email_template)

    crew = Crew(
        agents=[research_agent, writer_agent, reviewer_agent],
        tasks=[research_task, write_task, review_task],
        max_rpm=29,
    )

    result = crew.kickoff()
    print(result)


if __name__ == "__main__":
    main()
