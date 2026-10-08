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
if api_key == None:
    raise RuntimeError("No API key found")




def main(): # Main!
    # Client for connection
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key,)

    # Get input from the user via CLI
    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Combine the system prompt and the user prompt to be sent to the LLM
    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": args.user_prompt},
    ]

    # Feedback loop
    for i in range(20):
        # Get a response from the LLM. I set the temperature to 0 because I was having trouble getting the expected result.
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions,
            tool_choice=(
                {"type": "function", "function": {"name": "run_python_file"}}
                if re.match(r"^\s*(?:(?:please|can you)\s+)*(?:run|execute)\b", args.user_prompt, re.IGNORECASE)
                else "auto"
            ),
        )

        # If we don't hear back from the LLM, raise an error
        if response == None:
            raise RuntimeError("No response received")

        # If the user wants more details
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        # Take the message from the LLM and add it to the context
        message = response.choices[0].message
        messages.append(message)

        #TEMP
        print(json.dumps(messages, indent=2, default=str))

        # Iterate through and print the functions that LLM is using
        if message.tool_calls != None:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_arguments = json.loads(tool_call.function.arguments or "{}")
                if args.verbose == True:
                    print(f"Calling function: {function_name}({function_arguments})")
                result = call_function(tool_call, args.verbose)

                messages.append(result)

                if result == None:
                    raise RuntimeError("No result returned")
                if args.verbose == True:
                    print(f"-> {result['content']}")
                else:
                    print(result["content"])
        else:
            print(message.content)

        # Every five loops, get input from the user
        if (i+1) % 6 == 0:
            note = input('Add guidance, press "Enter" to continue, or press "q" to quit').strip()
            if note.lower() == 'q':
                break
            elif note:
                messages.append({"role": "user", "content": note})
            else:
                continue

    # If the loop goes on for too long, end the program to avoid burning too many tokens
    print("Max loops reached")
    sys.exit()




if __name__ == "__main__":
    main()
