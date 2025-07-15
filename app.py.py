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
import openai
from phi.model.groq import Groq
# --- 1. Load configuration ---
def load_config():
    load_dotenv(os.getenv('DOTENV_PATH', '.env'))
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    st.set_page_config(page_title="MarketBot | Stock & News Insights", layout="wide")

# --- 2. Define available companies ---
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

# --- 3. Initialize agents ---
def init_agents():
    
    groq_key = st.secrets["GROQ_API_KEY"]      
    
    base_model=Groq(id="llama-3.3-70b-versatile",
                api_key=groq_key,         # temperature=0.7,           # optional     
                # max_output_tokens=1024,    # optional  
               )
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
            "Be concise and to the point ",
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

# --- 4. Reset all inputs ---
def reset_inputs():
    st.session_state.selected_companies = []
    st.session_state.tickers_input = ""
    st.session_state.user_query = ""
    st.session_state.input_key += 1  # Force UI refresh

# --- 5. Main app flow ---
def main():
    # Initialize session state
    if 'selected_companies' not in st.session_state:
        st.session_state.selected_companies = []
    if 'tickers_input' not in st.session_state:
        st.session_state.tickers_input = ""
    if 'user_query' not in st.session_state:
        st.session_state.user_query = ""
    if 'last_response' not in st.session_state:
        st.session_state.last_response = None
    if 'input_key' not in st.session_state:
        st.session_state.input_key = 0

    # Load config
    load_config()
    
    # Page title
    st.title("📊 Stock Insights & Real-Time Market Answers")
    
    # Initialize agents
    companies = get_companies()
    web_agent, finance_agent, final_agent = init_agents()

    # --- Sidebar: Company Selection ---
    st.sidebar.header("Select Companies")
    
    # 1. COMPANY SELECTION (Checkbox approach)
    st.sidebar.subheader("Select from popular companies:")
    selected_from_list = []
    for name in companies:
        # Create a unique key using input_key to force refresh
        key = f"company_{name}_{st.session_state.input_key}"
        if st.sidebar.checkbox(name, value=(name in st.session_state.selected_companies), key=key):
            if name not in st.session_state.selected_companies:
                st.session_state.selected_companies.append(name)
        else:
            if name in st.session_state.selected_companies:
                st.session_state.selected_companies.remove(name)
    
    # 2. MANUAL TICKER INPUT
    st.sidebar.subheader("OR Enter Tickers Manually")
    # Create a unique key using input_key to force refresh
    tickers_input = st.sidebar.text_input(
        "Tickers (comma separated):", 
        value=st.session_state.tickers_input,
        key=f"tickers_input_{st.session_state.input_key}"
    )
    if tickers_input != st.session_state.tickers_input:
        st.session_state.tickers_input = tickers_input
    
    # Combine selected and custom tickers
    selected_tickers = [companies[name] for name in st.session_state.selected_companies]
    custom_tickers_list = [t.strip().upper() for t in st.session_state.tickers_input.split(",") if t.strip()]
    all_tickers = list(set(selected_tickers + custom_tickers_list))
    
    # Display current selection
    st.sidebar.subheader("Current Tickers")
    if all_tickers:
        st.sidebar.write(", ".join(all_tickers))
    else:
        st.sidebar.warning("No tickers selected")
    
    # Clear button in sidebar
    if st.sidebar.button("Clear All Inputs"):
        reset_inputs()
        st.session_state.last_response = None
        st.rerun()
    
    # --- Main Area: Query Input ---
    st.subheader("Ask a Question")
    # Create a unique key using input_key to force refresh
    user_query = st.text_input(
        "Enter your question about the selected companies:", 
        value=st.session_state.user_query,
        key=f"query_input_{st.session_state.input_key}"
    )
    if user_query != st.session_state.user_query:
        st.session_state.user_query = user_query
    
    # Submit button
    if st.button("Submit Query", key=f"submit_{st.session_state.input_key}"):
        # Validate inputs
        if not all_tickers:
            st.error("Please select at least one company or enter a ticker.")
            return
            
        if not st.session_state.user_query.strip():
            st.error("Please enter your query.")
            return
        
        # Combine for consistent payload
        combined = f"{', '.join(all_tickers)} - {st.session_state.user_query}"
        
        # Fetch agent responses
        with st.spinner("🔍 Processing your query..."):
            # Web search
            web_resp = web_agent.run(f"Explain {combined} with web sources")
        with st.spinner("💹 Fetching finance data..."):
            # Finance data
            finance_resp = finance_agent.run(f"Get financial details for {combined}")
            # Get final summary
            final_answer = summarize_final_answer(combined, web_resp, finance_resp, final_agent)
        
        st.session_state.last_response = final_answer
        
        # Reset inputs after successful response
        reset_inputs()
        st.rerun()
    
    # Display last response
    if st.session_state.last_response:
        st.subheader("Latest Response")
        st.markdown(st.session_state.last_response, unsafe_allow_html=True)

# --- 6. Generate final answer ---
def summarize_final_answer(combined_payload, web_resp, finance_resp, final_agent):
    prompt = f"""
## User Query: 
{combined_payload}

## Web Information:
{web_resp.get_content_as_string()}

## Finance Information:
{finance_resp.get_content_as_string()}

## Instructions:
Based on the information above, provide a final summarized answer that:
- Is clear, precise, and well-structured
- Includes relevant sources links not code functions
- Uses tables for financial data presentation
- Addresses all aspects of the user's query
- write complete message don't skip response due to length response
"""
    with st.spinner("✍️ Generating final answer..."):
        final_resp = final_agent.run(prompt)
    return final_resp.get_content_as_string()

if __name__ == "__main__":
    main()
