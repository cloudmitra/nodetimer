import os
import json
import requests

# Sample JSON data (could come from a file or remote source)
data = """
{
  "environments": [
    {
      "name": "dev",
      "endpoints": [
        { "name": "Dev API 1", "url": "https://jsonplaceholder.typicode.com/posts/1" },
        { "name": "Dev API 2", "url": "https://jsonplaceholder.typicode.com/posts/2" }
      ]
    },
    {
      "name": "int",
      "endpoints": [
        { "name": "Int API 1", "url": "https://int-api1.example.com" },
        { "name": "Int API 2", "url": "https://int-api2.example.com" }
      ]
    }
  ]
}
"""

def process_response(data):
    """
    This function receives the response from the endpoint and
    can be used to call another API with that data.
    """
    another_api_url = "https://httpbin.org/post"  # Sample API that echoes back the payload
    try:
        result = requests.post(another_api_url, json=data)
        print(f"   ➤ Forwarded to another API - Status: {result.status_code}")
    except requests.RequestException as e:
        print(f"   ➤ Error forwarding to another API: {e}")

def call_environment_apis():
    json_data = json.loads(data)
    env_code = os.getenv("ENVIRONMENT_CODE")

    if not env_code:
        print("ENVIRONMENT_CODE is not set.")
        return

    # Find environment by name
    environment = next((env for env in json_data["environments"] if env["name"] == env_code), None)

    if not environment:
        print(f"No matching environment found for '{env_code}'.")
        return

    print(f"Calling APIs for environment '{env_code}':")
    for endpoint in environment["endpoints"]:
        name = endpoint["name"]
        url = endpoint["url"]
        try:
            response = requests.get(url, timeout=5)
            print(f" - {name} ({url}) => Status: {response.status_code}")
            if response.ok:
                process_response(response.json())  # Pass JSON data to another API
            else:
                print(f"   ➤ Received error response: {response.status_code}")
        except requests.RequestException as e:
            print(f" - {name} ({url}) => Error: {e}")

# Call main function
call_environment_apis()
