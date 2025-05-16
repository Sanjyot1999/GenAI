import streamlit as st
from data_loader import load_laptop_data
from retrieval import setup_retrieval, query_index
from llm_services import ask_groq
from config import filter_data, save_chat_history, load_chat_history
import base64
import pandas as pd

st.set_page_config(
    page_title="💻 GenAI Laptop Recommender",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    dark_mode = st.checkbox("🌙 Enable Dark Mode")
    currency = st.selectbox("💱 Select Currency", ["INR", "USD"])
    currency_symbol = "₹" if currency == "INR" else "$"

custom_css = f"""
<style>
body, .main {{
    background-color: {"#121212" if dark_mode else "#f9fafd"};
    color: {"#ffffff" if dark_mode else "#000000"};
    font-weight: 700;
    font-size: 18px;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 8px 15px rgba(0,0,0,0.1);
}}
.header {{
    background: linear-gradient(90deg, {"#0b2340, #1a396f" if dark_mode else "#1e3c72, #2a5298"});
    padding: 1rem 2rem;
    border-radius: 10px;
    color: white;
    font-size: 32px;
    font-weight: 900;
    margin-bottom: 1.5rem;
    text-align: center;
    letter-spacing: 1.2px;
}}

/* Text input styling */
.stTextInput > div > div > input {{
    background-color: {"#333" if dark_mode else "white"};
    color: {"#ffffff" if dark_mode else "#000000"};
    border: 1px solid {"#555" if dark_mode else "#ccc"};
    border-radius: 6px;
    padding: 0.6rem;
    font-weight: 700;
    font-size: 18px;
}}

/* Button styling */
.stButton > button {{
    background-color: #1e3c72;
    color: white;
    font-weight: 700;
    font-size: 18px;
    padding: 0.6rem 1.2rem;
    border-radius: 6px;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-top: 1.7rem;
}}
.stButton > button:hover {{
    background-color: #16325c;
}}

/* Sidebar labels and inputs */
[data-testid="stSidebar"] {{
    background-color: {"#1a1a1a" if dark_mode else "transparent"} !important;
    padding: 1rem;
    border-radius: 10px;
}}
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] div[role="radiogroup"] > label,
[data-testid="stSidebar"] .css-1f0twzl,
[data-testid="stSidebar"] span[data-baseweb="tag"] {{
    color: {"#ffffff" if dark_mode else "#000000"} !important;
    font-weight: 700;
    font-size: 18px;
}}

/* Tabs: normal tab text color depends on mode, size and bold */
.css-1v0mbdj.e16nr0p33 > div[role="tablist"] > button {{
    color: {"#ffffff" if dark_mode else "#000000"};
    font-weight: 700;
    font-size: 20px;
    padding: 12px 16px;
}}

/* Tabs: selected tab text color is red always */
.css-1v0mbdj.e16nr0p33 > div[role="tablist"] > button[aria-selected="true"] {{
    color: red !important;
    font-weight: 900 !important;
    font-size: 22px !important;
    border-bottom: 3px solid red !important;
}}

/* Text input label color */
.css-1kyxreq.egzxvld1 {{
    color: {"#ffffff" if dark_mode else "#000000"} !important;
    font-weight: 700;
    font-size: 18px;
}}

/* Dataframe container text size and bold */
.stDataFrame > div > div > div > div {{
    font-weight: 700 !important;
    font-size: 16px !important;
    color: {"#ffffff" if dark_mode else "#000000"} !important;
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown('<div class="header">💻 GenAI Laptop Recommender 🚀</div>', unsafe_allow_html=True)

tabs = st.tabs(["🔍 Search", "📜 History", "💬 Feedback"])

with tabs[0]:
    df = load_laptop_data()

    if "Description" not in df.columns:
        st.error("The dataset must contain a 'Description' column.")
    else:
        index, embeddings = setup_retrieval(df, description_column="Description")

        with st.sidebar:
            st.header("📊 Filters")
            min_price = st.number_input(f"Min Price ({currency_symbol})", value=0, step=1000)
            max_price = st.number_input(f"Max Price ({currency_symbol})", value=int(df['Price'].max()), step=1000)
            brands = st.multiselect("Select Brand", df['Brand'].unique())

        col1, col2 = st.columns([4, 1])
        with col1:
            user_query = st.text_input(
                "What laptop are you looking for?",
                placeholder="Example: lightweight laptop for programming under 60k",
            )
        with col2:
            submit = st.button("🔍 Search", key="search_button")

        if submit:
            if not user_query.strip():
                st.warning("Please enter a laptop requirement to proceed.")
            else:
                filtered_df = filter_data(df, min_price, max_price, brands)
                results = query_index(index, user_query, filtered_df)

                if results.empty:
                    st.warning("No matching laptops found. Try refining your query.")
                else:
                    conversion_rate = 0.012
                    if 'Price' in results.columns:
                        if currency == "USD":
                            results[f"Price ({currency_symbol})"] = results["Price"].apply(lambda x: f"{currency_symbol}{x * conversion_rate:,.2f}")
                        else:
                            results[f"Price ({currency_symbol})"] = results["Price"].apply(lambda x: f"{currency_symbol}{x:,.0f}")
                        results = results.drop(columns=["Price"])

                    st.markdown(f'<h3 style="color:#1e3c72; font-weight: 900; font-size: 22px;">🔍 Top Matches (Prices in {currency}):</h3>', unsafe_allow_html=True)
                    st.dataframe(results)

                    groq_prompt = f"""
You are a laptop advisor. The user wants:

\"\"\"{user_query}\"\"\"

Here are the top matched laptops:
{results.to_string(index=False)}

Suggest the most suitable laptop with reasoning.
"""
                    st.markdown('<h3 style="color:#2a5298; font-weight: 900; font-size: 22px;">🤖 AI Suggestion:</h3>', unsafe_allow_html=True)
                    with st.spinner("Generating AI recommendation..."):
                        response = ask_groq(groq_prompt)
                    st.write(response)
                    save_chat_history(user_query, response)

        if 'results' in locals() and not results.empty:
            st.markdown("### 📁 Export Recommendations")
            export_df = results.copy()
            csv = export_df.to_csv(index=False).encode('utf-8')
            b64_csv = base64.b64encode(csv).decode()
            href_csv = f'<a href="data:file/csv;base64,{b64_csv}" download="recommendations.csv">Download CSV</a>'
            st.markdown(href_csv, unsafe_allow_html=True)

with tabs[1]:
    st.markdown("## 📜 Chat History")
    history_df = load_chat_history()
    if history_df.empty:
        st.info("No chat history yet.")
    else:
        st.dataframe(history_df)

with tabs[2]:
    st.markdown("## 💬 Feedback")
    feedback = st.text_area("Share your thoughts or suggestions")
    if st.button("Submit Feedback"):
        st.success("Thanks for your feedback!")
