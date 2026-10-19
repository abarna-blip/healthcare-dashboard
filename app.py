import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Healthcare Dashboard", layout="wide")
st.title("🏥 Healthcare Data Analysis Website")
st.markdown("### 1060 Patients Data - Exploration and Visualization")

st.sidebar.header("Settings")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    try:
        df = pd.read_csv("healthcare_1060.csv")
        st.sidebar.info("Loaded default file: healthcare_1060.csv")
    except:
        st.warning("Please upload your CSV file from the sidebar!")
        st.stop()

st.header("1. Data Overview")
st.write(f"**Total Rows:** {df.shape[0]} | **Total Columns:** {df.shape[1]}")
st.dataframe(df.head(20))

col1, col2, col3 = st.columns(3)
col1.metric("Total Patients", len(df))
col2.metric("Average Age", round(df["Age"].mean(), 1))
col3.metric("Total Billing Amount", f"${df['Billing Amount'].sum():,.0f}")

st.header("2. Data Exploration")
if st.checkbox("Show Data Structure"):
    st.write(df.dtypes)
if st.checkbox("Show Summary Statistics"):
    st.write(df.describe())
if st.checkbox("Show Missing Values"):
    st.write(df.isnull().sum())

st.header("3. Data Visualization")
tab1, tab2, tab3, tab4 = st.tabs(["Billing", "Age", "Conditions", "Correlation"])

with tab1:
    st.subheader("Billing Amount Distribution")
    fig = px.histogram(df, x="Billing Amount", nbins=30, color="Gender", title="Billing Distribution")
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Billing by Medical Condition")
    fig2 = px.box(df, x="Medical Condition", y="Billing Amount", color="Medical Condition")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Age Distribution")
    fig3 = px.histogram(df, x="Age", nbins=20, title="Age of Patients")
    st.plotly_chart(fig3, use_container_width=True)
    st.subheader("Age vs Billing Amount")
    fig4 = px.scatter(df, x="Age", y="Billing Amount", color="Gender", hover_data=["Medical Condition"])
    st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.subheader("Medical Condition Count")
    condition_counts = df["Medical Condition"].value_counts().reset_index()
    condition_counts.columns = ['Medical Condition', 'count']
    fig5 = px.bar(condition_counts, x='Medical Condition', y='count', title="Patients per Condition")
    st.plotly_chart(fig5, use_container_width=True)
    st.subheader("Gender Distribution")
    fig6 = px.pie(df, names="Gender", title="Gender Ratio")
    st.plotly_chart(fig6, use_container_width=True)

with tab4:
    st.subheader("Correlation Heatmap")
    numeric_cols = df.select_dtypes(include=np.number).columns
    corr = df[numeric_cols].corr()
    fig7, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig7)

st.header("4. Export Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download Data as CSV", csv, "healthcare_export.csv", "text/csv")

st.success("Website Ready! All Features Working ✅")
