import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load cleaned dataset
df = pd.read_csv('C:/Users/Lavanya/Desktop/MSIS Notes/Python/CA2/HRA Dataset/HRAnalytics_cleaned.csv')

# Title
st.title("📊👥 HR Analytics Dashboard")

# ---Sidebar and Cascading filters---
st.sidebar.header("Filter Employee Data")

# Cascading Filter for Department 
selected_dept = st.sidebar.selectbox("Select Department", options=['All'] + sorted(df['Department'].unique().tolist()))

# Cascading Filter for Job Role
if selected_dept != 'All':
    job_roles = df[df['Department'] == selected_dept]['JobRole'].unique()
else:
    job_roles = df['JobRole'].unique()
selected_role = st.sidebar.selectbox("Select Job Role", options=['All'] + sorted(job_roles.tolist()))

# Dynamic slider for Age
age_slider = st.sidebar.slider("Select Age Range", int(df['Age'].min()), int(df['Age'].max()),(18, 60))

# Filter data
df_filtered = df.copy()
if selected_dept != 'All':
    df_filtered = df_filtered[df_filtered['Department'] == selected_dept]
if selected_role != 'All':
    df_filtered = df_filtered[df_filtered['JobRole'] == selected_role]
final_df = df_filtered[(df_filtered['Age'] >= age_slider[0]) & (df_filtered['Age'] <= age_slider[1])]

# Main Dashboard - Summary metrics
st.markdown("### Summary Metrics")
col1, col2 = st.columns(2)
col1.metric("Total Employees", len(final_df))
col2.metric("Avg Monthly Income", f"${int(final_df['MonthlyIncome'].mean()):,}")

# 1. Bar Chart - Employee Distribution by Education Field
edu_count = df_filtered['EducationField'].value_counts().reset_index()
edu_count.columns = ['EducationField', 'Count']
fig1 = px.bar(
    edu_count,
    x='EducationField', 
    y='Count',
    color='EducationField',
    title='Bar Chart of Employee Distribution by Education Field'
)
st.plotly_chart(fig1)


# 2. Scatter Plot - Income vs Age by Attrition
fig2 = px.scatter(
    df_filtered, 
    x='Age', 
    y='MonthlyIncome', 
    color='Attrition', 
    hover_data=['JobRole'],
    title='Scatter Plot of Income vs Age Colored by Attrition'
)
st.plotly_chart(fig2)

# 3. Line Chart - Average Income by Age
avg_income_by_age = df_filtered.groupby('Age')['MonthlyIncome'].mean().reset_index()
fig3 = px.line(
    avg_income_by_age, 
    x='Age', 
    y='MonthlyIncome',
    title='Line Chart of Average Monthly Income by Age'
)
st.plotly_chart(fig3)

# 4. Conditional Heatmap 
if st.checkbox("Show Heatmap (Conditional Feature)"):
    st.subheader("Correlation Heatmap: Satisfaction and Performance")
    heatmap_cols = ['JobSatisfaction', 'EnvironmentSatisfaction', 'WorkLifeBalance', 'RelationshipSatisfaction', 'PerformanceRating']
    corr_matrix = df_filtered[heatmap_cols].corr()

    fig4, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig4)

# 5. Interactive Table
st.subheader("📋Interactive Table of Employee Data")
display_cols = ['EmpID', 'Age', 'JobRole', 'Department', 'MonthlyIncome', 'Attrition']
if all(col in df_filtered.columns for col in display_cols):
    st.dataframe(df_filtered[display_cols].sort_values(by='MonthlyIncome', ascending=False))
else:
    st.warning("One or more columns for the table are missing.")

st.markdown("### 🔗 Connected Visualizations")

# Pie Chart - Attrition distribution
attrition_counts = df_filtered['Attrition'].value_counts().reset_index()
attrition_counts.columns = ['Attrition', 'Count']
fig5 = px.pie(
    attrition_counts,
    names='Attrition',
    values='Count',
    title='Pie Chart of Attrition Rate Distribution '
)
st.plotly_chart(fig5)

# Bar Chart - Average Income by JobRole (Filtered)
income_by_role = df_filtered.groupby('JobRole')['MonthlyIncome'].mean().reset_index()
fig6 = px.bar(
    income_by_role,
    x='JobRole',
    y='MonthlyIncome',
    color='JobRole',
    title='Bar Chart of Average Monthly Income by Job Role (Filtered)'
)
st.plotly_chart(fig6)
