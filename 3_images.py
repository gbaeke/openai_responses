from openai import OpenAI
import os

# get env variable
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# Example of analyzing an image using the OpenAI API
# You can add multiple images to the input array
image_analysis_response = client.responses.create(
    model="gpt-4o-mini",
    input=[{
        "role": "user",
        "content": [
            {"type": "input_text", "text": "what's in this image?"},
            {
                "type": "input_image",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                "detail": "high"
            },
        ],
    }],
)

# Print the analysis result of the image
print(image_analysis_response.output_text)

