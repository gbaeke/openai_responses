from openai import OpenAI
import os
import json
# get env variable
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-4o",
    tools=[{
        "type": "web_search_preview",
        "user_location": {
            "type": "approximate",
            "country": "BE",
            "city": "Hamme",
            "region": "East Flanders",
        }
    }],
    input="Recent AI news?"
)

# Get the response data as a dictionary
response_data = response.to_dict()

# Print with indent
# print(json.dumps(response_data, indent=4))


# Import rich console
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.text import Text

# Initialize console
console = Console()

# Extract annotations from the response data
annotations = []
for output_item in response_data.get('output', []):
    if output_item.get('type') == 'message':
        for content_item in output_item.get('content', []):
            if content_item.get('type') == 'output_text':
                annotations.extend(content_item.get('annotations', []))

# Print a header
console.print("\n[bold cyan]Web Search Results[/bold cyan]\n")

# Print each annotation in a separate panel
for i, annotation in enumerate(annotations, 1):
    if annotation.get('type') == 'url_citation':
        title = annotation.get('title', 'No title')
        url = annotation.get('url', 'No URL')
        
        # Create formatted text for the panel content
        content = Text()
        content.append("Title: ", style="bold yellow")
        content.append(f"{title}\n\n", style="cyan")
        content.append("URL: ", style="bold yellow")
        content.append(url, style="green")
        
        # Create and print the panel
        panel = Panel(
            content,
            title=f"Result {i}",
            border_style="blue",
            box=box.ROUNDED
        )
        console.print(panel)
        console.print("")  # Add a blank line between panels


