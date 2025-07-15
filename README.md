# Stock & Query App

This Streamlit-based application allows users to fetch web information and financial data for selected companies, then combines and summarizes the results using OpenAI's GPT-3.5 model.

---

## Features

* **Web Search Agent**: Queries the web via DuckDuckGo for context and sources.
* **Finance Agent**: Retrieves stock prices, fundamentals, analyst recommendations, and company news using YFinance tools, displayed in tables.
* **Final Summarizer**: Merges web and finance data into a concise final answer.
* **Modular Structure**: Organized into separate modules for configuration, agents, inputs, processing, and the main app.

---

## File Structure

```bash
├── config.py          # Load .env settings & company list
├── agents.py          # Initializes web, finance, and final GPT agents
├── inputs.py          # Streamlit UI input functions
├── processing.py      # Agent calls and summarization logic
├── app.py             # Main Streamlit application runner
├── .env               # Environment variables (OPENAI_API_KEY)
└── README.md          # Project documentation
```

---

## Prerequisites

* Python 3.8+
* A valid OpenAI API key
* Internet connection for web search and stock data

---

## Installation

1. Clone this repository:

   ```bash
   git clone <repo-url>
   cd <repo-directory>
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file at the project root and add your OpenAI key:

   ```env
   OPENAI_API_KEY=sk-...
   ```

---

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

1. In the sidebar, select companies or enter tickers manually.
2. Enter your custom query in the input box.
3. Click **Send** to fetch web and finance data.
4. View the combined summary in the main panel.

---

## Customization

* **Add/Remove Companies**: Modify the `get_companies()` dictionary in `config.py`.
* **Adjust Agent Settings**: Tweak instructions or tools in `init_agents()` within `agents.py`.

---

## License

This project is licensed under the MIT License. Feel free to fork and modify!
