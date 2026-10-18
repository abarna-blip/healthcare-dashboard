import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Healthcare Dashboard", layout="wide")
st.title("🏥 Healthcare Dashboard")

try:
    df = pd.read_csv("Healthcare_dataset.csv")
    st.dataframe(df.head())
    
    cols = df.select_dtypes(include='number').columns
    if len(cols) > 0:
        c = st.selectbox("Chart column", cols)
        fig = px.histogram(df, x=c)
        st.plotly_chart(fig)
except Exception as e:
    st.error(f"Error: {e}")
    st.info("Please upload Healthcare_dataset.csv also")
