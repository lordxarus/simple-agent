import logging
import os
import sys
from functions.call_function import call_function
import functions.schemas as schemas
import time
import logger
from dotenv import load_dotenv
from google import genai
from google.genai import types


def print_usage():
    print(
        """
usage: agent prompt [options]
options:
  --help, -h         Print help message
  --verbose, -V      Print information on token usage
  --dir, -d          Set the working directory
          """
    )


class _NoToolNoise(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return (
            record.getMessage()
            != "Warning: there are non-text parts in the response: ['function_call'],returning concatenated text result from text parts,check out the non text parts for full response from model."
        )


def main():
    logging.getLogger("google_genai.types").addFilter(_NoToolNoise())

    n_opt = 0
    verbose: bool = False

    prompt: str = ""

    work_dir = "calculator"

    system_prompt = f"""
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read the content of text files
- Write text to files
- Run python files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

This is not an interactive session, you are operating as an autonomous agent. Do NOT ask the user for input. Do NOT ask the user any questions.

When you are satisfied the objective is complete emit the string "MAGIC_EOF_STR_"
"""
    if not load_dotenv():
        print("error: couldn't find any api keys in .env")
        exit(1)

    print_dbg = logger.get_print_dbg()

    for arg in sys.argv:
        match arg:
            case "--verbose" | "-V":
                n_opt += 1
                verbose = True
                print("info: enabling verbose output")
            case "--dir | -d":
                pass
            case "--help" | "-h":
                print_usage()
                exit(0)

    if (len(sys.argv) - n_opt) < 2:
        print_usage()
        exit(1)
    else:
        # [1:] removes the file e.g src/main.py and then we filter out the options
        prompt = " ".join([arg for arg in sys.argv[1:] if not arg.startswith("-")])
        print_dbg(f'using prompt "{prompt}"')

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    api_key = os.environ.get("GEMINI_API_KEY")

    available_functions = types.Tool(
        function_declarations=[
            schemas.get_files_info,
            schemas.get_file_content,
            schemas.write_file,
            schemas.run_python_file,
        ]
    )
    client = genai.Client(api_key=api_key)
    while True:
        resp = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        if resp.usage_metadata is not None and verbose:
            print("\n--- Statistics ---")
            print(f"prompt_token_count == {resp.usage_metadata.prompt_token_count}")
            print(f"cache_tokens_details == {resp.usage_metadata.cache_tokens_details}")
            print(
                f"candidates_token_count == {resp.usage_metadata.candidates_token_count}\n"
            )

        if resp.text:
            print(f"response: {resp.text}")
            if "MAGIC_EOF_STR_" in resp.text:
                break
        if resp.candidates:
            if len(resp.candidates) >= 1:
                if resp.candidates[0].content is not None:
                    messages.append(resp.candidates[0].content)
        if resp.function_calls is not None:
            for call in resp.function_calls:
                # TODO add CLI option for this
                result = call_function(call, work_dir, verbose)
                if not result.parts:
                    raise ValueError("result.parts is None")
                if len(result.parts) == 0:
                    raise ValueError("result.parts len == 0")
                if not result.parts[0].function_response:
                    raise ValueError("no function_response in result.parts[0")
                if not result.parts[0].function_response.response:
                    raise ValueError("no response in function_response")
                if verbose:
                    print(f"-> {result.parts[0].function_response.response['result']}")
                messages.append(types.Content(parts=result.parts, role="user"))

        time.sleep(1)


if __name__ == "__main__":
    main()
