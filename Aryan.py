import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ✅ Set config first
st.set_page_config(
    page_title="📊 Mutual Fund Explorer",
    layout="wide",
    page_icon="📈"
)

# Load and cache data
@st.cache_data
def load_data():
    df = pd.read_csv("mutual_funds_india.csv")
    df.columns = df.columns.str.replace(" ", "")  # Remove spaces in column names
    return df

df = load_data()

# ===================== 👋 Hero Section ======================
with st.container():
    st.markdown("""
        <div style='text-align: center; padding: 2rem 1rem 1rem;'>
            <h1 style='font-size: 3rem; color: #4CAF50;'>📈 Mutual Fund Explorer India</h1>
            <p style='font-size: 1.2rem; color: gray;'>Compare returns by category and AMC — Interactive, Beautiful & Fast</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ===================== 🎛 Sidebar Filters =====================
with st.sidebar:
    st.header("🔍 Filter Your Funds")
    categories = sorted(df.category.unique())
    selected_category = st.selectbox("📂 Select Fund Category", categories)

    filtered_df = df[df.category == selected_category]
    amcs = sorted(filtered_df.AMC_name.unique())
    selected_amc = st.selectbox("🏢 Select AMC", amcs)

    st.markdown("---")
    st.caption("Made with ❤️ using Streamlit")

# Filtered result
final_df = filtered_df[filtered_df.AMC_name == selected_amc]
final_df = final_df.sort_values(by="return_1yr", ascending=False)

# ===================== 📊 Chart Section =====================
with st.container():
    st.subheader(f"📊 1-Year Return: `{selected_category}` → `{selected_amc}`")
    if not final_df.empty:
        fig, ax = plt.subplots(figsize=(16, 8))
        sns.barplot(data=final_df, x="MutualFundName", y="return_1yr", palette="Spectral", ax=ax)

        ax.set_title("Top Mutual Funds by 1-Year Return", fontsize=18, fontweight='bold')
        ax.set_xlabel("")
        ax.set_ylabel("Return (%)", fontsize=14)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=10)

        # Annotate bars
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{height:.1f}%', 
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=9, color='black')

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("⚠️ No data found for this selection.")

# ===================== ⬇️ Download Button =====================
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

# ===================== 📌 Footer =====================
st.markdown("""
<hr style="margin-top: 3rem;">

<div style='text-align: center; font-size: 0.9rem; color: gray;'>
    Built with ❤️ by <b>Your Name</b> | Powered by Streamlit, Pandas, and Seaborn
</div>
""", unsafe_allow_html=True)
