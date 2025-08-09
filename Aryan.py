import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ==================== ✅ Streamlit Page Config ====================
st.set_page_config(
    page_title="📊 Mutual Fund Explorer",
    layout="wide",
    page_icon="📈"
)

# ==================== 🎨 Custom CSS - Premium Dark Transparent Theme ====================
st.markdown("""
    <style>
        /* Entire app background */
        .stApp {
            background: linear-gradient(135deg, rgba(18,18,18,0.95), rgba(28,28,28,0.95));
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }

        /* Transparent containers with glass effect */
        .block-container {
            background: rgba(30, 30, 30, 0.4);
            backdrop-filter: blur(8px);
            border-radius: 15px;
            padding: 1rem;
        }

        /* Sidebar - dark glass look */
        section[data-testid="stSidebar"] {
            background: rgba(20, 20, 20, 0.8);
            backdrop-filter: blur(10px);
            border-right: 2px solid #4CAF50;
        }

        /* Headings */
        h1, h2, h3, h4 {
            color: #4CAF50;
            font-weight: 700;
        }

        /* Buttons */
        .stDownloadButton button, .stButton button {
            background: linear-gradient(90deg, #4CAF50, #2E7D32);
            color: white;
            font-weight: bold;
            border-radius: 8px;
            border: none;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
            transition: 0.3s;
        }

        .stDownloadButton button:hover, .stButton button:hover {
            background: linear-gradient(90deg, #66BB6A, #388E3C);
            transform: scale(1.05);
        }

        /* Selectbox Labels */
        label {
            color: #b2dfdb !important;
            font-weight: bold;
        }

        /* Table Styling */
        .stDataFrame {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }

        /* Footer */
        footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)

# ==================== 📥 Load & Cache Data ====================
@st.cache_data
def load_data():
    df = pd.read_csv("mutual_funds_india.csv")
    df.columns = df.columns.str.replace(" ", "")  # Remove spaces in column names
    return df

df = load_data()

# ==================== 👋 Hero Section ====================
with st.container():
    st.markdown("""
        <div style='text-align: center; padding: 2rem 1rem 1rem;'>
            <h1 style='font-size: 3rem;'>📈 Mutual Fund Explorer India</h1>
            <p style='font-size: 1.2rem; color: #e0e0e0;'>Compare returns by category and AMC — Interactive, Beautiful & Fast</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border: 1px solid #4CAF50;'>", unsafe_allow_html=True)

# ==================== 🎛 Sidebar Filters ====================
with st.sidebar:
    st.header("🔍 Filter Your Funds")
    categories = sorted(df.category.unique())
    selected_category = st.selectbox("📂 Select Fund Category", categories)

    filtered_df = df[df.category == selected_category]
    amcs = sorted(filtered_df.AMC_name.unique())
    selected_amc = st.selectbox("🏢 Select AMC", amcs)

    st.markdown("---")
    st.caption("Made with ❤️ using Streamlit")

# ==================== 📊 Final Filtered Data ====================
final_df = filtered_df[filtered_df.AMC_name == selected_amc]
final_df = final_df.sort_values(by="return_1yr", ascending=False)

# ==================== 📊 Chart Section ====================
with st.container():
    st.subheader(f"📊 1-Year Return: `{selected_category}` → `{selected_amc}`")
    if not final_df.empty:
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.set_style("white")
        sns.barplot(data=final_df, x="MutualFundName", y="return_1yr", palette="crest", ax=ax)

        ax.set_facecolor("none")  # transparent plot bg
        fig.patch.set_alpha(0)    # transparent figure bg
        ax.set_title("Top Mutual Funds by 1-Year Return", fontsize=18, fontweight='bold', color="white")
        ax.set_xlabel("")
        ax.set_ylabel("Return (%)", fontsize=14, color="white")
        ax.tick_params(colors='white')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10, color='white')

        # Annotate bars
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{height:.1f}%', 
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=9, color='white')

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("⚠️ No data found for this selection.")

# ==================== ⬇️ Download Section ====================
with st.container():
    st.markdown("### 📥 Download Filtered Data")
    st.markdown("You can download this table for your own analysis or presentation.")
    download_csv = final_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download CSV",
        data=download_csv,
        file_name=f"{selected_amc}_{selected_category}_returns.csv",
        mime="text/csv"
    )

# ==================== 📌 Footer ====================
st.markdown("""
<hr style="margin-top: 3rem; border: 1px solid #4CAF50;">
<div style='text-align: center; font-size: 0.9rem; color: gray;'>
    Built with ❤️ by <b>Your Name</b> | Powered by Streamlit, Pandas & Seaborn
</div>
""", unsafe_allow_html=True)
