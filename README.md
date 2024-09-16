# AI-Powered Sales Development Representative (SDR) Email Outreach System
## Objectives
Develop an AI-driven system that automates and enhances the email outreach process for Sales Development Representatives (SDRs). The system should focus on researching prospects, generating personalized emails, and ensuring adherence to best practices.

## Usage
In order to reproduce the output shown in the demonstration, unzip the file into a directory. 
Create a python virtual environment with:

```bash
python -m venv .venv
source .venv/bin/activate
```

Now, install the python dependencies using `pip`

```bash
pip install -r requirements.txt
```

Get the API keys from providers: Groq (Max), Perplexity (Ava) and Anthropic (Claude-3.5 sonnet). Store it in the .env.example and rename the file into `.env`

```bash
export GROQ_API_KEY = ...
export PERPLEXITY_API_KEY = ...
export ANTHROPIC_API_KEY = ...
```

Create two terminal instances and run the below two commands seperately

Terminal 1:
```bash
cd <project_folder>
cd frontend
streamlit run Home.py
```

Terminal 2:
```bash
cd <project_folder>
cd backend
uvicorn main:app --reload
```
Congragulations!!!
Now, you can run the AI-powered Saled Development Representative (SDR) Email outreach system
