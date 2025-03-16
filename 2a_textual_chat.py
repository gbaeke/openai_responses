from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer, Container
from textual.widgets import Header, Footer, Input, Static
from textual.binding import Binding
from openai import OpenAI
import os
import json
from rich.text import Text
import asyncio

class Message(Static):
    """A custom widget for displaying chat messages."""
    def __init__(self, sender: str, message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sender = sender
        self.message = message
        sender_style = "bold blue" if self.sender == "You" else "bold magenta"
        self.update(Text.from_markup(f"[{sender_style}]{self.sender}:[/{sender_style}] {self.message}"))

    def compose(self) -> ComposeResult:
        yield from ()  # Properly return an empty iterator

class TokenUsage(Static):
    """A widget to display token usage statistics."""
    def update_stats(self, input_tokens: int, output_tokens: int, total_tokens: int):
        self.update(f"Tokens - Input: {input_tokens}, Output: {output_tokens}, Total: {total_tokens}")

class ChatApp(App):
    """A Textual app for chatting with OpenAI's GPT models."""
    
    CSS = """
    Screen {
        layout: grid;
        grid-size: 1 3;
        grid-rows: 1fr auto auto;
    }

    #chat-container {
        height: 100%;
        border: solid green;
        background: $surface;
        padding: 1;
    }

    #token-usage {
        height: auto;
        color: $text-muted;
        text-align: center;
        padding: 1;
    }

    Input {
        dock: bottom;
        margin: 1 1;
    }

    Message {
        margin: 0 0;
        height: auto;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", show=True),
        Binding("ctrl+d", "quit", "Quit", show=False),
    ]

    def __init__(self):
        super().__init__()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.previous_response_id = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with ScrollableContainer(id="chat-container"):
            yield Message("System", "Welcome to the OpenAI Chat! Type your message below.")
        yield TokenUsage(id="token-usage")
        yield Input(placeholder="Type your message here... (Press Enter to send)")

    async def on_input_submitted(self, message: Input.Submitted) -> None:
        # Clear the input
        input_widget = self.query_one(Input)
        user_message = message.value
        input_widget.value = ""

        # Add user message to chat
        chat_container = self.query_one("#chat-container")
        await chat_container.mount(Message("You", user_message))
        self.scroll_chat_to_bottom()

        # Create a response from the OpenAI API
        try:
            response = self.client.responses.create(
                model="gpt-4",
                input=user_message,
                previous_response_id=self.previous_response_id,
                stream=True
            )

            # Initialize AI message
            ai_message = Message("AI", "")
            await chat_container.mount(ai_message)
            self.scroll_chat_to_bottom()

            # Collect the full response
            full_response = ""
            for event in response:
                if hasattr(event, "type") and "text.delta" in event.type:
                    full_response += event.delta
                    ai_message.update(Text.from_markup(f"[bold magenta]AI:[/bold magenta] {full_response}"))
                    self.scroll_chat_to_bottom()
                    self.refresh()
                    await asyncio.sleep(0.01)  # Small delay for smooth streaming
                if hasattr(event, "type") and "response.completed" in event.type:
                    response_json = event.to_json()

            # Update token usage
            response_data = json.loads(response_json)
            usage = response_data['response']['usage']
            token_usage = self.query_one(TokenUsage)
            token_usage.update_stats(
                usage['input_tokens'],
                usage['output_tokens'],
                usage['total_tokens']
            )

            # Update previous response ID
            self.previous_response_id = response_data['response']['id']

        except Exception as e:
            await chat_container.mount(Message("System", f"Error: {str(e)}"))
            self.scroll_chat_to_bottom()

    def scroll_chat_to_bottom(self):
        """Scroll the chat container to the bottom."""
        chat_container = self.query_one("#chat-container")
        chat_container.scroll_end(animate=False)

if __name__ == "__main__":
    app = ChatApp()
    app.run() 