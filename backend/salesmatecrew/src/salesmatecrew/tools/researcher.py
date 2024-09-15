from crewai_tools import BaseTool
from exa_py import Exa
import os


class SearchAndContents(BaseTool):
    name: str = "Search and Contents Tool"
    description: str = (
        "Searches the web based on a search query for the latest results. Uses the Exa API. This also returns the contents of the search results."
    )

    def _run(self, search_query: str) -> str:

        exa = Exa(api_key=os.getenv("EXA_API_KEY"))
        search_results = exa.search_and_contents(
            query=search_query,
            use_autoprompt=True,
            text={"include_html_tags": False, "max_characters": 8000},
        )

        return search_results


class FindSimilar(BaseTool):
    name: str = "Find Similar Tool"
    description: str = (
        "Searches for similar websites to a given website using the Exa API. Takes in a URL of the website"
    )

    def _run(self, website_url: str) -> str:

        exa = Exa(api_key=os.getenv("EXA_API_KEY"))

        search_results = exa.find_similar(
            url=website_url
        )

        return search_results


class GetContents(BaseTool):
    name: str = "Get Contents Tool"
    description: str = "Gets the contents of a specific website using the Exa API. Takes in the ID of the website in a list, like this: ['https://www.cnbc.com/2024/04/18/my-news-story']."
    
    def _run(self, website_ids: str) -> str:

        exa = Exa(api_key=os.getenv("EXA_API_KEY"))

        contents = exa.get_contents(website_ids)
        return contents
      
