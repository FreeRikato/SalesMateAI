from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import Response
from research import research
from email_generation import write
from email_review import review
from email_sender import send_email
from utils import pdf2md
import os
import json  # Import the json module

app = FastAPI()

# Constants for file paths
LOGS_DIR = "./logs"
PRODUCT_CATALOG_PATH = "../data/product_catalog"
EMAIL_TEMPLATE_TEXT_PATH = "../data/email_templates.txt"
EMAIL_TEMPLATE_PDF_PATH = "../data/email_templates.pdf"
LOCAL_DB_PATH = "local_db.json"  # Path for the local database file


# Payload models
class ResearchPayload(BaseModel):
    model: str
    prospect_name: str
    company_name: str
    additional_information: str
    additional_context: str
    temperature: float
    streaming: bool


class EmailGenerationPayload(BaseModel):
    model: str
    additional_context: str
    temperature: float
    streaming: bool


class EmailReviewPayload(BaseModel):
    model: str
    additional_context: str
    temperature: float
    streaming: bool


class EmailSendPayload(BaseModel):
    to_email: str
    subject: str
    gmail_user: str
    app_password: str


# Utility function to read file content
def read_file(file_path: str) -> str:
    """Read content from a file."""
    with open(file_path, "r") as file:
        return file.read()


def load_product_catalog(file_path: str) -> str:
    """Load product catalog from a txt or pdf file."""
    if file_path.endswith(".txt"):
        return read_file(file_path)
    elif file_path.endswith(".pdf"):
        return pdf2md(file_path)
    return ""


# New utility functions for the local database
def load_db():
    """Load the local database from a JSON file."""
    if os.path.exists(LOCAL_DB_PATH):
        with open(LOCAL_DB_PATH, "r") as f:
            return json.load(f)
    else:
        return {}


def save_db(data):
    """Save data to the local database JSON file."""
    with open(LOCAL_DB_PATH, "w") as f:
        json.dump(data, f, indent=4)


# Endpoints
@app.post("/research-analysis")
def research_analysis(payload: ResearchPayload):
    """
    Perform research analysis based on the provided model and details.
    """
    markdown_response = research(
        payload.model,
        prospect_name=payload.prospect_name,
        company_name=payload.company_name,
        additional_information=payload.additional_information,
        additional_context=payload.additional_context,
        temperature=payload.temperature,
        streaming=payload.streaming,
    )

    # Load the current database
    db = load_db()

    # Prepare the data to be stored
    prospect_data = {
        "prospect_name": payload.prospect_name,
        "company_name": payload.company_name,
        "research_analysis_response": markdown_response,
    }

    # Append the new data to the 'research_analysis' list in the database
    if "research_analysis" not in db:
        db["research_analysis"] = []

    db["research_analysis"].append(prospect_data)

    # Save the updated database
    save_db(db)

    return Response(content=markdown_response, media_type="text/markdown")


@app.post("/generate-email")
async def generate_email(payload: EmailGenerationPayload):
    """
    Generate an email based on the research report and product catalog.
    """
    research_report = read_file(os.path.join(LOGS_DIR, "research_report.md"))
    product_catalog = load_product_catalog(PRODUCT_CATALOG_PATH)

    markdown_response = write(
        payload.model,
        research_report=research_report,
        product_catalog=product_catalog,
        additional_context=payload.additional_context,
        temperature=payload.temperature,
        streaming=payload.streaming,
    )
    return Response(content=markdown_response, media_type="text/markdown")


@app.post("/review-email")
async def review_email(payload: EmailReviewPayload):
    """
    Review a draft email using the provided email templates.
    """
    draft_email = read_file(os.path.join(LOGS_DIR, "draft_email.txt"))

    if os.path.exists(EMAIL_TEMPLATE_TEXT_PATH):
        email_template = read_file(EMAIL_TEMPLATE_TEXT_PATH)
    else:
        email_template = pdf2md(EMAIL_TEMPLATE_PDF_PATH)

    markdown_response = review(
        payload.model,
        draft_email=draft_email,
        email_template=email_template,
        additional_context=payload.additional_context,
        temperature=payload.temperature,
        streaming=payload.streaming,
    )
    return Response(content=markdown_response, media_type="text/plain")


@app.post("/send-email")
async def email_send(payload: EmailSendPayload):
    """
    Send an email using the provided SMTP credentials and email content.
    """
    email_body = read_file(os.path.join(LOGS_DIR, "final_email.txt"))

    send_email(
        to_email=payload.to_email,
        subject=payload.subject,
        body_text=email_body,
        gmail_user=payload.gmail_user,
        app_password=payload.app_password,
    )

    # Load the current database
    db = load_db()

    # Prepare the data to be stored
    email_data = {
        "prospect_email": payload.to_email,
        "subject": payload.subject,
        "text_body": email_body,
    }

    # Append the new data to the 'sent_emails' list in the database
    if "sent_emails" not in db:
        db["sent_emails"] = []

    db["sent_emails"].append(email_data)

    # Save the updated database
    save_db(db)

    return {"progress": "Mail Sent Successfully"}
