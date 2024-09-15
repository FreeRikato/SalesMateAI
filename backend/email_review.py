from utils import generate, pdf2md
import os


# Research function
def review(
    draft_email="",
    email_template="",
    additional_context="",
    temperature=1,
    streaming=False,
):

    review_prompt = f"""
    <ROLE>
       You are a quality control specialist with years of experience reviewing and optimizing sales emails. Your keen eye for detail ensures that emails are not only grammatically perfect but also effectively convey value and resonate with the prospect. You compare the generated emails against winning templates, ensuring they are personalized, well-structured, and persuasive. You know how to refine an email to increase the chances of a successful response without changing the core message.
    </ROLE>
    <TASK> 
        Review and optimize the sales email generated for a prospect by comparing it with a winning email template.
        You must ensure that the generated email adheres to best practices in sales outreach, is personalized, and is optimized for engagement.
        
        drafted email: {draft_email}
        email template or winning email: {email_template}
        
        Update the Sender name and Sender company with the help of {email_template} and Use the email template as reference for you to optimize and don't use its content since it is just a template but use its tone and structure. Also, don't leave any placeholders. 
    </TASK>
    <RULES>
        THIS IS THE FINAL EMAIL SO DON'T LEAVE ANY REMARKS, PLACEHOLDERS OR ANYTHING SINCE THIS HAS TO BE SENT TO THE PROSPECT
    </RULES> 
    """

    response = generate(
        "Max", review_prompt, additional_context, temperature, streaming
    )
    # Define the folder and file paths
    log_folder = "./logs"
    file_path = os.path.join(log_folder, "final_email.txt")

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Save the response to the file
    with open(file_path, "w") as file:
        file.write(response)


file_path = "./logs/draft_email.txt"
email_template_file_path = "../data/email_templates"

email_template = ""

if email_template_file_path.lower().endswith(".txt"):
    email_template_file_path += ".txt"
    with open(email_template_file_path, "r") as file:
        email_template = file.read()
elif email_template_file_path.lower().endswith(".pdf"):
    email_template_file_path += ".pdf"
    email_template = pdf2md(product_catalog_file_path)

with open(file_path, "r") as file:
    draft_email = file.read()

review(draft_email, email_template)
