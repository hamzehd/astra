import os
from openai import OpenAI
from django.conf import settings

client = OpenAI(
    api_key=settings.OPENAI_API_KEY,  # This is the default and can be omitted
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-4o",
)