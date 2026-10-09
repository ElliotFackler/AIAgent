import os, argparse, json, sys
import re
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import available_functions, call_function

# Load stuff from .env into our environment
load_dotenv()

# Grab the OpenRouter API key from the .env file
api_key = os.environ.get('OPENROUTER_API_KEY')

# Raise error if the key isn't found.
if api_key is None:
    raise RuntimeError("No API key found")

def main(): # Main!
    # Client for connection
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key,)

    # Get input from the user via CLI
    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("--dir", default=".", help="The directory that the LLM may work in")
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        raise SystemExit("{args.dir} is not a valid directory")

    # Set the working directory so the agent can't change it later
    working_directory = os.path.abspath(args.dir)

    # Combine the system prompt and the user prompt to be sent to the LLM
    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": args.user_prompt},
    ]

    # If the user wants more details
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    # Feedback loop
    for i in range(20):
        # Get a response from the LLM. I set the temperature to 0 because I was having trouble getting the expected result.
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions,
            tool_choice="auto"
        )

        if response is None:
            raise RuntimeError("No response received")

        # Return token usage if user has verbose enabled
        if args.verbose:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        # Take the message from the LLM and add it to the context
        message = response.choices[0].message
        messages.append(message)

        # Iterate through and print the functions that the agent is using
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_arguments = json.loads(tool_call.function.arguments or "{}")
                if args.verbose:
                    print(f"Calling function: {function_name}({function_arguments})")

                result = call_function(tool_call, args.dir, args.verbose)

                if result is None:
                    raise RuntimeError("No result returned")
                
                messages.append(result)

                if args.verbose:
                    print(f"-> {result['content']}")
                else:
                    print(result["content"])
        else:
            print(message.content)
            break

        # Every five loops, get input from the user
        if (i+1) % 5 == 0:
            note = input('Add guidance, press "Enter" to continue, or press "q" to quit \n').strip()
            if note.lower() == 'q':
                break
            if note:
                messages.append({"role": "user", "content": note})

    # If the loop goes on for too long, end the program to avoid burning too many tokens
    else:
        print("Max loops reached")
        sys.exit()




if __name__ == "__main__":
    main()
