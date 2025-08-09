import os
from dotenv import load_dotenv
import streamlit as st

# Your phi/OpenAI/YFinance imports (same as original)
from phi.tools.duckduckgo import DuckDuckGo
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
# from phi.model.google import Gemini
# from phi.model.deepseek import DeepSeekChat
from phi.model.groq import Groq

import openai

# ---------------------------
# Helper / setup functions
# ---------------------------

def load_config():
    """
    Load secrets / env vars. Don't call st.set_page_config here.
    """
    # load_dotenv(os.getenv('DOTENV_PATH', '.env'))
    # Expecting Streamlit secrets to have OPENAI_API_KEY
    api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None
    if not api_key:
        # If you prefer, raise or st.error later in UI
        return None
    openai.api_key = api_key
    return api_key

def get_companies():
    return {
        'Apple Inc.': 'AAPL',
        'Microsoft Corp.': 'MSFT',
        'NVIDIA': 'NVDA',
        'Tesla': 'TSLA',
        'BlackRock': 'BLK',
        'LVMH': 'MC.PA',
        'Samsung Electronics': '005930.KS',
        'Amazon': 'AMZN',
        'Alphabet': 'GOOGL',
        'Meta Platforms': 'META',
        'Berkshire Hathaway': 'BRK.B',
        'Visa': 'V',
        'JPMorgan Chase': 'JPM',
        'Johnson & Johnson': 'JNJ',
        'UnitedHealth Group': 'UNH',
        'Procter & Gamble': 'PG',
        'Mastercard': 'MA',
        'Eli Lilly': 'LLY',
        'Home Depot': 'HD',
        'Walmart': 'WMT',
        'Bank of America': 'BAC',
        'Disney': 'DIS',
        'Intel': 'INTC',
        'Oracle': 'ORCL'
    }

def init_agents():
    """
    Initialize agents with a shared base model.
    Adjust model IDs/keys as required for your environment.
    """
    base_model = OpenAIChat(id="gpt-3.5-turbo-0125", stream=True)

    web_agent = Agent(
        name="Web Agent",
        role="Search the web for information",
        model=base_model,
        tools=[DuckDuckGo()],
        instructions=[
            "Summarize and always include sources (links)",
            "Provide precise and clear information on the topic"
        ],
        show_tools_calls=True,
        markdown=True,
    )
    finance_agent = Agent(
        name="Finance Agent",
        model=base_model,
        tools=[YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            company_news=True,
        )],
        instructions=[
            "Use tables to display data, not text",
            "Be concise and restrict to the topic",
            "Always include sources (links)",
        ],
        show_tools_calls=True,
        markdown=True,
    )
    final_agent = Agent(
        name="Final Answer Agent",
        model=base_model,
        instructions=[
            "Summarize clearly and precisely",
            "Always include sources (links)",
            "Use tables to display data"
        ],
        markdown=True,
    )
    return web_agent, finance_agent, final_agent

def send_input():
    """
    Callback for the Send button.
    We set a flag in session_state so app flow can continue.
    """
    st.session_state.send_input = True

def get_user_inputs(companies: dict):
    st.sidebar.header("Select Companies")
    # dynamic checkboxes
    selected = [
        ticker for name, ticker in companies.items()
        if st.sidebar.checkbox(name, value=False)
    ]

    tickers_input = st.text_input(
        "Tickers (comma-separated):",
        value=", ".join(selected),
        key="tickers_input"
    )
    user_query = st.text_input("Your Query:", key="user_query")
    return tickers_input, user_query

def fetch_agent_responses(tickers, combined_payload, web_agent, finance_agent):
    # 5a. Web search
    with st.spinner("🔎 Searching the web..."):
        web_resp = web_agent.run(f"Explain {combined_payload} with web sources")
    # 5b. Finance data
    with st.spinner("💹 Fetching finance data..."):
        finance_resp = finance_agent.run(f"Get financial details for {combined_payload}")
    return web_resp, finance_resp

def summarize_final_answer(combined_payload, web_resp, finance_resp, final_agent):
    prompt = f"""
User Query: {combined_payload}

Web Information:
{web_resp.get_content_as_string()}

Finance Information:
{finance_resp.get_content_as_string()}

Now, based on this information, give a final summarized answer in a clear, friendly format.
"""
    with st.spinner("✍️ Generating final answer..."):
        final_resp = final_agent.run(prompt)
    return final_resp.get_content_as_string()

# ---------------------------
# Main app
# ---------------------------

def main():
    # IMPORTANT: call this once and before any other st.* calls that render content
    st.set_page_config(
        page_title="MarketBot | Stock & News Insights",
        layout="wide",
        initial_sidebar_state="expanded"   # <-- sidebar open by default
    )

    # Load API keys & config
    api_key = load_config()
    if not api_key:
        st.error("Missing OPENAI_API_KEY in Streamlit secrets. Please add it and reload the app.")
        # Still show basic UI so user can edit inputs if needed
    companies = get_companies()

    # Initialize agents (may be slow — consider caching if needed)
    try:
        web_agent, finance_agent, final_agent = init_agents()
    except Exception as e:
        st.error(f"Failed to initialize agents: {e}")
        return

    st.title("📊 Stock Insights & Real-Time Market Answers")

    # Initialize session state flags
    if "send_input" not in st.session_state:
        st.session_state.send_input = False
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Inputs
    tickers_input, user_query = get_user_inputs(companies)

    # Use on_click to avoid calling send_input immediately
    st.button("Send", on_click=send_input)

    # Proceed if button clicked (flag set)
    if st.session_state.get("send_input", False):
        # Clear flag immediately so subsequent reruns don't auto-fire
        st.session_state.send_input = False

        # Validate form
        tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
        if not tickers:
            st.error("Please select or enter at least one ticker.")
            return
        if not user_query.strip():
            st.error("Please enter your query.")
            return

        # Combine payload: nicer format than Python list literal
        combined = f"{', '.join(tickers)} — {user_query}"

        # Fetch intermediate results
        try:
            web_resp, finance_resp = fetch_agent_responses(tickers, combined, web_agent, finance_agent)
        except Exception as e:
            st.error(f"Error while fetching data from agents: {e}")
            return

        # Summarize final answer
        try:
            final_answer = summarize_final_answer(combined, web_resp, finance_resp, final_agent)
        except Exception as e:
            st.error(f"Error while summarizing final answer: {e}")
            return

        # Display final result (markdown - agents already produce markdown)
        st.markdown(final_answer)

if __name__ == "__main__":
    main()
