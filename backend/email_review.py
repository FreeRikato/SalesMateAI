from utils import generate, pdf2md
import os


# Research function
def review(
    model_name="Max",
    draft_email="",
    email_template="",
    additional_context="Proceed with system message",
    temperature=1,
    streaming=False,
):

    review_prompt = f"""
    <ROLE>
       You are a quality control specialist with years of experience reviewing and optimizing sales emails. Your keen eye for detail ensures that emails are not only grammatically perfect but also effectively convey value and resonate with the prospect. You compare the generated emails against winning templates, ensuring they are personalized, well-structured, and persuasive. You know how to refine an email to increase the chances of a successful response without changing the core message.
    </ROLE>
    <EXAMPLE>
        {email_template}
    </EXAMPLE>
    <TASK> 
        Review and optimize the sales email generated for a prospect by comparing it with a winning email template.
        You must ensure that the generated email adheres to best practices in sales outreach, is personalized, and is optimized for engagement.
        
        drafted email: {draft_email}
        email template or winning email: {email_template}
        
        Update the your contact present with the contact information present in the end of the email template or winning email and Use the email template as reference for you to optimize and don't use its content since it is just a template but use its tone and structure. Also, don't leave any placeholders. 
    </TASK>
    <RULES>
        - THIS IS THE FINAL EMAIL SO DON'T LEAVE ANY REMARKS OR FEEDBACK AT THE START OR END, PLACEHOLDERS OR ANYTHING SINCE THIS HAS TO BE SENT TO THE PROSPECT 
        - MAKE SURE THE CONTACT INFORMATION (MAIL SENDER NAME, COMPANY AND ANYTHING ELSE) IS STRICTLY EXTRACTED FROM THE EXAMPLE EMAIL TEMPLATE AND DON'T ASSUME ANYTHING WHICH IS MOSTLY PRESENT IN THE END
    </RULES> 
    """

    response = generate(
        model_name, review_prompt, additional_context, temperature, streaming
    )
    # Define the folder and file paths
    log_folder = "./logs"
    file_path = os.path.join(log_folder, "final_email.txt")

    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Save the response to the file
    with open(file_path, "w") as file:
        file.write(response)

    return response


file_path = "./logs/draft_email.txt"
email_template_file_path_text = "../data/email_templates.txt"
email_template_file_path_pdf = "../data/email_templates.pdf"

email_template = ""

if email_template_file_path_text.lower():
    email_template_file_path = email_template_file_path_text
    with open(email_template_file_path, "r") as file:
        email_template = file.read()
elif email_template_file_path_pdf.lower():
    email_template_file_path = email_template_file_path_pdf
    email_template = pdf2md(email_template_file_path)
else:
    print("No such file exists")


with open(file_path, "r") as file:
    draft_email = file.read()
review(draft_email, email_template)
