from openai import OpenAI
import os
import json
from rich.console import Console
from rich.spinner import Spinner

# get env variable
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

prompt = """
Write a bash script that takes a matrix represented as a string with 
format '[1,2],[3,4],[5,6]' and prints the transpose in the same format.
"""

console = Console()
with console.status("[bold green]Waiting for OpenAI response...", spinner="dots"):
    response = client.responses.create(
        model="o3-mini",
        reasoning={"effort": "medium"},
        input=[
            {
                "role": "user", 
                "content": prompt
            }
        ]
    )

print(response.output_text)