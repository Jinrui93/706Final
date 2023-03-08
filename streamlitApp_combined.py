import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data
import datetime

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


@st.cache_data
def load_data():
    df = pd.read_csv('df_state_level.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df


var_names = ['date', 'state', 'cases', 'deaths', 'total_population', 'num_deaths', 'state-code',
             'mean_temp', 'precipitation', 'wind_speed',
             'percent_adults_with_obesity', 'percent_smokers', 'percent_insufficient_sleep']

st.write("## COVID-19 and Weather Conditions")
df = load_data()

df = df.dropna(subset=['total_population'])
df = df[df['total_population']>0]
df["Rate"] = (df["cases"] / df["total_population"]) * 100000
df["Rate"] = df["Rate"].round(3)
var_names.append("Rate")

# map_date_range = st.slider("Date Range", min_value=df['date'].min().to_pydatetime(), max_value=df['date'].max().to_pydatetime(),
#                            value=(datetime.datetime(2020, 5, 1), datetime.datetime(2020, 7, 1)))
map_date_range = st.slider("Date",
                           min_value=df['date'].min().to_pydatetime(),
                           max_value=df['date'].max().to_pydatetime(),
                           value=(datetime.datetime(2020, 8, 1)))
subset = df[df["date"] == map_date_range]

map_temp_range = st.slider("Temperate",
                           value=(float(df['mean_temp'].min()),
                                  float(df['mean_temp'].max())),
                           step=5.0)
subset = subset[subset["mean_temp"] >= map_temp_range[0]]
subset = subset[subset["mean_temp"] <= map_temp_range[1]]

map_precip_range = st.slider("Precipitation",
                             value=(float(df['precipitation'].min()),
                                    float(df['precipitation'].max())))
subset = subset[subset["precipitation"] >= map_precip_range[0]]
subset = subset[subset["precipitation"] <= map_precip_range[1]]

map_wind_range = st.slider("Wind Speed", value=(float(df['wind_speed'].min()), float(df['wind_speed'].max())))
subset = subset[subset["wind_speed"] >= map_wind_range[0]]
subset = subset[subset["wind_speed"] <= map_wind_range[1]]

alt.data_transformers.enable('default', max_rows=None)
states = alt.topo_feature(data.us_10m.url, 'states')
color_scale = alt.Scale(
    domain=(subset['Rate'].min(), subset['Rate'].max()),
    scheme='orangered'
)

if subset.shape[0] > 0:

    layer_deaths = alt.Chart(states).mark_geoshape(
        stroke='white'
    ).encode(
        color=alt.Color('Rate:Q', scale=color_scale, legend=alt.Legend(title='Infection Rate per 100k')),
        tooltip=['state:N', 'Rate:Q']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(subset, 'state-code', var_names)
    ).project(
        type='albersUsa'
    )
    chart = alt.layer(
        alt.Chart(states).mark_geoshape(
            fill='lightgray',
            stroke='white'
        ),
        layer_deaths
    ).properties(
        width=850,
        height=660
    ).properties(
    title='Infection Rate per 100k'
)

    chart
else:
    st.write("No data available for the selected range. Please try different range.")
    states = alt.topo_feature(data.us_10m.url, 'states')
    chart1 = alt.Chart(states).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).project('albersUsa').properties(
        width=850,
        height=660
    ).properties(
    title='Infection Rate per 100k'
)
    chart1


st.write("##  COVID-19 and Health Indicators")
df = load_data()

df = df.dropna(subset=['total_population'])
df = df[df['total_population'] > 0]

df["infection_rate"] = (df["cases"] / df["total_population"]) * 100000
df["infection_rate"] = df["infection_rate"].round(2)

states = ['Washington','Georgia', 'California', 'Illinois', 'Florida']
selected_states = st.multiselect("States", options = list(df["state"].unique()), default = states)
subset = df[df["state"].isin(selected_states)]

