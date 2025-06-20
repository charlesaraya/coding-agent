import os
import sys
from dotenv import load_dotenv

from google import genai
from google.genai import types

def verbose(prompt, response):
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
 
    client = genai.Client(api_key=api_key)

    flag_verbose = False

    num_args = len(sys.argv)
    if num_args > 1:
        prompt = sys.argv[1]
    else:
        print("missing prompt argument. expecting `python3 main.py [prompt]`")
        exit(1)
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        flag_verbose = True

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)

    print(response.text)
    if flag_verbose:
        verbose(prompt, response)

if __name__ == "__main__":
    main()