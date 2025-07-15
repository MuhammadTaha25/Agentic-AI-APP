# import os
# from dotenv import load_dotenv
# import streamlit as st
# from phi.tools.duckduckgo import DuckDuckGo
# from phi.agent import Agent
# # from phi.model.openai import OpenAIChat
# from phi.tools.yfinance import YFinanceTools
# # from phi.model.google import Gemini
# # from phi.model.google import Gemini
# # from phi.model.deepseek import DeepSeekChat
# from phi.model.groq import Groq

# # import openai
# # # --- 1. Load configuration from .env ---
# def load_config():
#     # load_dotenv(os.getenv('DOTENV_PATH', '.env'))
#     # openai.api_key = st.secrets["OPENAI_API_KEY"]
#     st.set_page_config(page_title="Stock & Query App",)

# # --- 2. Define the pool of available companies ---
# def get_companies():
#     return {
#         'Apple Inc.': 'AAPL',
#         'Microsoft Corp.': 'MSFT',
#         'NVIDIA': 'NVDA',
#         'Tesla': 'TSLA',
#         'BlackRock': 'BLK',
#         'LVMH': 'MC.PA',
#         'Samsung Electronics': '005930.KS',
#         'Amazon': 'AMZN',
#         'Alphabet': 'GOOGL',
#         'Meta Platforms': 'META',
#         'Berkshire Hathaway': 'BRK.B',
#         'Visa': 'V',
#         'JPMorgan Chase': 'JPM',
#         'Johnson & Johnson': 'JNJ',
#         'UnitedHealth Group': 'UNH',
#         'Procter & Gamble': 'PG',
#         'Mastercard': 'MA',
#         'Eli Lilly': 'LLY',
#         'Home Depot': 'HD',
#         'Walmart': 'WMT',
#         'Bank of America': 'BAC',
#         'Disney': 'DIS',
#         'Intel': 'INTC',
#         'Oracle': 'ORCL'
#     }


# # --- 3. Initialize all three agents with shared model config ---
# def init_agents():
#     # base_model = OpenAIChat(id="gpt-3.5-turbo-1106")
# #     base_model = Gemini(
# #     id="gemini-1.5-flash",
# #     name="Gemini",
# #     provider="Google",
# api_key=*****
# #     max_output_tokens=512,       # limit output
# #     temperature=0.7,
# # )
#     # base_model = DeepSeekChat(
#     #     id="deepseek-v1",
#     #     name="DeepSeek"
#     #     # agar DeepSeekChat ko api_key ya koi config chahiye to yahan pass karo
#     # )
#     groq_key = st.secrets["GROQ_API_KEY"]

#     base_model=Groq(
#         id="llama-3.3-70b-versatile",
#         api_key=groq_key,
#         # temperature=0.7,           # optional
#         # max_output_tokens=1024,    # optional
#     )
#     web_agent = Agent(
#         name="Web Agent",
#         role="Search the web for information",
#         model=base_model,
#         tools=[DuckDuckGo()],
#         instructions=[
#             "Summarize and always include sources (links)",
#             "Provide precise and clear information on the topic"
#         ],
#         show_tools_calls=True,
#         markdown=True,
#     )
#     finance_agent = Agent(
#         name="Finance Agent",
#         model=base_model,
#         tools=[YFinanceTools(
#             stock_price=True,
#             analyst_recommendations=True,
#             stock_fundamentals=True,
#             company_news=True,
#         )],
#         instructions=[
#             "Use tables to display data, not text",
#             "Be concise and to the point ",
#             "Always include sources (links)",
#         ],
#         show_tools_calls=True,
#         markdown=True,
#     )
#     final_agent = Agent(
#         name="Final Answer Agent",
#         model=base_model,
#         instructions=[
#             "Summarize clearly and precisely",
#             "Always include sources (links)",
#             "Use tables to display data"
#         ],
#         markdown=True,
#     )
#     return web_agent, finance_agent, final_agent

