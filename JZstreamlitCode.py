import altair as alt
import pandas as pd
import streamlit as st

data_task1 = pd.read_csv('data_cut.csv')
data_task1['date'] = pd.to_datetime(data_task1['date'])
data_task1['year_month'] = data_task1['date'].dt.to_period('M')
data_task1['year_month'] = data_task1['year_month'].astype(str).str.replace('-', '').astype(int)
data_task1['day'] = data_task1['date'].dt.day
data_task1['day'] = data_task1['day'].astype(int)

default_ym = 202003
ym_slider = st.slider('Year_Month', min(data_task1['year_month']), max(data_task1['year_month']), value=default_ym)

combined_data = data_task1
combined_data['states'] = pd.read_csv('data_cut2.csv')['state']
combined_data['deaths'] = pd.read_csv('data_cut5_ddeath.csv')['deaths']
combined_data['num_below_poverty'] = pd.read_csv('data_cut2.csv')['num_below_poverty']
combined_data['overcrowding'] = pd.read_csv('data_cut2.csv')['overcrowding']
combined_data['median_household_income'] = pd.read_csv('data_cut3_mhi.csv')['median_household_income']
combined_data['average_number_of_physically_unhealthy_days'] = pd.read_csv('data_cut3_unhds.csv')['average_number_of_physically_unhealthy_days']
combined_data['average_number_of_mentally_unhealthy_days'] = pd.read_csv('data_cut3_unhds.csv')['average_number_of_mentally_unhealthy_days']
combined_data['fips'] = pd.read_csv('data_cut4.csv')['fips']
combined_data['percent_adults_with_obesity'] = pd.read_csv('data_cut4.csv')['percent_adults_with_obesity']

state_selectbox = st.selectbox(
    "State", tuple(combined_data["states"].unique()))

state_filtered = combined_data[combined_data['states'] == state_selectbox]

default_counties = ['Snohomish', 'King', 'Ferry', 'Pierce', 'Franklin', 'Adams', 'Yakima', 'Cowlitz']
county_multiselect = st.multiselect(
    "County", combined_data["county"].unique(), default=default_counties) 

filtered_data_task1 = combined_data[(combined_data['year_month'] == ym_slider) &
                   (combined_data['states'] == state_selectbox) &
                   (combined_data['county'].isin(county_multiselect))]

line_chart = alt.Chart(filtered_data_task1).mark_line(point = True).encode(
    x = 'day:N',
    y = 'cases:Q',
    color = 'county:N'
).properties(
    title='Daily New COVID-19 Cases'
)
st.altair_chart(line_chart, use_container_width=True)

line_chart2 = alt.Chart(filtered_data_task1).mark_line(point = True).encode(
    x = 'day:N',
    y = 'deaths:Q',
    color = 'county:N'
).properties(
    title='Daily New COVID-19 Deaths'
)
st.altair_chart(line_chart2, use_container_width=True)

filtered_data_task1_2 = combined_data[(combined_data['states'] == state_selectbox) &
                   (combined_data['county'].isin(county_multiselect))]

bar_chart = alt.Chart(filtered_data_task1_2).mark_bar().encode(
    x = 'year_month:N',
    y = 'num_deaths:Q',
    color = 'county:N'
).properties(
    title='Total COVID-19 Deaths by Months'
)
st.altair_chart(bar_chart, use_container_width=True)

state_selectbox2 = st.selectbox(
    "Select State", tuple(combined_data["states"].unique()))

filtered_data_task2 = combined_data[(combined_data['states'] == state_selectbox2)]

scatter1 = alt.Chart(filtered_data_task2).mark_point(color='red').encode(
    x='num_below_poverty:Q',
    y='num_deaths:Q',
)
scatter2 = alt.Chart(filtered_data_task2).mark_point(color='navy').encode(
    x='median_household_income:Q',
    y='num_deaths:Q'
)
combined_scatter_chart = alt.hconcat(scatter1, scatter2)
combined_scatter_chart = combined_scatter_chart.properties(
    title='Number of Deaths vs. Poverty-related Conditions'
)
st.altair_chart(combined_scatter_chart, use_container_width=True)


scatter3 = alt.Chart(filtered_data_task2).mark_point(color='teal').encode(
    x='overcrowding:Q',
    y='num_deaths:Q',
)
scatter4 = alt.Chart(filtered_data_task2).mark_point(color='mediumvioletred').encode(
    x='average_number_of_physically_unhealthy_days:Q',
    y='num_deaths:Q'
)
scatter5 = alt.Chart(filtered_data_task2).mark_point(color='orange').encode(
    x='average_number_of_mentally_unhealthy_days:Q',
    y='num_deaths:Q',
)
combined_scatter_chart2 = alt.hconcat(scatter3, scatter4, scatter5).properties(
    title='Number of Deaths vs. Living Conditions '
)
st.altair_chart(combined_scatter_chart2, use_container_width=True)

### https://jinrui93-706finaljz-streamlitapp-eb9syk.streamlit.app/