date_range = st.slider("Date Range",
                           min_value=df['date'].min().to_pydatetime(),
                           max_value=df['date'].max().to_pydatetime(),
                           value=(datetime.datetime(2020, 1, 21),
                                  datetime.datetime(2020, 7, 1)))
subset = subset[subset["date"] >= date_range[0]]
subset = subset[subset["date"] <= date_range[1]]

# Infection rate per 100k - Obesity
obesity = alt.Chart(subset).mark_circle(size=60).encode(
    x=alt.X("percent_adults_with_obesity:Q",
            title="Obesity Percentage",
            scale=alt.Scale(domain=(min(subset['percent_adults_with_obesity']), max(subset['percent_adults_with_obesity'])))),
    y=alt.Y("infection_rate:Q", title="Infection rate per 100k"),
    color=alt.Color("state:N", title="States"),
    tooltip=['percent_adults_with_obesity', 'infection_rate'],
    opacity=alt.value(0.6),
).properties(
    title='Obesity'
).properties(
        width=900,
        height=300
    )
st.altair_chart(obesity, use_container_width=True)

# Infection rate per 100k - percent_smokers
smoker = alt.Chart(subset).mark_circle(size=60).encode(
    x=alt.X("percent_smokers:Q",
            title="Smoker Percentage",
            scale=alt.Scale(domain=(min(subset['percent_smokers']), max(subset['percent_smokers'])))),
    y=alt.Y("infection_rate:Q", title="Infection rate per 100k"),
    color=alt.Color("state:N", title="States"),
    tooltip=['percent_smokers', 'infection_rate'],
    opacity=alt.value(0.6),
).properties(
    title='Smoking'
).properties(
        width=900,
        height=300
    )
st.altair_chart(smoker, use_container_width=True)

# Infection rate per 100k - percent_insufficient_sleep
sleep = alt.Chart(subset).mark_circle(size=60).encode(
    x=alt.X("percent_insufficient_sleep:Q",
            title="Insufficient sleep Percentage",
            scale=alt.Scale(domain=(min(subset['percent_insufficient_sleep']), max(subset['percent_insufficient_sleep'])))),
    y=alt.Y("infection_rate:Q", title="Infection rate per 100k"),
    color=alt.Color("state:N", title="States"),
    tooltip=['percent_insufficient_sleep', 'infection_rate'],
    opacity=alt.value(0.6),
).properties(
    title='Insufficient sleep'
).properties(
        width=900,
        height=300
    )
st.altair_chart(sleep, use_container_width=True)


df1_0 = pd.read_csv('data.csv')
df1_1 = pd.read_csv('data_month.csv')

default_ym1 = 202003
ym_slider1 = st.slider('Year_Month', min(df1_1['new_date']), max(df1_1['new_date']), value=default_ym1)

st.write("## Association between Insurance Rate and Number of Covid Cases")


df5_1 = df1_1[df1_1['new_date'] == ym_slider1]

scatter1_0 = alt.Chart(df5_1).mark_circle().encode(
    x=alt.X('percent_insured:Q', scale=alt.Scale(domain=[75, 100]), title = 'Percent Insured'),
    y=alt.Y('cases_k:Q', title = 'Number of Cases (thousands)'),
    tooltip=['state','percent_insured','cases_k']
).properties(
    title='Insured Rate and COVID-19 Cases'
).interactive()

scatter1_1 = alt.Chart(df5_1).mark_circle().encode(
    x=alt.X('percent_insured:Q', scale=alt.Scale(domain=[75, 100]), title = 'Percent Insured'),
    y=alt.Y('deaths_k:Q', title = 'Number of Deaths (thousands)'),
    tooltip=['state','percent_insured','deaths_k']
).properties(
    title='Insured Rate and COVID-19 Deaths'
).interactive()

col1_1, col2_1 = st.columns(2)
with col1_1:
    st.altair_chart(scatter1_0, use_container_width=True)

with col2_1:
    st.altair_chart(scatter1_1, use_container_width=True)
    
