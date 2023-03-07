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

st.write("## Association between Insurance Rate and Number of Covid Cases")

# state_filtered = df[df['state'] == state_selectbox]

df5 = df1[df1['new_date'] == ym_slider]

scatter = alt.Chart(df5).mark_circle().encode(
    x=alt.X('percent_insured:Q', scale=alt.Scale(domain=[75, 100]), title = 'Percent Insured'),
    y=alt.Y('cases_k:Q', title = 'Number of Cases (thousands)'),
    tooltip=['state','percent_insured','cases_k']
).properties(
    title='Insured Rate and COVID-19 Cases'
).interactive()

scatter1 = alt.Chart(df5).mark_circle().encode(
    x=alt.X('percent_insured:Q', scale=alt.Scale(domain=[75, 100]), title = 'Percent Insured'),
    y=alt.Y('deaths_k:Q', title = 'Number of Deaths (thousands)'),
    tooltip=['state','percent_insured','deaths_k']
).properties(
    title='Insured Rate and COVID-19 Deaths'
).interactive()

col1, col2 = st.columns(2)
with col1:
    st.altair_chart(scatter, use_container_width=True)

with col2:
    st.altair_chart(scatter1, use_container_width=True)