# def send_input():
#     st.session_state.send_input=True
# # --- 4. Get user inputs (tickers + custom query) from sidebar & main UI ---
# def get_user_inputs(companies: dict):
#     st.sidebar.header("Select Companies")
#     # dynamic checkboxes
#     selected = [
#         ticker for name, ticker in companies.items()
#         if st.sidebar.checkbox(name, value=False)
#     ]

#     tickers_input = st.text_input(
#         "Tickers (comma-separated):",
#         value=", ".join(selected),
#         key="tickers_input"
#     )
#     user_query = st.text_input("Your Query:", key="user_query")
#     return tickers_input, user_query,  


# # --- 5. Query each agent and return their raw responses ---
# def fetch_agent_responses(tickers, combined_payload, web_agent, finance_agent):
#     # 5a. Web search
#     with st.spinner("🔎 Searching the web..."):
#         web_resp = web_agent.run(f"Explain {combined_payload} with web sources")
#     # 5b. Finance data
#     with st.spinner("💹 Fetching finance data..."):
#         finance_resp = finance_agent.run(f"Get financial details for {combined_payload}")
#     return web_resp, finance_resp


# # --- 6. Combine context & get final summarized answer ---
# def summarize_final_answer(combined_payload, web_resp, finance_resp, final_agent):
#     prompt = f"""
# User Query: {combined_payload}

# Web Information:
# {web_resp.get_content_as_string()}

# Finance Information:
# {finance_resp.get_content_as_string()}

# Now, based on this information, give a final summarized answer in a clear, friendly format.
# """
#     with st.spinner("✍️ Generating final answer..."):
#         final_resp = final_agent.run(prompt)
#     return final_resp.get_content_as_string()


# # --- 7. Main app flow ---
# def main():
#     # Load config & agents
#     load_config()
#     companies = get_companies()
#     web_agent, finance_agent, final_agent = init_agents()

#     # Page title
#     st.set_page_config(page_title="MarketBot | Stock & News Insights", layout="wide")
#     st.title("📊 Stock Insights & Real-Time Market Answers")
#     chat_container = st.container()
#     if "messages" not in st.session_state:
#         st.session_state.messages = []
#     # Inputs
#     tickers_input, user_query = get_user_inputs(companies)
#     if st.button("Send") or send_input():
#         # Validate tickers
#         tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
#         if not tickers:
#             st.error("Please select or enter at least one ticker.")
#             return
#         if not user_query.strip():
#             st.error("Please enter your query.")
#             return

#         # Combine for consistent payload
#         combined = f"{tickers}.{user_query}"

#         # Fetch intermediate results
#         web_resp, finance_resp = fetch_agent_responses(tickers, combined, web_agent, finance_agent)

#         # Get final summary
#         final_answer = summarize_final_answer(combined, web_resp, finance_resp, final_agent)

#         # Display only the final result
#         st.markdown(final_answer)


# if __name__ == "__main__":
# #     main()
import os
from dotenv import load_dotenv
import streamlit as st
from phi.tools.duckduckgo import DuckDuckGo
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.model.groq import Groq
import openai

# --- Config & Session Setup ---
def load_config():
    load_dotenv(os.getenv('DOTENV_PATH', '.env'))
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    st.set_page_config(page_title="MarketBot | Stock & News Insights", layout="wide")

