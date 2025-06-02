import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("mutual_funds_india.csv")  # Update path if needed
    df.columns = df.columns.str.replace(" ", "")
    return df

df = load_data()

# Page configuration
st.set_page_config(page_title="Mutual Funds Explorer", layout="wide")

# Sidebar
st.sidebar.header("🔍 Filter Mutual Funds")
categories = sorted(df.category.unique())
selected_category = st.sidebar.selectbox("📂 Select Category", categories)

filtered_df = df[df.category == selected_category]
amcs = sorted(filtered_df.AMC_name.unique())
selected_amc = st.sidebar.selectbox("🏢 Select AMC Name", amcs)

final_df = filtered_df[filtered_df.AMC_name == selected_amc]

# Main Title
st.title("📈 Mutual Funds 1-Year Return Explorer")
st.markdown(f"""
### 🏷️ **Category**: `{selected_category}`  
### 🏦 **AMC**: `{selected_amc}`  
""")

# Sort by return if needed
final_df = final_df.sort_values(by="return_1yr", ascending=False)

# Plotting
if not final_df.empty:
    fig, ax = plt.subplots(figsize=(18, 8))
    barplot = sb.barplot(x=final_df.MutualFundName, y=final_df.return_1yr, palette='rocket', ax=ax)
    
    ax.set_title("📊 1-Year Returns of Mutual Funds", fontsize=16, weight='bold')
    ax.set_xlabel("Mutual Fund Name", fontsize=12)
    ax.set_ylabel("1-Year Return (%)", fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    
    # Add value annotations
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{height:.1f}%', (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom', fontsize=8, color='black')

    plt.tight_layout()
    st.pyplot(fig)
else:
    st.warning("No data available for the selected combination.")

# Footer
st.markdown("---")
st.markdown("✅ **Tip**: Use the sidebar to explore other categories and AMCs.")
