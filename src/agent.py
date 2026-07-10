"""
Core agent loop implementing the ReAct pattern:
Reason -> Act (tool call) -> Observe (tool result) -> Repeat -> Final Answer
"""

import os
import json
from tools_schema import TOOLS
from tool_executor import execute_tool
from dotenv import load_dotenv
from openrouter import OpenRouter

load_dotenv()

MAX_ITERATIONS = 6  # hard cap to prevent infinite tool-calling loops

SYSTEM_PROMPT = f"""You are a Daily Planning Agent. Your job is to produce a realistic,
time-blocked schedule for the user's day. You are a function calling AI model.
You are provided with function signatures within <tools></tools> XML tags.
You may call one or more functions to assist with the user query. Don't make assumptions about what values to plug 
into functions. Pay special attention to the properties 'types'. You should use those types as in a Python dict.
For each function call return a json object with function name and arguments within <tool_call></tool_call> XML tags as follows:

<tool_call>
{{"name": <function-name>,"arguments": <args-dict>"}}
</tool_call>

Rules:
1. Always fetch calendar events, weather, and pending tasks before building a plan.
2. Fixed calendar events are non-negotiable — schedule tasks AROUND them.
3. Use weather data to flag any outdoor/commute risk (e.g., heavy rain).
4. Prioritize high-priority tasks with earlier deadlines first, fitting them into free
   time slots between meetings.
5. Produce a final schedule as a clear, time-ordered list from 9:00 to 21:00,
   with each block labeled as [Meeting], [Task], or [Free/Buffer].
6. After gathering all needed data, stop calling tools and give the final schedule
   as plain text — do not call tools again once you have enough information.

Here are the available tools:

<tools>
    {TOOLS}
</tools>

You will be provided with the tool's result once you confirm the call of the tool. You will then use that result to reason and produce the final answer.

<tool_result>
    tool_name : tool_result
</tool_result>

Output Format:
if you want to call a tool you will use the below format:
{{
    "stop_reason" : "tool_call",
    "tool_use" : [
        {{
            "name": <function-name>,
            "input": <args-dict>
        }}
    ]
}}

if you want to finalize the response you will use the below format:
{{
    "stop_reason": "final_answer",
    "final_answer" : "<Your Final Response>"
}}
"""


class DailyPlannerAgent:
    def __init__(self):
        self.client = OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY", ""), )
        self.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def run(self, user_request: str) -> str:
        self.messages.append({"role": "user", "content": user_request})
        # print(self.messages)

        for iteration in range(1, MAX_ITERATIONS + 1):
            print(f"\n--- Agent Iteration {iteration} ---")

            response = self.client.chat.send(
                model=os.getenv("MODEL", ""),
                max_completion_tokens=1500,
                messages=self.messages
            )

            print(f"LLM response: {response.choices[0].message.content}")

            # Append LLM's response (may contain text + tool_use blocks)
            self.messages.append({"role": "assistant", "content": response.choices[0].message.content})

            response_dict = json.loads(response.choices[0].message.content)
            if response_dict.get("stop_reason") == "tool_call":
                tool_use = response_dict.get("tool_use", [])
                for tool in tool_use:
                    tool_name = tool.get("name")
                    tool_input = tool.get("input", {})
                    print(f"Calling tool: {tool_name} with input: {tool_input}")

                    # Execute the tool and get the result
                    tool_result = execute_tool(tool_name, tool_input)
                    print(f"Tool result: {tool_result}")

                    # Append the tool result to the messages for the next iteration
                    self.messages.append({"role": "system", "content": f"<tool_result>{tool_name}:{json.dumps(tool_result)}</tool_result>"})
            elif response_dict.get("stop_reason") == "final_answer":
                final_answer = response_dict.get("final_answer", "")
                print(f"Final answer received: {final_answer}")
                return final_answer

        return "Agent reached maximum iterations without a final answer. Check tool logic."

if __name__ == "__main__":
    agent = DailyPlannerAgent()
    user_query = "Plan my day for 2026-07-16. Fit in my pending tasks around my meetings, and account for the weather."
    final_schedule = agent.run(user_query)
    print("\n--- Final Schedule ---")
    print(final_schedule)