import os
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig
from dotenv import load_dotenv
load_dotenv()
API_KEY_EMBEDDING = os.getenv("API_KEY_EMBEDDING")
API_KEY = os.getenv("API_KEY")

client = genai.Client(api_key=API_KEY_EMBEDDING)

classic = genai.Client(api_key=API_KEY)

async def get_embedding(chunk: str):
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=chunk,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT", output_dimensionality=768)
    )
    vector = response.embeddings[0].values
    return vector

async def generate_answer(text: str):
    interaction = classic.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=text,
        config=types.GenerateContentConfig(
            temperature=0.0
        )
    )
    return interaction.text