import json
import os
import openai
from django.conf import settings


class OpenAIClient:
    _instance = None
    api_key = settings.OPENAI_API_KEY

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        if not self.api_key:
            raise ValueError("OpenAI API Key is not set in Django settings.")
        openai.api_key = self.api_key
        self.api_key
        self.client = openai

    def get_client(self):
        return self.client
    
def analyze_song_lyrics(lyrics: str):
    """
    Summarizes song lyrics and extracts mentioned countries.

    Args:
        lyrics (str): The song lyrics to analyze.

    Returns:
        dict: A JSON response containing the summary and list of countries mentioned.
    """
    prompt = (
        "You are a helpful assistant. Analyze the following song lyrics, summarize their content, "
        "and provide a list of countries mentioned in the text.\n\n"
        "Lyrics:\n" + lyrics + "\n\n"
        "Respond in the following JSON format:\n"
        "{\n"
        "  \"summary\": \"<summary of the song>\",\n"
        "  \"countries\": [\"<list of countries mentioned>\"]\n"
        "}"
    )

    try:
        # Get the OpenAI client
        client = OpenAIClient().get_client()

        # Call the ChatCompletion API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        # Extract the message content from the response
        summarized_content = response.choices[0].message.content
        # Convert the JSON response to Python JSON
        jsoned_lyrics_response =  json.loads(summarized_content)
        jsoned_lyrics_response['request_id'] = response.id

        return jsoned_lyrics_response
    except Exception as e:
        return {"error": str(e)}