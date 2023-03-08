import altair as alt
import pandas as pd
import streamlit as st
from vega_datasets import data
import datetime


@st.cache
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



df_8 = pd.read_csv('data.csv')
df1_8 = pd.read_csv('data_month.csv')

default_ym_8 = 202003
ym_slider_8 = st.slider('Year_Month', min(df1_8['new_date']), max(df1_8['new_date']), value=default_ym_8)

st.write("## Association between Insurance Rate and Number of Covid Cases")


df5_8 = df1_8[df1_8['new_date'] == ym_slider_8]

scatter_8 = alt.Chart(df5_8).mark_circle().encode(
    x=alt.X('percent_insured:Q', scale=alt.Scale(domain=[75, 100]), title = 'Percent Insured'),
    y=alt.Y('cases_k:Q', title = 'Number of Cases (thousands)'),
    tooltip=['state','percent_insured','cases_k']
).properties(
    title='Insured Rate and COVID-19 Cases'
).interactive()

scatter1_8 = alt.Chart(df5_8).mark_circle().encode(
    x=alt.X('percent_insured:Q', scale=alt.Scale(domain=[75, 100]), title = 'Percent Insured'),
    y=alt.Y('deaths_k:Q', title = 'Number of Deaths (thousands)'),
    tooltip=['state','percent_insured','deaths_k']
).properties(
    title='Insured Rate and COVID-19 Deaths'
).interactive()

col1_8, col2_8 = st.columns(2)
with col1_8:
    st.altair_chart(scatter_8, use_container_width=True)

with col2_8:
    st.altair_chart(scatter1_8, use_container_width=True)

