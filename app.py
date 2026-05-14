import streamlit as st
import anthropic
from streamlit_cookies_controller import CookieController
from prompts import SYSTEM_INSTRUCTIONS

st.set_page_config(page_title="Social Protocol Debugger", layout="centered")

client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
MODEL = "claude-haiku-4-5-20251001"

SYSTEM = [{"type": "text", "text": SYSTEM_INSTRUCTIONS, "cache_control": {"type": "ephemeral"}}]

MAX_TURNS = 20
EXTRA_TURNS = 50

cookie = CookieController()

# ── Seed session state from cookies on first load ─────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_protocol" not in st.session_state:
    st.session_state.pending_protocol = None
if "turn_count" not in st.session_state:
    stored = cookie.get("turn_count")
    st.session_state.turn_count = int(stored) if stored else 0
if "used_codes" not in st.session_state:
    stored = cookie.get("used_codes")
    st.session_state.used_codes = set(stored.split(",")) if stored else set()


def stream_response(messages):
    with client.messages.stream(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


def queue_protocol(prompt_text):
    st.session_state.pending_protocol = prompt_text


def turn_limit():
    return MAX_TURNS + (EXTRA_TURNS * len(st.session_state.used_codes))


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Social Protocols")

    if st.button("Cold Start: Coffee Line", use_container_width=True):
        queue_protocol("Give me a word-for-word script for starting a conversation with a stranger in the coffee line at a conference.")

    if st.button("Packet Switch: Go Deeper", use_container_width=True):
        queue_protocol("I'm stuck in small talk and want to move to a real conversation. Give me a packet switch script.")

    if st.button("Exit: The Group Circle", use_container_width=True):
        queue_protocol("How do I leave a group conversation of 3–4 people without it being awkward? Give me the exact script.")

    if st.button("Exit: One-on-One", use_container_width=True):
        queue_protocol("Give me a graceful exit routine for ending a one-on-one conversation at a networking event.")

    if st.button("Error: Name Forgotten", use_container_width=True):
        queue_protocol("I completely forgot the name of someone I've met before and they just said hi. What's the recovery protocol?")

    if st.button("Error: Awkward Silence", use_container_width=True):
        queue_protocol("There's been a silence in my conversation for more than 5 seconds. Give me the error recovery script.")

    if st.button("Handshake: Follow-Up Email", use_container_width=True):
        queue_protocol("Write me a follow-up email script for someone I met briefly at an event. Keep it short and non-weird.")

    if st.button("Buffer: Keep It Going", use_container_width=True):
        queue_protocol("The conversation is stalling but I don't want it to end yet. Give me 3 conversation buffer prompts I can use.")

    st.divider()
    st.caption(f"Responses: {st.session_state.turn_count} / {turn_limit()}")

    # ── Unlock more turns ────────────────────────────────────────────────────
    st.divider()
    with st.expander("Need more turns?"):
        stripe_link = st.secrets.get("STRIPE_LINK", "")
        if stripe_link:
            st.link_button("Get 50 more turns — $5", stripe_link, use_container_width=True)
        st.text_input("Access code", key="code_input", placeholder="DATATECH-XXXXXXXX")
        if st.button("Unlock", use_container_width=True):
            entered = st.session_state.code_input.strip().upper()
            valid_codes = list(st.secrets.get("ACCESS_CODES", []))
            if not entered:
                st.error("Enter a code first.")
            elif entered in st.session_state.used_codes:
                st.error("Code already used this session.")
            elif entered in valid_codes:
                st.session_state.used_codes.add(entered)
                cookie.set("used_codes", ",".join(st.session_state.used_codes))
                st.success(f"+{EXTRA_TURNS} turns unlocked.")
                st.rerun()
            else:
                st.error("Invalid code.")


# ── Main area ────────────────────────────────────────────────────────────────
st.title("Social Protocol Debugger")
st.caption("Explicit scripts. Decision trees. No subtext.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Describe your scenario...")

prompt = user_input or st.session_state.pending_protocol
if prompt:
    st.session_state.pending_protocol = None
    if st.session_state.turn_count >= turn_limit():
        st.warning(
            f"Session limit reached ({turn_limit()} responses). "
            "Unlock more turns in the sidebar or clear your session."
        )
    else:
        st.session_state.turn_count += 1
        cookie.set("turn_count", str(st.session_state.turn_count))
        st.session_state.messages.append({"role": "user", "content": prompt})
        if user_input:
            with st.chat_message("user"):
                st.markdown(prompt)
        with st.chat_message("assistant"):
            reply = st.write_stream(stream_response(st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()
