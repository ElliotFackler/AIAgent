AI Agent

Purpose:
* This is an AI Agent that can work within a directory specified by the user. It read from and write to files and answer questions. It is a code writing assistant.

How To Use:
* You can run this tool using the following command "uv run main.py" followed by your question. You can add the flag "--verbose" for an indepth answer and stats.

Setup:
* You will need to sign up for OpenRouter and get an API key. You can store this in your .env file. Title it OPENROUTER_API_KEY
* Install UV

Tech
* OpenRouter: This AI Agent utilizes OpenRouter to find the best available free-use LLM. Be aware that free levels have low token limits. Using "--verbose" on your cmd will show the tokens used in the request.

Interesting Decisions:
* I currently include a line in the main.py file that forces the agent to use "run_python_file" when the user uses the either the word "run" or "execute". I was having trouble getting the agent to use this file as it preferred using "get_file_info" when I would use prompts like "uv run main .py 'run the main.py' file".

Dependencies:
* OpenAI 2.44.0
* Python dotenv 1.1.0