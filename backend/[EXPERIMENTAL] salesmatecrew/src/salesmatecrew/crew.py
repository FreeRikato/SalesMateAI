from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from salesmatecrew.tools.researcher import SearchAndContents, FindSimilar, GetContents
from langchain_groq import ChatGroq
from datetime import datetime


@CrewBase
class SalesmatecrewCrew:
    """Salesmatecrew crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def llm(self):
        llm = ChatGroq(model="mixtral-8x7b-32768")
        return llm

    @agent
    def prospect_research_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["prospect_research_specialist"],
            tools=[
                SearchAndContents(),
                FindSimilar(),
                GetContents(),
            ],  # Example of custom tool, loaded on the beginning of file
            verbose=True,
            llm=self.llm(),
            max_iter=2,
        )

    @agent
    def email_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["email_generator"],
            tools=[SearchAndContents(), FindSimilar(), GetContents()],
            verbose=True,
            llm=self.llm(),
            max_iter=3,
        )

    @agent
    def email_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["email_reviewer"],
            verbose=True,
            llm=self.llm(),
            max_iter=3,
            allow_delegation=False,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            agent=self.prospect_research_specialist(),
            output_file="research_task.md",
        )

    @task
    def write_email_task(self) -> Task:
        return Task(
            config=self.tasks_config["write_email_task"],
            agent=self.email_generator(),
            output_file="write_task.md", 
        )

    @task
    def review_email_task(self) -> Task:
        return Task(
            config=self.tasks_config["review_email_task"],
            agent=self.email_reviewer(),
            output_file="report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Salesmatecrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            max_rpm=29,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
