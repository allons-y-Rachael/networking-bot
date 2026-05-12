import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SCENARIO_PROMPTS = {
    "Cold Intro": "You are helping someone introduce themselves cold at a networking event. Be warm, direct, and brief.",
    "Follow-Up": "You are helping someone follow up with someone they briefly met. Reference the prior meeting naturally.",
    "Ask for Intro": "You are helping someone ask a mutual contact for an introduction. Make it easy to say yes.",
    "Reconnect": "You are helping someone reconnect with someone they haven't spoken to in a while. Keep it genuine and low-pressure.",
}


def get_script(scenario: str, context: str) -> str:
    system_prompt = SCENARIO_PROMPTS.get(scenario, SCENARIO_PROMPTS["Cold Intro"])
    user_prompt = f"Context about the person I'm talking to: {context}\n\nWrite a short, natural opening script for this scenario. 3–5 sentences max."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=300,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()
