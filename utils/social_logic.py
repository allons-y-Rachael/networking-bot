import random

EXIT_LINES = [
    "It was great meeting you — I want to let you mingle. I'll follow up on LinkedIn.",
    "I promised myself I'd connect with a few more people tonight. Really enjoyed this. Let's stay in touch.",
    "I need to track someone down before they leave, but this was a great conversation. Can I grab your card?",
    "I'll let you go — I know how these things move fast. Really glad we got to talk.",
    "I've taken enough of your time. Thanks for the insight — I'll reach out this week.",
]

PIVOT_LINES = [
    "That's interesting — it actually makes me think about something else. Can I ask you about...",
    "I want to shift gears for a second — what's the biggest thing on your plate right now?",
    "Speaking of that — are you seeing the same thing in your market?",
    "Let me ask you something different — what brought you to this event specifically?",
    "I'm curious — how does that connect to what you're working on day-to-day?",
]


def get_exit_strategy() -> str:
    return random.choice(EXIT_LINES)


def get_pivot() -> str:
    return random.choice(PIVOT_LINES)