def init_session():
    defaults = {
        'selected_companies': [], 'tickers_input': "", 'user_query': "",
        'last_response': None, 'input_key': 0
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def get_companies():
    return {
        'Apple Inc.': 'AAPL', 'Microsoft Corp.': 'MSFT', 'NVIDIA': 'NVDA',
        'Tesla': 'TSLA', 'BlackRock': 'BLK', 'LVMH': 'MC.PA', 'Samsung Electronics': '005930.KS',
        'Amazon': 'AMZN', 'Alphabet': 'GOOGL', 'Meta Platforms': 'META',
        'Berkshire Hathaway': 'BRK.B', 'Visa': 'V', 'JPMorgan Chase': 'JPM',
        'Johnson & Johnson': 'JNJ', 'UnitedHealth Group': 'UNH', 'Procter & Gamble': 'PG',
        'Mastercard': 'MA', 'Eli Lilly': 'LLY', 'Home Depot': 'HD', 'Walmart': 'WMT',
        'Bank of America': 'BAC', 'Disney': 'DIS', 'Intel': 'INTC', 'Oracle': 'ORCL'
    }

# --- Agent Setup ---
def init_agents():
    model = Groq(id="llama-3.3-70b-versatile", api_key=st.secrets["GROQ_API_KEY"])

    web_agent = Agent(
        name="Web Agent", role="Search the web",
        model=model, tools=[DuckDuckGo()], markdown=True, show_tools_calls=True,
        instructions=["Summarize with sources"]
    )

    finance_agent = Agent(
        name="Finance Agent", model=model, tools=[YFinanceTools(
            stock_price=True, analyst_recommendations=True,
            stock_fundamentals=True, company_news=True
        )], markdown=True, show_tools_calls=True,
        instructions=["Use tables, be concise, include sources"]
    )

    final_agent = Agent(
        name="Final Agent", model=model, markdown=True,
        instructions=["Summarize with sources, use tables"]
    )

    return web_agent, finance_agent, final_agent

# --- Reset UI ---
def reset_inputs():
    for key in ['selected_companies', 'tickers_input', 'user_query']:
        st.session_state[key] = "" if isinstance(st.session_state[key], str) else []
    st.session_state.input_key += 1

# --- Final Answer Logic ---
def summarize_final_answer(query, web_resp, finance_resp, agent):
    prompt = f"""
User Query:\n{query}
\nWeb Info:\n{web_resp.get_content_as_string()}
\nFinance Info:\n{finance_resp.get_content_as_string()}
\nInstructions:
- Clear summary with sources
- Use tables for financial data
- Don't skip details due to length
"""
    with st.spinner("✍️ Generating summary..."):
        return agent.run(prompt).get_content_as_string()

# --- UI ---
def sidebar_ui(companies):
    st.sidebar.header("Select Companies")
    for name in companies:
        key = f"company_{name}_{st.session_state.input_key}"
        if st.sidebar.checkbox(name, value=(name in st.session_state.selected_companies), key=key):
            if name not in st.session_state.selected_companies:
                st.session_state.selected_companies.append(name)
        else:
            if name in st.session_state.selected_companies:
                st.session_state.selected_companies.remove(name)

    tickers = st.sidebar.text_input(
        "OR enter tickers (comma-separated):",
        value=st.session_state.tickers_input,
        key=f"tickers_input_{st.session_state.input_key}"
    )
    st.session_state.tickers_input = tickers

    selected = [companies[n] for n in st.session_state.selected_companies]
    custom = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    all_tickers = list(set(selected + custom))

    st.sidebar.subheader("Current Tickers")
    if all_tickers:
        st.sidebar.write(", ".join(all_tickers))
    else:
        st.sidebar.warning("No tickers selected")

    if st.sidebar.button("Clear Inputs"):
        reset_inputs()
        st.session_state.last_response = None
        st.rerun()

    return all_tickers

def main():
    load_config()
    init_session()
    companies = get_companies()
    web_agent, finance_agent, final_agent = init_agents()

    st.title("📊 Stock Insights & Market Answers")
    all_tickers = sidebar_ui(companies)

    user_query = st.text_input(
        "Enter your question:", value=st.session_state.user_query,
        key=f"query_input_{st.session_state.input_key}"
    )
    st.session_state.user_query = user_query

    if st.button("Submit", key=f"submit_{st.session_state.input_key}"):
        if not all_tickers:
            st.error("Select or enter at least one ticker.")
            return
        if not user_query.strip():
            st.error("Enter your query.")
            return

        combined = f"{', '.join(all_tickers)} - {user_query}"
        with st.spinner("🔍 Searching web..."):
            web_resp = web_agent.run(f"Explain {combined} with web sources")
        with st.spinner("💹 Fetching financial data..."):
            fin_resp = finance_agent.run(f"Get financial details for {combined}")
        final = summarize_final_answer(combined, web_resp, fin_resp, final_agent)

        st.session_state.last_response = final
        reset_inputs()
        st.rerun()

    if st.session_state.last_response:
        st.subheader("Latest Response")
        st.markdown(st.session_state.last_response, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

#     main()

