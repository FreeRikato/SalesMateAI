from utils import generate
import os


# Research function
def research(
    model_name="Max",
    prospect_name="",
    company_name="",
    additional_information="",
    additional_context="",
    temperature=1,
    streaming=False,
):

    research_prompt = f"""
    <ROLE>
        You are an experienced research expert, specializing in gathering key information on prospects for sales teams. Your deep research skills enable you to extract the most relevant and actionable insights about individuals and companies. 
    </ROLE>
    <TASK> 
        Gather actionable, personalized insights about a potential lead with a focus on identifying Pain Points/Opportunities. Use the following details: 
        Prospect name: {prospect_name} 
        Company name: {company_name}
        Additional information: {additional_information} 
    </TASK> 
    <STEPS> 
        A markdown document for the research report. The report should be elaborate with structured points containing:
        - Company Overview
        - Prospect's Role & Background
        - Personalization Hook
        - Potential Pain Points or Opportunities
        - URL of the website where the information was found
        1. Pain Points/Opportunities: Dive into industry trends and the company's recent developments to identify key challenges or opportunities. 
        2. Company Information: Provide a brief overview of the company, focusing on its industry, key products/services, and any recent news or milestones relevant to identifying pain points or opportunities.
        3. Prospect Background: Summarize the prospect's role and any relevant projects or initiatives, with an emphasis on identifying areas where they may be seeking solutions or facing challenges.
        4. Personalization Hook: Pinpoint any relevant mutual connections, social media activity, or public mentions (like awards, articles, or speaking engagements) that might hint at pain points or opportunities, which can be referenced in your outreach.
    </STEPS>
    <RULES>
        - Only include websites that are especially relevant to {prospect_name} and {company_name}. Do not include any website that are not directly related to {prospect_name} or {company_name}. 
        - Do not include sources that are not authentic. If the content of the page includes a list of websites or looks like the front page of a website, do not include it in the list!
        - Summarize the prospect research in a few sentences. Make the summary as long as necessary to include all the relevant information, but not too long for a research report.
        - Include the URL of the article where you found the information.
        - Include a minimum of 4 websites and a maximum of 10 websites in the list.
    </RULES>
    <EXAMPLE>
        # Company Overview:
        ---
        ## Prospect Research
        - Acme Corp is a global provider of cloud-based software solutions for the e-commerce industry. 
        - Acme recently secured $50 million in Series C funding and expanded its operations to Europe.
        - Their flagship product helps retailers manage online inventory, optimize shipping, and enhance customer experience.
        - Acme's client base includes several Fortune 500 companies, and their software integrates with major e-commerce platforms like Shopify and Magento.
        - The company has seen a 30% year-over-year growth, primarily driven by the increasing demand for streamlined e-commerce operations in the post-pandemic environment.
        ---
        ## Prospect’s Role & Background:
        - John Smith is the VP of Operations at Acme Corp.
        - He has over 15 years of experience in supply chain management and e-commerce operations.
        - John has been with Acme for 5 years and has led several initiatives to improve logistical efficiency and customer satisfaction.
        - Prior to joining Acme, John worked at Global Shipping Inc., where he played a pivotal role in modernizing their supply chain systems.
        - He holds a Master’s degree in Business Administration with a focus on Operations from Stanford University.
        - John is known for his hands-on leadership style and has been recognized for his innovative approach to solving complex supply chain challenges.
        ---
        ## Personalization Hook:
        - John’s recent speaking engagement at the logistics conference is a great entry point for outreach.
        - He shared key insights into the future of supply chain automation, which can serve as a conversation starter.
        - Acknowledging his expertise in optimizing supply chains and referencing his leadership in Acme’s European expansion adds credibility to the outreach.
        - Highlighting the synergy between Acme’s goals and your solutions could demonstrate a shared vision, especially around automating logistics and improving customer experience.
        ---
        ## Potential Pain Points or Opportunities:
        - There may also be challenges in scaling their current infrastructure to support global operations.
        - With Acme's expansion into Europe, they are likely facing new supply chain complexities due to differing regulations, shipping logistics, and market demands.
        - The European market presents unique challenges such as navigating tariffs, local customer preferences, and complex last-mile delivery issues, which could strain Acme’s current logistical setup.
        - Acme may be looking for advanced data analytics tools to predict and manage supply chain disruptions, ensuring smooth operations across continents.
        - Offering solutions to streamline cross-border logistics or optimize customer delivery timelines can be of interest.
        - Additionally, with Acme’s aggressive growth, they might be exploring opportunities to integrate AI-driven tools to further enhance operational efficiency.
        ---
        ## Sources:
        - [Acme corp trade publication](https://www.Acmeblogs/articles/12325)
        - [John Smith logistics conference](https://www.logistics_with_john_smith/articles/1243)
        - [Acme Series C funding news](https://www.financialnews.com/acme_series_c_expansion)
        - [E-commerce growth trends post-pandemic](https://www.ecommerceinsights.com/articles/post-pandemic_growth_trends)
    </EXAMPLE>
    """

    response = generate(
        model_name, research_prompt, additional_context, temperature, streaming
    )

    # Define the folder and file paths
    log_folder = "./logs"
    file_path = os.path.join(log_folder, "research_report.md")

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Save the response to the file
    with open(file_path, "w") as file:
        file.write(response)

    return response
