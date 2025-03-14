from openai import OpenAI
import os
import json
from pydantic import BaseModel
from typing import List

# get env variable
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# recommendation to use this over json mode
response = client.responses.create(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."}
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "calendar_event",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string"
                    },
                    "date": {
                        "type": "string"
                    },
                    "participants": {
                        "type": "array", 
                        "items": {
                            "type": "string"
                        }
                    },
                },
                "required": ["name", "date", "participants"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
)

event = json.loads(response.output_text)

# print event with indent
print(json.dumps(event, indent=4))

# create a Pydantic model
class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: List[str]

# to use a Pydantic model, use the parse method
response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."}
    ],
    text_format=CalendarEvent
)

event = json.loads(response.output_text)

# print event with indent
print(json.dumps(event, indent=4))