import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ Set Streamlit Page Config
st.set_page_config(
    page_title="📊 Mutual Fund Explorer India",
    layout="wide",
    page_icon="📈"
)

# ========== 💾 Load and Cache Data ==========
@st.cache_data
def load_data():
    df = pd.read_csv("mutual_funds_india.csv")
    df.columns = df.columns.str.replace(" ", "")
    return df

df = load_data()

# ========== 🎨 Custom CSS Styling ==========
st.markdown("""
    <style>
        .main {background-color: #f9f9f9;}
        h1, h2, h3 {
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton>button {
            color: white;
            background-color: #4CAF50;
            border: None;
            padding: 0.6em 1.2em;
            border-radius: 8px;
        }
        .stDownloadButton>button {
            background-color: #0072B2;
            color: white;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ========== 👋 Hero Section ==========
with st.container():
    st.markdown("""
        <div style='text-align: center; padding: 2rem 1rem 1rem;'>
            <h1 style='font-size: 3rem; color: #2E8B57;'>📈 Mutual Fund Explorer India</h1>
            <p style='font-size: 1.2rem; color: #555;'>Analyze and compare mutual funds based on 1-year returns — Interactive, Fast & Beautiful</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ========== 🎛 Sidebar Filters ==========
with st.sidebar:
    st.header("🔍 Filter Your Funds")
    categories = sorted(df.category.unique())
    selected_category = st.selectbox("📂 Select Fund Category", categories)

    filtered_df = df[df.category == selected_category]
    amcs = sorted(filtered_df.AMC_name.unique())
    selected_amc = st.selectbox("🏢 Select AMC", amcs)

    st.markdown("---")
    st.caption("📊 Made with ❤️ using Streamlit")

# Final filtered dataframe
final_df = filtered_df[filtered_df.AMC_name == selected_amc].sort_values(by="return_1yr", ascending=False)

# ========== 📊 Chart Section ==========
with st.container():
    st.subheader(f"📊 Top Mutual Funds by 1-Year Return\n({selected_category} → {selected_amc})")

    if not final_df.empty:
        fig = px.bar(
            final_df,
            x='MutualFundName',
            y='return_1yr',
            text='return_1yr',
            color='return_1yr',
            color_continuous_scale='Viridis',
            title="",
            labels={'return_1yr': '1-Year Return (%)'},
            height=600
        )
        fig.update_layout(
            xaxis_tickangle=45,
            xaxis_title=None,
            yaxis_title='1-Year Return (%)',
            plot_bgcolor='white',
            margin=dict(l=40, r=40, t=20, b=80)
        )
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ No data found for this selection.")

# ========== 🧾 Data Table ==========
with st.expander("🔎 View Filtered Table"):
    st.dataframe(final_df, use_container_width=True, hide_index=True)

# ========== 📥 Download Section ==========
with st.container():
    st.markdown("### 📥 Download Filtered Data as CSV")
    st.markdown("Download the filtered mutual fund data for your own analysis.")
    download_csv = final_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV File",
        data=download_csv,
        file_name=f"{selected_amc}_{selected_category}_returns.csv",
        mime="text/csv"
    )

# ========== 📌 Footer ==========
st.markdown("""
    <hr style="margin-top: 3rem; margin-bottom: 1rem;">

    <div style='text-align: center; font-size: 0.9rem; color: gray;'>
        Built with ❤️ by <b>Your Name</b> | Powered by Streamlit + Plotly + Pandas
    </div>
""", unsafe_allow_html=True)
