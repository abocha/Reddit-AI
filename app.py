from agno.agent import Agent
# from agno.tools.reddit import RedditTools
from agno.models.google import Gemini
from reddit import get_post_comments
from instructions import instructions

import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

model = Gemini(
    id="gemini-1.5-flash",
    api_key=GEMINI_API_KEY
)

reddit_tools = [get_post_comments]

agent = Agent(
    name="RedditAI",
    model=model,
    instructions=instructions,
    tools=reddit_tools,
    show_tool_calls=True,
    read_chat_history=True,
    markdown=True,
    debug_mode=True
)

# # CLI
while True:
    prompt = input("You: ")
    if prompt.lower().strip() == 'exit':
        break

    response = agent.run(prompt)
    print(response.content)
