import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Healthcare Analytics", page_icon="🏥", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("healthcare_dataset.csv")
    # Clean column names - remove extra spaces
    df.columns = df.columns.str.strip()
    return df

df = load_data()

st.title("🏥 Healthcare Analytics Dashboard")
st.markdown(f"**Total Records:** {len(df):,} | **Columns:** {', '.join(df.columns)}")
st.divider()

# --- Show columns for debug ---
# st.write("Columns:", df.columns.tolist())

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")

# Find correct column names (case-insensitive safe)
def get_col(name_options):
    for col in df.columns:
        for opt in name_options:
            if opt.lower() in col.lower():
                return col
    return None

gender_col = get_col(['Gender', 'Sex'])
condition_col = get_col(['Medical Condition', 'Condition', 'Diagnosis'])
hospital_col = get_col(['Hospital', 'Hospital Name'])
age_col = get_col(['Age'])
billing_col = get_col(['Billing', 'Amount', 'Cost'])
admission_col = get_col(['Admission Type', 'Admission'])

# Filters
filtered_df = df.copy()
if gender_col:
    genders = st.sidebar.multiselect("Gender", df[gender_col].unique(), default=df[gender_col].unique())
    filtered_df = filtered_df[filtered_df[gender_col].isin(genders)]
if condition_col:
    conditions = st.sidebar.multiselect("Medical Condition", df[condition_col].unique(), default=df[condition_col].unique())
    filtered_df = filtered_df[filtered_df[condition_col].isin(conditions)]

# --- KPIs ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Patients", len(filtered_df))
if age_col:
    c2.metric("Avg Age", f"{filtered_df[age_col].mean():.1f}")
if billing_col:
    # clean billing if it has $ sign
    filtered_df[billing_col] = pd.to_numeric(filtered_df[billing_col].astype(str).str.replace('$','').str.replace(',',''), errors='coerce')
    c3.metric("Avg Billing", f"${filtered_df[billing_col].mean():,.0f}")
if hospital_col:
    c4.metric("Hospitals", filtered_df[hospital_col].nunique())

st.divider()

# --- CHARTS - Guaranteed to show ---
col1, col2 = st.columns(2)

with col1:
    if condition_col:
        st.subheader("Medical Condition")
        fig = px.pie(filtered_df, names=condition_col, hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    elif gender_col:
        st.subheader("Gender Distribution")
        fig = px.pie(filtered_df, names=gender_col, hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

with col2:
    if gender_col and billing_col:
        st.subheader("Billing by Gender")
        fig2 = px.box(filtered_df, x=gender_col, y=billing_col, color=gender_col)
        st.plotly_chart(fig2, use_container_width=True)
    elif age_col:
        st.subheader("Age Distribution")
        fig2 = px.histogram(filtered_df, x=age_col, nbins=20)
        st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    if age_col:
        st.subheader("Age Histogram")
        fig3 = px.histogram(filtered_df, x=age_col, nbins=30, color=gender_col if gender_col else None)
        st.plotly_chart(fig3, use_container_width=True)

with col4:
    if admission_col:
        st.subheader("Admission Type")
        adm_counts = filtered_df[admission_col].value_counts().reset_index()
        fig4 = px.bar(adm_counts, x=admission_col, y='count', color=admission_col)
        st.plotly_chart(fig4, use_container_width=True)

if hospital_col and billing_col:
    st.subheader("Hospital vs Billing")
    hb = filtered_df.groupby(hospital_col)[billing_col].sum().reset_index().sort_values(billing_col, ascending=False)
    fig5 = px.bar(hb, x=hospital_col, y=billing_col, color=hospital_col)
    st.plotly_chart(fig5, use_container_width=True)

# Table
st.subheader("📋 Data Preview")
st.dataframe(filtered_df.head(100), use_container_width=True)
st.download_button("📥 Download Data", filtered_df.to_csv(index=False), "filtered_data.csv")

    
