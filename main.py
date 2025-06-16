import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions

def main():
    load_dotenv()
   
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("no prompt provided")
        sys.exit(1)

    user_prompt = " ".join(args)
    messages = [
        types.Content(role="user",parts=[types.Part(text=user_prompt)]),
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

   


    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )

    if verbose:
        print("User prompt: ", user_prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if not response.function_calls == None:
        for call in response.function_calls:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print("Response:")
        print(response.text)


if __name__ == "__main__":
    main()
