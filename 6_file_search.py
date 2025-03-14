from openai import OpenAI
import os
import json
import requests
import urllib3
import ssl
import certifi

# get env variable
api_key = os.getenv("OPENAI_API_KEY")

# Configure client with additional options
client = OpenAI(
    api_key=api_key,
    # Uncomment the following line if you're behind a proxy
    # http_client=httpx.Client(proxy="http://your-proxy:port")
)

def upload_local_file(client, file_path, purpose="assistants", max_retries=3):
    """
    Upload a local file to OpenAI.
    
    Args:
        client: OpenAI client instance
        file_path: Path to the local file
        purpose: Purpose of the file (default: "assistants")
        max_retries: Maximum number of retry attempts (default: 3)
        
    Returns:
        The file ID of the uploaded file
    """
    # Verify the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist")
    
    # Print SSL info for debugging
    print(f"Using SSL version: {ssl.OPENSSL_VERSION}")
    print(f"Using certifi version: {certifi.__version__}")
    print(f"Certificate path: {certifi.where()}")
    
    # Try uploading with retries
    retry_count = 0
    last_error = None
    
    while retry_count < max_retries:
        try:
            # Upload the local file
            with open(file_path, "rb") as file_content:
                result = client.files.create(
                    file=file_content,
                    purpose=purpose
                )
            
            print(f"File uploaded successfully with ID: {result.id}")
            return result.id
            
        except Exception as e:
            last_error = e
            retry_count += 1
            print(f"Attempt {retry_count} failed: {str(e)}")
            
            # Wait a bit before retrying
            import time
            time.sleep(1)
    
    # If we get here, all retries failed
    print("\nTroubleshooting tips:")
    print("1. Check your internet connection")
    print("2. Verify your OpenAI API key is correct")
    print("3. Check if you're behind a proxy or firewall that might be blocking the connection")
    print("4. Try updating your SSL certificates: pip install --upgrade certifi")
    print("5. Try using a different network connection")
    
    raise Exception(f"Failed to upload file after {max_retries} attempts. Last error: {str(last_error)}")

# Test connection to OpenAI API
def test_openai_connection():
    try:
        print("Testing connection to OpenAI API...")
        # Simple API call that doesn't cost tokens
        models = client.models.list()
        print("Connection successful! Available models:")
        for model in models.data[:3]:  # Show just first 3 models
            print(f"- {model.id}")
        return True
    except Exception as e:
        print(f"Connection test failed: {str(e)}")
        return False


# Get or create vector store
vector_store_id = None
file_id = None
try:
    # create vector store if it doesn't exist
    if not os.path.exists("vector_store_id.txt"):
        vector_store = client.vector_stores.create(
            name="knowledge_base"
        )
        vector_store_id = vector_store.id
        print(f"Created vector store with ID: {vector_store_id}")
        with open("vector_store_id.txt", "w") as f:
            f.write(vector_store_id)
        file_id = upload_local_file(client, "files/intro_to_ml.pdf", max_retries=2)
        if not file_id:
            file_id = "file-Q3RrXhn8AR3u63GXzEMSLG"  # this file should exist in uploads

        # add file to vector store
        client.vector_stores.files.create(
            vector_store_id=vector_store_id,
            file_id=file_id
        )
    else:
        with open("vector_store_id.txt", "r") as f:
            vector_store_id = f.read().strip()
            print(f"Using existing vector store with ID: {vector_store_id}")
except Exception as e:
    print(f"Error with vector store operations: {str(e)}")

# use file search tool
response = client.responses.create(
    model="gpt-4o-mini",
    input="Who is the author of the book?",
    tools=[{
        "type": "file_search",
        "vector_store_ids": [vector_store_id],
        "max_num_results": 3   # default is 10
    }],
    include=["output[*].file_search_call.search_results"]  # returns search results in the response
    
)

# print the final response
print("Response text:")
print(response.output_text)

# print entire response including search results and citations
print("\n--- Full Response JSON ---")
print(response.model_dump_json(indent=4))

