from openai import OpenAI
import os
import json
# get env variable
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


# no need for a messages array and new instructions option
response = client.responses.create(
    model="gpt-4o",
    instructions="Talk like you are drunk",
    input="Write a one-sentence bedtime story about a unicorn."
)

# simpler way to get the output text
print(response.output_text)

# Print only the JSON-serializable parts of the response
print(json.dumps(response.to_dict(), indent=4))

# you can still use the old messages array
# there's also a role called "developer" to steer the model in a specific direction
# system messages are also supported and take precedence
response = client.responses.create(
    model="gpt-4o",
    input=[
        {
            "role": "developer",
            "content": "Talk like a pirate."
        },
        {
            "role": "user",
            "content": "Are semicolons optional in JavaScript?"
        }
    ]
)

print(response.output_text)

response = client.responses.create(
    model="gpt-4o",
    input="My name is Geert"
)

print(response.output_text)

# ask for the name that was just mentioned
second_response = client.responses.create(
    model="gpt-4o",
    input="What is my name based on what I just told you?",
    previous_response_id=response.id
)

print(second_response.output_text)