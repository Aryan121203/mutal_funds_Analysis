import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# ✅ Set Streamlit page configuration FIRST
st.set_page_config(page_title="Mutual Funds Explorer", layout="wide")

# 🎯 Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("mutual_funds_india.csv")  # Adjust path as needed
    df.columns = df.columns.str.replace(" ", "")  # Clean column names
    return df

df = load_data()

# 🎨 Sidebar for user input
st.sidebar.header("🔍 Filter Mutual Funds")
categories = sorted(df.category.unique())
selected_category = st.sidebar.selectbox("📂 Select Category", categories)

filtered_df = df[df.category == selected_category]
amcs = sorted(filtered_df.AMC_name.unique())
selected_amc = st.sidebar.selectbox("🏢 Select AMC Name", amcs)

final_df = filtered_df[filtered_df.AMC_name == selected_amc]

# 🧾 Page Title and Description
st.title("📈 Mutual Funds 1-Year Return Explorer")
st.markdown(f"""
### 🏷️ **Category**: `{selected_category}`  
### 🏦 **AMC**: `{selected_amc}`  
""")

# 📊 Plotting
if not final_df.empty:
    final_df = final_df.sort_values(by="return_1yr", ascending=False)  # Sort by return

    fig, ax = plt.subplots(figsize=(18, 8))
    sb.barplot(x=final_df.MutualFundName, y=final_df.return_1yr, palette='rocket', ax=ax)

    # Add labels and formatting
    ax.set_title("📊 1-Year Returns of Mutual Funds", fontsize=16, weight='bold')
    ax.set_xlabel("Mutual Fund Name", fontsize=12)
    ax.set_ylabel("1-Year Return (%)", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

    # Annotate bars
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.1f}%', 
                    (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom', fontsize=8)

    plt.tight_layout()
    st.pyplot(fig)

else:
    st.warning("⚠️ No data available for the selected combination.")

# 🧭 Footer
st.markdown("---")
st.markdown("🔁 Use the **sidebar** to explore different categories and AMCs.")
st.markdown("📊 Built with ❤️ using Streamlit, Pandas, Seaborn, and Matplotlib.")
