import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config ---
st.set_page_config(page_title="Healthcare Analytics", page_icon="🏥", layout="wide")

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("healthcare_dataset.csv")
    return df

df = load_data()

# --- Header ---
st.title("🏥 Healthcare Analytics Dashboard")
st.markdown(f"Analyzing **{df.shape[0]:,}** patient records")
st.divider()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
gender_filter = st.sidebar.multiselect("Gender", options=df['Gender'].unique(), default=df['Gender'].unique())
condition_filter = st.sidebar.multiselect("Medical Condition", options=df['Medical Condition'].unique(), default=df['Medical Condition'].unique())
hospital_filter = st.sidebar.multiselect("Hospital", options=df['Hospital'].unique(), default=df['Hospital'].unique())

filtered_df = df[
    (df['Gender'].isin(gender_filter)) &
    (df['Medical Condition'].isin(condition_filter)) &
    (df['Hospital'].isin(hospital_filter))
]

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients", f"{len(filtered_df):,}")
col2.metric("Avg Age", f"{filtered_df['Age'].mean():.1f}")
col3.metric("Avg Billing", f"${filtered_df['Billing Amount'].mean():,.0f}")
col4.metric("Hospitals", filtered_df['Hospital'].nunique())

st.divider()

# --- Charts ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Medical Condition Distribution")
    fig1 = px.pie(filtered_df, names='Medical Condition', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("Gender vs Billing Amount")
    fig2 = px.box(filtered_df, x='Gender', y='Billing Amount', color='Gender')
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    st.subheader("Age Distribution")
    fig3 = px.histogram(filtered_df, x='Age', nbins=30, color='Gender', barmode='overlay')
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("Admission Type Count")
    fig4 = px.bar(filtered_df['Admission Type'].value_counts().reset_index(), x='Admission Type', y='count', color='Admission Type')
    st.plotly_chart(fig4, use_container_width=True)

st.subheader("Hospital vs Total Billing")
hospital_billing = filtered_df.groupby('Hospital')['Billing Amount'].sum().reset_index().sort_values('Billing Amount', ascending=False)
fig5 = px.bar(hospital_billing, x='Hospital', y='Billing Amount', color='Hospital')
st.plotly_chart(fig5, use_container_width=True)

# --- Data Table ---
st.subheader("📋 Detailed Data")
st.dataframe(filtered_df, use_container_width=True, height=400)

st.download_button("📥 Download Filtered Data", filtered_df.to_csv(index=False), "filtered_healthcare.csv", "text/csv")
