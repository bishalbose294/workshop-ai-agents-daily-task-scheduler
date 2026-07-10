"""
Core agent loop implementing the ReAct pattern:
Reason -> Act (tool call) -> Observe (tool result) -> Repeat -> Final Answer
"""

import os
import json
from src.tools_schema import TOOLS
from src.tool_executor import execute_tool
from dotenv import load_dotenv
from openrouter import OpenRouter
from colorama import Fore

load_dotenv()

MAX_ITERATIONS = 6  # hard cap to prevent infinite tool-calling loops

SYSTEM_PROMPT = f"""You are a Daily Planning Agent. Your job is to produce a realistic,
time-blocked schedule for the user's day. You are a function-calling AI model.
You are provided with function signatures within <tools></tools> XML tags.
You may call one or more functions to assist with the user query. Don't make assumptions
about what values to plug into functions. Pay special attention to the 'type' field of each
property — use those exact types as you would in a Python dict.

Here are the available tools:
<tools>
    {TOOLS}
</tools>

You will be provided with each tool's result once you confirm the call of the tool.
You will then use that result to reason and produce the final answer.
<tool_result>
    tool_name : tool_result
</tool_result>

Rules:
1. Always understand what to fetch which function to call and accordingly.
 Call the calendar events, weather, and pending tasks before building a plan.
2. Fixed calendar events are non-negotiable — schedule tasks AROUND them.
3. Use weather data to flag any outdoor/commute risk (e.g., heavy rain).
4. Prioritize high-priority tasks with earlier deadlines first, fitting them into free
   time slots between meetings.
5. Produce a final schedule as a clear, time-ordered list from 9:00 to 21:00,
   with each block labeled as [Meeting], [Task], or [Free/Buffer].
6. After gathering all needed data, stop calling tools and give the final schedule
   as plain text inside the final_answer field — do not call tools again once you
   have enough information.
7. If the user plans to stay at home then we do not need any data for weather hence you dont need to call
  weather function.

OUTPUT CONTRACT — STRICT, NON-NEGOTIABLE:
- Your entire response MUST be a single valid JSON object. Nothing before it, nothing
  after it. No markdown code fences (no ```), no XML tags, no commentary outside the JSON.
- Use ONLY the two shapes below. Never mix them. Never invent new keys. Never omit a
  required key. Never change a key name or its casing.
- Use double quotes for every key and every string value. Never use single quotes.
  Never leave a trailing comma after the last item in an object or array.
- All property values must match the declared type exactly (string stays string,
  never wrap a string in extra quotes, never leave a dangling quote character).
- The "input" object for a tool call must contain exactly the arguments defined in
  that tool's schema — correct key names, correct types, no extra keys, no missing
  required keys, no guessed values.
- Inside "final_answer", the entire schedule must be encoded as ONE JSON string:
  - Every line break inside the schedule must be written as the two characters \n
    (backslash-n), never as a raw newline.
  - Any double quote character that must appear inside the text must be escaped as \".
  - Do not use raw tab characters; use spaces for alignment.
- Before returning your response, mentally verify it parses as valid JSON:
  matching braces and brackets, no trailing commas, no unescaped quotes or newlines,
  no comments, no extra text outside the single JSON object.

Shape 1 — calling one or more tools:
{{
    "stop_reason": "tool_call",
    "tool_use": [
        {{
            "name": "<function-name>",
            "input": {{"<param-name>": "<param-value>"}}
        }}
    ]
}}

Shape 2 — finalizing the response:
{{
    "stop_reason": "final_answer",
    "final_answer": "09:00-09:30 [Task] Review pull request #482\n09:30-10:00 [Meeting] Client Standup Call (Zoom)\n..."
}}

Return exactly one JSON object matching Shape 1 or Shape 2. Nothing else.
"""


class DailyPlannerAgent:
    def __init__(self):
        self.client = OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY", ""), )
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def run(self, user_request: str) -> str:
        self.messages.append({"role": "user", "content": user_request})

        for iteration in range(1, MAX_ITERATIONS + 1):
            print(Fore.LIGHTGREEN_EX +f"\n--- Agent Iteration {iteration} ---")

            response = self.client.chat.send(
                model=os.getenv("MODEL", ""),
                max_completion_tokens=1500,
                messages=self.messages
            )

            # Append LLM's response (may contain text + tool_use blocks)
            self.messages.append({"role": "assistant", "content": response.choices[0].message.content})

            response_dict = json.loads(response.choices[0].message.content)
            if response_dict.get("stop_reason") == "tool_call":
                tool_use = response_dict.get("tool_use", [])
                for tool in tool_use:
                    tool_name = tool.get("name")
                    tool_input = tool.get("input", {})
                    print(Fore.LIGHTGREEN_EX +f"Calling tool: {tool_name} with input: {tool_input}")

                    # Execute the tool and get the result
                    tool_result = execute_tool(tool_name, tool_input)
                    print(Fore.LIGHTGREEN_EX +f"Tool result: {tool_result}")

                    # Append the tool result to the messages for the next iteration
                    self.messages.append({"role": "system", "content": f"<tool_result>{tool_name}:{json.dumps(tool_result)}</tool_result>"})
                    print("")
            elif response_dict.get("stop_reason") == "final_answer":
                final_answer = response_dict.get("final_answer", "")
                return final_answer

        return "Agent reached maximum iterations without a final answer. Check tool logic."

if __name__ == "__main__":
    agent = DailyPlannerAgent()
    user_query = "Plan my day for 2026-07-16 I will mostly be staying at home I also dont want to do any tasks hence only consider meetings for today."
    final_schedule = agent.run(user_query)
    print("\n--- Final Schedule ---\n")
    print(final_schedule)