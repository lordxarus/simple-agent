import os
import sys
import logger
from dotenv import load_dotenv
from google import genai
from google.genai import types


def print_usage():
    print(
        """
                usage: agent prompt [options]
                options:
                    --help, -h         print help message
                    --verbose, -V      print information on token usage
          """
    )


def main():
    n_opt = 0
    verbose: bool = False

    prompt: str = ""

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    if not load_dotenv():
        print("error: couldn't find any api keys in .env")
        exit(1)

    print_dbg = logger.get_print_dbg()

    for arg in sys.argv:
        match arg:
            case "--verbose" | "-V":
                n_opt += 1
                verbose = True
            case "--help" | "-h":
                print_usage()
                exit(0)

    if (len(sys.argv) - n_opt) < 2:
        print("usage: agent prompt")
        exit(1)
    else:
        # [1:] removes the file e.g src/main.py and then we filter the options
        prompt = [arg for arg in sys.argv[1:] if not arg.startswith("-")][0]
        print_dbg(f'using prompt "{prompt}"')

    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt,
    )
    if resp.usage_metadata is not None and verbose:
        print(f"prompt_token_count == {resp.usage_metadata.prompt_token_count}")
        print(f"cache_tokens_details == {resp.usage_metadata.cache_tokens_details}")
        print(
            f"candidates_token_count == {resp.usage_metadata.candidates_token_count}\n"
        )

    print(resp.text)


if __name__ == "__main__":
    main()
