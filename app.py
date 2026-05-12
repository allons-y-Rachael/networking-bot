import streamlit as st
from utils.scripts import get_script
from utils.social_logic import get_exit_strategy, get_pivot

st.set_page_config(page_title="Networking Bot", layout="centered")

st.title("Networking Bot")
st.caption("Your AI-powered conversation navigator for networking events.")

# --- Sidebar ---
st.sidebar.header("Settings")
scenario = st.sidebar.selectbox(
    "Conversation scenario",
    ["Cold Intro", "Follow-Up", "Ask for Intro", "Reconnect"],
)
context = st.sidebar.text_area("Context (who are you talking to?)", placeholder="e.g. VP of Sales at a medtech company, met at a conference")

# --- Main panel ---
if st.button("Generate Opening Script"):
    if not context:
        st.warning("Add some context about who you're talking to.")
    else:
        with st.spinner("Crafting your opener..."):
            script = get_script(scenario=scenario, context=context)
        st.subheader("Your Script")
        st.write(script)

st.divider()

st.subheader("Social Toolkit")
col1, col2 = st.columns(2)

with col1:
    if st.button("The Exit"):
        exit_line = get_exit_strategy()
        st.info(exit_line)

with col2:
    if st.button("The Pivot"):
        pivot_line = get_pivot()
        st.info(pivot_line)
