## AI Agent
This is a Python CLI AI coding agent that uses OpenRouter LLMs to read, run, and write files within a user-chosen directory.

## Purpose:
* This is an AI Agent that can work within a directory specified by the user. It can read and write files and answer questions. It is a code writing assistant.

## How To Use:
* You can run this tool using the following command "uv run main.py" followed by your question. You can add the flag "--verbose" for an in-depth answer and stats. You can add "--dir" to decide the working directory of the agent. If no directory is specified, it defaults to your open directory in the CLI.
* Example 1: "uv run main.py 'Write a hello world print statement to a new file called helloworld.py' --verbose --dir ./calculator"
* Example 2: "uv run main.py 'Fix the weight error in calculator.py'"

## Setup:
* Clone the repo
* Sync UV: https://docs.astral.sh/uv/getting-started/installation/
* Sign up for OpenRouter: https://openrouter.ai
* Get an API key on OpenRouter. You can store this in your .env file. Title it OPENROUTER_API_KEY. Example: OPENROUTER_API_KEY=your_api_key_here

## Tech:
* OpenRouter: This AI Agent utilizes OpenRouter to find the best available free-use LLM. Be aware that free levels have low token limits. Using "--verbose" on your cmd will show the tokens used in the request.

## Dependencies:
* See pyproject.toml

## Safety Note:
* This agent can read and write files so only run it in a sandbox or a folder that you don't mind changing

## Challenges & Choices in Production:
* After I made all the functions and allowed the LLM to use them, I ran into a calling issue. Whenever I would try to get the LLM to execute a function by using "run_python_file", it would call "get_files_info" instead. My first attempted fix was to be more specific in the system prompt but still no dice. After some frustration, I added a regex check on the user input so that if it began with "execute" or "run", it would force the LLM to use "run_python_file". This got the LLM to run the correct function but I was unhappy with this solution as I could foresee this causing other issues: e.g. "Execute a check on main.py's metadata". After poking around each function's schema, I realized that the LLM must be getting confused because the descriptions weren't clear enough. I made the descriptions for each function more specific and it began to call the "run_python_file" function when I intended it and the regex check was no longer needed. The lesson: The model's choice of function is mostly based on the schema provided. The clearer the schema, the greater the accuracy of the LLM.
* The very last issue I dealt with in this project was that sometimes I would get an error code 400 because the API request was malformed. I isolated it to the third index of messages which was the return from call_functions.py. The problem was that the last part of the object wasn't being stringified. I added str() to it and problem solved.