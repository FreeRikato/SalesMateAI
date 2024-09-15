from fastapi import FastAPI
from pydantic import BaseModel
from research import research
from email_generation import write
from email_review import review
from email_sender import send_email
from utils import pdf2md

app = FastAPI()


# Define the payload model for validation
class ResearchPayload(BaseModel):
    model: str
    prospect_name: str
    company_name: str
    additional_information: str
    additional_context: str
    temperature: float
    streaming: bool


# Define the endpoint
@app.post("/research-analysis")
async def research_analysis(payload: ResearchPayload):
    # Execute the research function asynchronously
    markdown_response = research(
        payload.model,
        prospect_name=payload.prospect_name,
        company_name=payload.company_name,
        additional_information=payload.additional_information,
        additional_context=payload.additional_context,
        temperature=payload.temperature,
        streaming=payload.streaming,
    )

    # Return the markdown content as a response
    return markdown_response


# Define the payload model for validation
class EmailGenerationPayload(BaseModel):
    model: str
    additional_context: str
    temperature: float
    streaming: bool


# Define the endpoint
@app.post("/generate-email")
async def generate_email(payload: EmailGenerationPayload):
    # Execute the research function asynchronously
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

    markdown_response = write(
        payload.model,
        research_report=research_report,
        product_catalog=product_catalog,
        additional_context=payload.additional_context,
        temperature=payload.temperature,
        streaming=payload.streaming,
    )

    # Return the markdown content as a response
    return markdown_response


class EmailReviewPayload(BaseModel):
    model: str
    additional_context: str
    temperature: float
    streaming: bool


# Define the endpoint
@app.post("/review-email")
async def review_email(payload: EmailReviewPayload):
    # Execute the research function asynchronously
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

    markdown_response = review(
        payload.model,
        draft_email=draft_email,
        email_template=email_template,
        additional_context=payload.additional_context,
        temperature=payload.temperature,
        streaming=payload.streaming,
    )

    # Return the markdown content as a response
    return markdown_response


class EmailSendPayload(BaseModel):
    to_email: str
    subject: str
    gmail_user: str
    app_password: str


# Define the endpoint
@app.post("/send-email")
async def email_send(payload: EmailSendPayload):
    # Execute the research function asynchronously
    with open("../backend/logs/final_email.txt", "r") as file:
        email_body = file.read()
    markdown_response = send_email(
        to_email=payload.to_email,
        subject=payload.subject,
        body_text=email_body,
        gmail_user=payload.gmail_user,
        app_password=payload.app_password,
    )

    # Return the markdown content as a response
    return {"progress": "Mail Sent Successfully"}
