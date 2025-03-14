from openai import OpenAI
import os
from rich.console import Console
from rich.prompt import Prompt
import json

# Get the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Initialize the rich console
console = Console()

# Start the chat loop
previous_response_id = None
console.print("[bold green]Welcome to the OpenAI Chat![/bold green]")

while True:
    # Get user input
    user_input = Prompt.ask("[bold blue]You[/bold blue]")
    
    # Exit the chat if the user types 'exit'
    if user_input.lower() == 'exit':
        console.print("[bold red]Goodbye![/bold red]")
        break
    
    # Create a response from the OpenAI API
    response = client.responses.create(
        model="gpt-4o",
        input=user_input,
        previous_response_id=previous_response_id,
        stream=True
    )

    # Print the response
    console.print(f"[bold magenta]AI:[/bold magenta] ", end="")

    # Print the chunks
    for event in response:
        if hasattr(event, "type") and "text.delta" in event.type:
            console.print(event.delta, end="")
        if hasattr(event, "type") and "response.completed" in event.type:
            response_json = event.to_json()    
    
    
    # Display token usage
    response_data = json.loads(response_json)
    input_tokens = response_data['response']['usage']['input_tokens']
    output_tokens = response_data['response']['usage']['output_tokens']
    total_tokens = response_data['response']['usage']['total_tokens']
    console.print(f"\n[dim]Tokens - Input: {input_tokens}, Output: {output_tokens}, Total: {total_tokens}[/dim]\n")
    
    # Update the previous response ID
    previous_response_id = response_data['response']['id'] 