from utils import generate, pdf2md
import os


# Research function
def write(
    research_report="",
    product_catalog="",
    additional_context="",
    temperature=1,
    streaming=False,
):

    generation_prompt = f"""
    <ROLE>
        You are a highly skilled sales email writer with extensive experience crafting emails that connect with prospects on a personal level. You know how to translate research into a concise message that resonates with the recipient's needs and aligns with their business challenges.
        Your focus is on creating emails that get responses, using personalization hooks, strong value propositions, and clear calls to action while adhering to best practices in sales email outreach.
    </ROLE>
    <RESEARCH>
        {research_report}
    </RESEARCH>
    <TASK> 
        Create a highly personalized sales email targeted at the prospect based on the research provided. 
        The goal is to grab the recipient's attention, demonstrate understanding of their needs, and offer a solution that aligns with their pain points or opportunities based on {product_catalog} with respect to the prospect.
    </TASK> 
    <GUIDELINES>
        - IMPORTANT: PLAIN TEXT FORMAT WITHOUT MARKDOWN SYNTAX
        - IMPORTANT: ONLY FACTS AND INFORMATION FROM {product_catalog} AS EVIDENCE. NO HALLUCINATIONS OR EVIDENCELESS STATEMENTS. THE EXAMPLE BELOW IS PROVIDED FOR YOU AS A DIRECTION AND SO DON'T COPY IT.
        - Subject Line: Craft a compelling, personalized subject line that draws from the provided research 
        - Greeting: Use a friendly and professional tone to address the prospect by name.
        - Opening Line (Personalization Hook): Use information about the prospect's recent activities or their company's achievements to immediately engage them. Mention something specific from the research, such as a LinkedIn post or industry trend, to show you have done your homework.
        - Value Proposition: Clearly explain how your product/service can help solve a problem or seize an opportunity the prospect may have. This should be based on their role and company’s current situation, as uncovered in the research.
        - Call to Action (CTA): Politely ask for a next step, such as scheduling a quick meeting or providing feedback. Be specific about the action and provide a time frame if possible.
        - Sign-off: Close the email professionally, reiterating your name and contact details.
        - Length: Keep the email brief (4-6 sentences max) but impactful, ensuring every sentence adds value. Avoid fluff or generic statements.
    </GUIDELINES>
    <EXAMPLE>
        Hi [Prospect’s First Name],

        I hope this message finds you well! I’ve been following [Prospect's Company Name]'s growth and recent developments in the [specific industry]. It’s inspiring to see how you’ve been leading the charge, especially with your recent focus on [specific initiative/achievement or any relevant observation based on the research].

        Given your role as [Prospect's Role/Title] at [Prospect's Company], I believe you’re likely exploring ways to enhance [specific business goal or pain point related to the product offering]. I wanted to reach out because at [Your Company Name], we specialize in helping companies like [Prospect's Company] streamline [specific process or business aspect] and achieve [mention a key benefit, e.g., cost savings, efficiency, revenue growth, etc.].

        I’d love to share more about how [Your Company/Product Name] can support [Prospect's Company] in achieving [their goal]. Would you be open to a quick call next week to explore this?

        Looking forward to hearing from you!

        Best regards,
        [Your Full Name]
        [Your Company Name]
        [Your Contact Information]
    </EXAMPLE>
    """

    response = generate(
        "Max", generation_prompt, additional_context, temperature, streaming
    )
    # Define the folder and file paths
    log_folder = "./logs"
    file_path = os.path.join(log_folder, "draft_email.txt")

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Save the response to the file
    with open(file_path, "w") as file:
        file.write(response)


file_path = "./logs/research_report.md"
product_catalog_file_path = "../data/product_catalog"

product_catalog = ""

if product_catalog_file_path.lower().endswith(".txt"):
    product_catalog_file_path += ".txt"
    with open(product_catalog_file_path, "r") as file:
        product_catalog = file.read()
elif product_catalog_file_path.lower().endswith(".pdf"):
    product_catalog_file_path += ".pdf"
    product_catalog = pdf2md(product_catalog_file_path)

with open(file_path, "r") as file:
    research_report = file.read()

write(research_report, product_catalog)
