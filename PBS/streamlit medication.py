import streamlit as st
import pandas as pd
import plotly.express as px

# Load your dataset
df = pd.read_csv("C:/Users/belin/PycharmProjects/Population Health/PBS/PBS_all_fin_year.csv")
df.columns = df.columns.str.strip()  # Clean up column names
df['FY24 All'] = df['FY24 All'].replace(',', '', regex=True).astype(int)
df['FY24 change'] = df['FY24 change'].replace(',', '', regex=True).astype(int)

# Streamlit App Layout
st.title("PBS Dashboard")

# Slicers (Filters)
medication_type = st.selectbox("Select Medication Type:", ["All"] + list(df['Medication_Type'].unique()))
gccsa_name = st.selectbox("Select GCCSA Name:", ["All"] + list(df['GCCSA_NAME_2021'].unique()))
state = st.selectbox("Select State:", ["All"] + list(df['State'].unique()))

# Filter data based on selections
filtered_df = df.copy()
if medication_type != "All":
    filtered_df = filtered_df[filtered_df['Medication_Type'] == medication_type]
if gccsa_name != "All":
    filtered_df = filtered_df[filtered_df['GCCSA_NAME_2021'] == gccsa_name]
if state != "All":
    filtered_df = filtered_df[filtered_df['State'] == state]

# Total PBS Scripts by GCCSA
fig1 = px.bar(
    filtered_df.groupby('GCCSA_NAME_2021')['FY24 All'].sum().reset_index(),
    x='GCCSA_NAME_2021', y='FY24 All',
    title="Total PBS Scripts by GCCSA"
)
st.plotly_chart(fig1)

# Change in PBS Scripts by GCCSA
fig2 = px.bar(
    filtered_df.groupby('GCCSA_NAME_2021')['FY24 change'].sum().reset_index(),
    x='GCCSA_NAME_2021', y='FY24 change',
    title="Change in PBS Scripts by GCCSA"
)
st.plotly_chart(fig2)

# Total PBS Scripts by LGA
fig3 = px.bar(
    filtered_df.groupby('LGA_Name')['FY24 All'].sum().reset_index(),
    x='LGA_Name', y='FY24 All',
    title="Total PBS Scripts by LGA"
)
st.plotly_chart(fig3)

# Change in PBS Scripts by LGA
fig4 = px.bar(
    filtered_df.groupby('LGA_Name')['FY24 change'].sum().reset_index(),
    x='LGA_Name', y='FY24 change',
    title="Change in PBS Scripts by LGA"
)
st.plotly_chart(fig4)

# Total PBS Scripts by Medication Type
fig5 = px.bar(
    filtered_df.groupby('Medication_Type')['FY24 All'].sum().reset_index(),
    x='Medication_Type', y='FY24 All',
    title="Total PBS Scripts by Medication Type"
)
st.plotly_chart(fig5)

# Change in PBS Scripts by Medication Type
fig6 = px.bar(
    filtered_df.groupby('Medication_Type')['FY24 change'].sum().reset_index(),
    x='Medication_Type', y='FY24 change',
    title="Change in PBS Scripts by Medication Type"
)
st.plotly_chart(fig6)
