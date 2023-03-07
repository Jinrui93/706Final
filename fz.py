import altair as alt
import pandas as pd
import streamlit as st

df = pd.read_csv('data.csv')
df1 = pd.read_csv('data_month.csv')

# df['date'] = pd.to_datetime(df['date'])
# df['year_month'] = df['date'].dt.to_period('M')
# df['year_month'] = df['year_month'].astype(str).str.replace('-', '').astype(int)
# df['day'] = df['date'].dt.day
# df['day'] = df['day'].astype(int)

default_ym = 202003
ym_slider = st.slider('Year_Month', min(df1['new_date']), max(df1['new_date']), value=default_ym)

st.write("## Association between Vaccination Rate and Number of Covid Cases")

# state_filtered = df[df['state'] == state_selectbox]

df5 = df1[df1['new_date'] == ym_slider]

scatter = alt.Chart(df5).mark_point().encode(
    x='percent_insured:Q',
    y='cases_k:Q',
    tooltip=['state','percent_insured','cases_k']
).properties(
    title='Vaccination Rate and COVID-19 Cases'
)

st.altair_chart(scatter, use_container_width=True)

scatter1 = alt.Chart(df5).mark_point().encode(
    x='percent_insured:Q',
    y='deaths_k:Q',
    tooltip=['state','percent_insured','deaths_k']
).properties(
    title='Vaccination Rate and COVID-19 Deaths'
)

st.altair_chart(scatter1, use_container_width=True)