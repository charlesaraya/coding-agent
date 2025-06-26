import os
import sys
from dotenv import load_dotenv

from google import genai
from google.genai import types

from functions.schemas import available_functions
import prompts
from call_function import call_function

MAX_ITERATIONS = 20
MODEL_NAME = "gemini-2.0-flash-001"

def verbose(prompt, response):
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
 
    client = genai.Client(api_key=api_key)

    flag_verbose = False

    num_args = len(sys.argv)
    if num_args <= 1:
        print("Missing prompt argument")
        print('Usage: python main.py "<prompt>"')
        print('Example: python main.py "Foo bar baz?"')
        exit(1)
    if num_args > 1:
        prompt = sys.argv[1]
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        flag_verbose = True

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    iteration = 0
    isValidResponse = False
    while iteration < MAX_ITERATIONS:
        while not isValidResponse:
            try:
                m_response = client.models.generate_content(
                    model = MODEL_NAME,
                    contents = messages,
                    config = types.GenerateContentConfig(
                        system_instruction = prompts.system_prompt,
                        tools = [available_functions]
                    )
                )
            except Exception as e:
                print(f"error: {e}")
            if m_response.text:
                isValidResponse = True

        if flag_verbose:
            print(f"Agent: {m_response.text}\n")

        # Populate messages with the agent's intent
        for candidate in m_response.candidates:
            messages.append(candidate.content)
            break

        # the model wants a function call
        if m_response.function_calls:
            for fc in m_response.function_calls:
                fncall_result = call_function(fc, flag_verbose)
                fn_response = fncall_result.parts[0].function_response.response

                if not fn_response:
                    raise Exception("func call has no response")
                if flag_verbose:
                    print(f"-> {fncall_result.parts[0].function_response.response}")

                messages.append(fncall_result)

            if flag_verbose:
                verbose(prompt, m_response)
        # otherwise the agent is done with the task
        else:
            print(m_response.text)
            break

        isValidResponse = False
        iteration += 1

if __name__ == "__main__":
    main()