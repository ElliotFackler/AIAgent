import os, argparse, json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import available_functions

load_dotenv()

api_key = os.environ.get('OPENROUTER_API_KEY')

if api_key == None:
    raise RuntimeError("No API key found")




def main():
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key,)

    parser = argparse.ArgumentParser(description="chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

    if response == None:
        raise RuntimeError("No response received")

    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print(response.choices[0].message.content)
    print(response.choices[0].message.tool_calls)
    #print(response.choices[0].message.tool_calls.function.name)



if __name__ == "__main__":
    main()
