import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("mutual_funds_india.csv")  # Adjust path if needed
    df.columns = df.columns.str.replace(" ", "")
    return df

df = load_data()

st.title("Mutual Funds in India - 1 Year Returns")

# Category selection
categories = df.category.unique()
selected_category = st.selectbox("Select Category", categories)

# Filter by selected category
filtered_df = df[df.category == selected_category]

# AMC selection
amcs = filtered_df.AMC_name.unique()
selected_amc = st.selectbox("Select AMC Name", amcs)

# Filter by selected AMC
final_df = filtered_df[filtered_df.AMC_name == selected_amc]

# Show the mutual fund names and their 1-year returns
st.subheader(f"1-Year Returns for Mutual Funds in {selected_amc} under {selected_category}")
if not final_df.empty:
    plt.figure(figsize=(12, 6))
    plot = sb.barplot(x=final_df.MutualFundName, y=final_df.return_1yr, palette='hot')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)
else:
    st.write("No data available for the selected category and AMC.")
