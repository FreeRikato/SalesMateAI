import os
from langchain_groq import ChatGroq
from textwrap import dedent
from crewai import Agent
from tools import ExaSearchTool


class SalesCrew:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"), model="llama-3.1-70b-versatile"
        )
        self.tool_usage_llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama3-groq-70b-8192-tool-use-preview",
        )

    def researcher(self):
        return Agent(
            role="Prospect research specialist",
            goal="Conduct research on a specific prospect to gather information about their company, industry, and potential pain points.",
            tools=ExaSearchTool.tools(),
            backstory=dedent(
                f"""You are an expert prospect researcher, tasked with gathering information about a specific prospect. Your goal is to gather as much information as possible about the prospect's company, industry, and potential pain points."""
            ),
            verbose=True,
            llm=self.tool_usage_llm,
            allow_delegation=False,
            max_iter=3,
        )

    def writer(self):
        return Agent(
            role="Sales email writer",
            goal="Write a personalized sales email to a prospect based on the provided information.",
            tools=[],
            backstory=dedent(
                f"""You are an expert sales email writer, tasked with crafting a personalized sales email to a prospect based on the provided information. Your goal is to create a compelling and persuasive email that highlights the benefits of the company's products or services and encourages the prospect to take action."""
            ),
            verbose=True,
            allow_delegation=False,
            context=[self.researcher],
            llm=self.llm,
            max_iter=3,
        )

    def reviewer(self):
        return Agent(
            role="Sales email reviewer",
            goal="Review a sales email to ensure it is effective and persuasive.",
            tools=[],
            backstory=dedent(
                f"""You are an expert sales email reviewer, tasked with reviewing a sales email to ensure it is effective and persuasive. Your goal is to ensure the email is well-written, persuasive, and tailored to the specific prospect."""
            ),
            verbose=True,
            allow_delegation=False,
            context=[self.writer],
            llm=self.llm,
            max_iter=3,
        )
