import os
import sys

from google import genai
from google.genai import types

from functions.schemas import available_functions
from internal.config import Config
import prompts
from call_function import call_function

def verbose(prompt, response):
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}\n")

def print_agent_response(response):
    for part in response.candidates[0].content.parts:
        if part.text:
            print(f"Agent says: {part.text}")
        if part.function_call:
            print(f"[Function Call] {part.function_call.name}({part.function_call.args})")

def main():
    cfg = Config()

    client = genai.Client(api_key=cfg.api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=cfg.prompt)])
    ]

    iteration = 0
    isValidResponse = False
    while iteration < cfg.iterations:
        while not isValidResponse:
            try:
                m_response = client.models.generate_content(
                    model = cfg.model_name,
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

        if cfg.verbose:
            print_agent_response(m_response)

        # Populate messages with the agent's intent
        for candidate in m_response.candidates:
            messages.append(candidate.content)
            break

        # the model wants a function call
        if m_response.function_calls:
            for fc in m_response.function_calls:
                fncall_result = call_function(fc, cfg.verbose)
                fn_response = fncall_result.parts[0].function_response.response

                if not fn_response:
                    raise Exception("func call has no response")
                if cfg.verbose:
                    print(f"-> {fncall_result.parts[0].function_response.response}")

                messages.append(fncall_result)

            if cfg.verbose:
                verbose(cfg.prompt, m_response)
        # otherwise the agent is done with the task
        else:
            print(m_response.text)
            break

        isValidResponse = False
        iteration += 1

if __name__ == "__main__":
    main()