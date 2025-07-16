# 📊 MarketBot - AI-Powered Stock & News Insights

![Python](https://img.shields.io/badge/python-3.10%2B-blue) ![Streamlit](https://img.shields.io/badge/streamlit-%E2%9C%93-brightgreen) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

MarketBot is a modern **Streamlit** web application that leverages **Phi SDK** and **Groq’s LLaMA 3** model to deliver real-time financial data and curated web search insights. Get concise, data-driven answers to your stock market questions across top global companies.

---

## 🚀 Key Features

- **Real-Time Finance**: Live stock prices, company fundamentals, analyst ratings, and news (via YFinanceTools).
- **Web Summaries**: DuckDuckGo-powered searches with source citations.
- **Multi-Agent Architecture**: Separate agents for web search, financial data, and final summarization.
- **Flexible Input**: Select companies via checkboxes or enter tickers manually.
- **Structured Output**: Markdown formatting and tables for clarity.
- **Streamlined UI**: Sidebar-driven controls with dynamic input clearing.

---

## 🛠️ Tech Stack

| Component         | Technology                    |
| ----------------- | ----------------------------- |
| Frontend          | Streamlit                     |
| Agents & Tools    | Phi SDK, DuckDuckGo, YFinanceTools |
| LLM               | Groq LLaMA 3.3 (70B Versatile) |
| Language          | Python 3.10+                  |

---

## 📦 Installation & Setup

1. **Clone repository**
   ```bash
   git clone https://github.com/your-username/marketbot.git
   cd marketbot
   ```
2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure secrets**
   - Create `~/.streamlit/secrets.toml`:
     ```toml
     OPENAI_API_KEY = "<your_openai_api_key>"
     GROQ_API_KEY      = "<your_groq_api_key>"
     ```
   - Or use a `.env` file for local testing:
     ```ini
     DOTENV_PATH=.env
     ```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧠 How It Works

1. **Initialization**: Load API keys and configure Groq model.
2. **Company Selection**: Choose from popular tickers or enter custom ones.
3. **User Query**: Provide a question in the main panel.
4. **Web Agent**: Fetch and summarize search results with citations.
5. **Finance Agent**: Retrieve and tabulate live financial data.
6. **Final Agent**: Combine insights into a concise, well-structured markdown summary.

---

## 🎯 Use Cases

- Compare stock performance (e.g., Apple vs NVIDIA).
- Latest news on leading companies (e.g., Tesla updates).
- Investment guidance based on fundamentals and market sentiment.

---

## 🔧 Roadmap

- [ ] Interactive chart visualizations
- [ ] Multi-company comparative reports
- [ ] Deployment to Streamlit Cloud or Docker container
- [ ] CI/CD integration and automated tests

---

## 📄 License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 🙋‍♂️ Contributing & Support

Feel free to open issues or submit pull requests. For questions or feedback, reach out at **your.email@example.com**.

