import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Streamlit Config
st.set_page_config(
    page_title="📊 Mutual Fund Explorer India",
    layout="wide",
    page_icon="📈"
)

# 🔄 Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("mutual_funds_india.csv")
    df.columns = df.columns.str.replace(" ", "")
    return df

df = load_data()

# 🌑 Dark Theme + Flipkart Accent CSS
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #121212;
            color: #e0e0e0;
        }
        .block-container {
            padding-top: 2rem;
        }
        h1, h2, h3 {
            font-family: 'Segoe UI', sans-serif;
            color: #e0e0e0;
        }
        .stButton > button {
            background-color: #2874f0;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            transition: 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #1a5fd6;
        }
        .stDownloadButton > button {
            background-color: #ff9f00;
            color: white;
            font-weight: 600;
            border-radius: 8px;
        }
        .stDownloadButton > button:hover {
            background-color: #fb8c00;
        }
        .fund-card {
            background: rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .fund-card:hover {
            box-shadow: 0 6px 30px rgba(0, 0, 0, 0.6);
        }
        .dataframe th {
            background-color: #2874f0 !important;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# 🧭 Hero Section
with st.container():
    st.markdown("""
        <div style='text-align: center; padding: 2rem 1rem 0;'>
            <h1 style='font-size: 2.8rem; color: #2874f0;'>📈 Mutual Fund Explorer India</h1>
            <p style='font-size: 1.2rem; color: #bbb;'>Dark Mode • Flipkart-Inspired • Performance Dashboard</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 🎛 Sidebar Filters
with st.sidebar:
    st.header("🔍 Filter Your Funds")
    category = st.selectbox("📂 Choose Fund Category", sorted(df.category.unique()))
    amcs = sorted(df[df.category == category].AMC_name.unique())
    amc = st.selectbox("🏢 Select AMC", amcs)

    st.markdown("---")
    st.caption("🌙 Dark mode powered by Streamlit + Plotly")

# 📦 Filtered Data
filtered_df = df[(df.category == category) & (df.AMC_name == amc)].sort_values(by="return_1yr", ascending=False)

# 📊 Plotly Bar Chart
with st.container():
    st.subheader(f"📊 1-Year Return for `{category}` → `{amc}`")
    if not filtered_df.empty:
        fig = px.bar(
            filtered_df,
            x='MutualFundName',
            y='return_1yr',
            text='return_1yr',
            color='return_1yr',
            color_continuous_scale='icefire',  # vibrant dark mode colors
            height=600,
            labels={'return_1yr': '1-Year Return (%)'}
        )
        fig.update_layout(
            xaxis_tickangle=45,
            xaxis_title=None,
            yaxis_title='Return (%)',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            margin=dict(l=40, r=40, t=20, b=80)
        )
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No mutual funds available for this combination.")

# 🧾 Top 5 Fund Cards
if not filtered_df.empty:
    st.markdown("### 💎 Top 5 Funds (By 1-Year Return)")
    top5 = filtered_df.head(5)
    for i, row in top5.iterrows():
        st.markdown(f"""
        <div class='fund-card'>
            <h4 style='margin: 0; color: #64b5f6;'>{row['MutualFundName']}</h4>
            <p style='margin: 0.2rem 0;'><b>1Y Return:</b> {row['return_1yr']}%</p>
            <p style='margin: 0.2rem 0;'><b>Category:</b> {row['category']}</p>
            <p style='margin: 0.2rem 0;'><b>AMC:</b> {row['AMC_name']}</p>
        </div>
        """, unsafe_allow_html=True)

# 📋 Table View
with st.expander("📋 View Full Table"):
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# 📥 Download Button
with st.container():
    st.markdown("### 📥 Download Filtered Data")
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name=f"{amc}_{category}_returns.csv",
        mime="text/csv"
    )

# 📌 Footer
st.markdown("""
    <hr style="margin-top: 3rem; margin-bottom: 1rem;">
    <div style='text-align: center; font-size: 0.9rem; color: #888;'>
        Built with 💙 by <b>Your Name</b> | Inspired by Flipkart | Dark Mode Dashboard
    </div>
""", unsafe_allow_html=True)
