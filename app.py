
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Healthcare Dashboard", layout="wide")
st.title("🏥 Healthcare Dashboard")

try:
    df = pd.read_csv("healthcare_dataset.csv")
    st.success(f"Loaded {df.shape[0]} rows!")
    
    st.write("### Preview")
    st.dataframe(df.head())
    
    st.write("### Dashboard")
    col1, col2 = st.columns(2)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    if numeric_cols:
        c = st.selectbox("Choose column for chart", numeric_cols)
        fig = px.histogram(df, x=c)
        st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Error: {e}")
