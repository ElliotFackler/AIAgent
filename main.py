import os, argparse, json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import available_functions, call_function

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

    message = response.choices[0].message

    # Iterate through and print the functions that LLM is using
    if message.tool_calls != None:
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            function_arguments = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {function_name}({function_arguments})")
            result = call_function(tool_call, args.verbose)

            if result == None:
                raise Error("No result returned")
            if args.verbose == True:
                print(f"-> {result['content']}")
    else:
        print(message.content)




if __name__ == "__main__":
    main()
