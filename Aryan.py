import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ✅ Set Streamlit config first!
st.set_page_config(page_title="📊 Mutual Funds Explorer", layout="wide")

# 🎯 Load and cache data
@st.cache_data
def load_data():
    df = pd.read_csv("mutual_funds_india.csv")
    df.columns = df.columns.str.replace(" ", "")  # Clean column names
    return df

df = load_data()

# 🖼️ Page Title & Description
st.markdown("""
# 💼 Mutual Funds Explorer - India
Analyze and compare **1-Year Returns** across different **categories** and **AMCs**.

Use the **sidebar** to filter, explore, and visualize mutual fund performance 🔍📈
""")

# 🎛️ Sidebar Controls
st.sidebar.header("🔍 Filter Funds")
categories = sorted(df.category.unique())
selected_category = st.sidebar.selectbox("📂 Select Category", categories)

filtered_df = df[df.category == selected_category]
amcs = sorted(filtered_df.AMC_name.unique())
selected_amc = st.sidebar.selectbox("🏢 Select AMC", amcs)

final_df = filtered_df[filtered_df.AMC_name == selected_amc]

# 🧾 Show Selection
st.markdown(f"### 📂 Category: `{selected_category}` | 🏦 AMC: `{selected_amc}`")

# 📊 Plot
if not final_df.empty:
    # Sort by return for better visuals
    final_df = final_df.sort_values(by="return_1yr", ascending=False)

    # Create two columns
    col1, col2 = st.columns([4, 1])

    # Main Plot
    with col1:
        st.subheader("📈 1-Year Return Comparison")
        fig, ax = plt.subplots(figsize=(18, 8))
        barplot = sns.barplot(
            data=final_df,
            x="MutualFundName",
            y="return_1yr",
            palette="flare",
            ax=ax
        )
        ax.set_title("Top Mutual Funds by 1-Year Return", fontsize=16, fontweight='bold')
        ax.set_xlabel("Mutual Fund", fontsize=12)
        ax.set_ylabel("Return (%)", fontsize=12)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

        # Annotate bars
        for p in ax.patches:
            val = p.get_height()
            ax.annotate(f"{val:.1f}%", 
                        (p.get_x() + p.get_width() / 2., val), 
                        ha='center', va='bottom', fontsize=8, color='black')

        plt.tight_layout()
        st.pyplot(fig)

    # 📁 Download Filtered Data
    with col2:
        st.subheader("⬇️ Download")
        csv = final_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{selected_amc}_funds.csv",
            mime='text/csv'
        )

else:
    st.warning("⚠️ No data found for the selected combination.")

# Footer
st.markdown("---")
st.markdown("""
🧠 **Tip**: Use the sidebar to change filters and explore different funds.

Made with ❤️ using Streamlit, Pandas, Seaborn, and Matplotlib.
""")
