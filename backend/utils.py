import os
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatPerplexity
from langchain_core.prompts import ChatPromptTemplate
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from dotenv import load_dotenv

load_dotenv()


def pdf2md(path):
    parser = LlamaParse(
        result_type="markdown", verbose=False
    )  # "markdown" and "text" are available
    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(
        input_files=[path], file_extractor=file_extractor
    ).load_data()
    return documents[0].text


def generate(
    model_name="Max",
    system_message="Give a short funny intro of yourself",
    context="Hi there! Introduce yourself",
    temperature=1,
    streaming=False,
):

    groq_key = os.getenv("GROQ_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    perplexity_key = os.getenv("PERPLEXITY_API_KEY")
    response_content = "No response"

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "{system_message}",
            ),
            ("human", "{context}"),
        ]
    )

    if model_name == "Max":

        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=temperature,
            streaming=streaming,
            api_key=groq_key,
        )
        chain = prompt | llm  # LCEL - Langchain Express Language
        response = chain.invoke(
            {
                "system_message": system_message,
                "context": context,
            }
        )
        response_content = response.content

    elif model_name == "Ava":

        llm = ChatPerplexity(
            pplx_api_key=perplexity_key,
            model="llama-3.1-sonar-small-128k-online",
            max_tokens=256,
            temperature=temperature,
            streaming=streaming,
            api_key=perplexity_key,
        )
        chain = prompt | llm
        response = chain.invoke(
            {
                "system_message": system_message,
                "context": context,
            }
        )
        response_content = response.content

    elif model_name == "Sophia":

        llm = ChatAnthropic(
            model="claude-3-haiku-20240307",
            temperature=temperature,
            max_tokens=1024,
            streaming=streaming,
            api_key=anthropic_key,
        )
        chain = prompt | llm
        response = chain.invoke(
            {
                "system_message": system_message,
                "context": context,
            }
        )
        response_content = response.content

    return response_content
