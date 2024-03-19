import os
from openai import AzureOpenAI
from fastapi import FastAPI
from pydantic import BaseModel
import json

description = """
An API to wrap elements of Azure OpenAI to enable standarisation of medicine data for Mid Yorks NHS Trust.
"""

app = FastAPI(
    title="Police Scotland AI Hack Example",
    description=description,
    summary="Wrapping Azure OpenAI to demonstrate a simple API",
    version="0.0.2",
    contact={
        "name": "Hippo Data",
        "url": "https://hippodigital.co.uk/data/",
        "email": "ed.thewlis@hippodigital.co.uk",
    },
    swagger_ui_parameters={"syntaxHighlight.theme": "nord", "showExtensions": True, "theme": "flattop"})
    
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

SYSTEM_MESSAGE_GPT35 = """

- Act as a professional assistant to a police officer. 
- Your responses should be based on verifiable facts and should be consistent over time.
- When summarising information, respond with the most relevant and important information.
- Where you have interpreted information, make it clear that this is your interpretation.
- Summarise the incident log provided, using bullet points to highlight the most important information.

"""

SYSTEM_MESSAGE_GPT4 = """

- Act as a professional assistant to a police officer. 
- Your responses should be based on verifiable facts and should be consistent over time.
- When summarising information, respond with the most relevant and important information.
- Where you have interpreted information, make it clear that this is your interpretation.
- When summarising information, respond with a valid JSON message.

"""

class IncidentLog(BaseModel):
    full_text: str


@app.post("/gpt-4-json", description="GPT4 Model returning JSON.",)
def get_gpt4_json(prompt: str):
 
    completion = client.chat.completions.create(
        model="gpt-4-auto", # This must match the custom deployment name you chose for your model.
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGE_GPT4},
            {"role":"user", "content": prompt }
        ],
        response_format={ "type": "json_object" },
        temperature=0.2
    )

    response = json.loads(completion.choices[0].message.content)
   
    return response


@app.post("/gpt-3-response",description="GP35-Turbo text response",)

def gpt3_response(prompt: IncidentLog):

    completion = client.chat.completions.create(
        model="gpt-35-turbo", # This must match the custom deployment name you chose for your model.
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGE_GPT35},
            {"role": "user", "content": prompt.full_text }
        ],
        temperature=0.2
    )
    response = completion.choices
    
    return response






