# 706Final - Group: Eagle+Goats - Visualization of COVID-19

In this project, we are interested in the visualization of COVID-19. We use the dataset "US Counties COVID-19 + Weather + Socio/Health Data” published on Kaggle with comprehensive data on COVID-19 cases and deaths in various counties, as well as information on related weather patterns, social indicators, and health statistics, providing a unique opportunity to understand the impact of different factors on the spread of COVID-19. During the pandemic, counties of the United States span a diverse range of social, economic, health, and weather conditions. Because of the COVID19 pandemic, more than 2000 counties have already experienced some COVID19 cases. The data was collected and aimed to identify which populations are at risk of COVID-19 and help prepare high-risk communities. Each observations included in the dataset was collected on a daily basis in each county. The dataset used in the visualization tasks is the subset of the original large full dataset according to the questions that are trying to answer.

All codes deployed on StreamLit is stored in `streamlitApp_combined.py` for visualization tasks.    
Here is the link guiding to the **StreamLit application**: https://jinrui93-706final-streamlitapp-combined-dicvxm.streamlit.app/. 

`JZstreamlitCode.py`, `fz.py`, `streamlit_app.py` are three sub-applications of the combined one with the needs to shorter the wait time when changing features of interest in the application if only interested in visualizing some of the tasks. Below are the links for three applications respectively: 
- https://jinrui93-706finaljz-streamlitapp-eb9syk.streamlit.app/
- https://jinrui93-706final-streamlit-app-y2xo8z.streamlit.app/
- https://jinrui93-706final-fz-opfd3n.streamlit.app/.

5 visualization task are included in the application in total: 
- County-level COVID-19 trends and state-level cumulative deaths
- State-level health disparities
- Weather and COVID-19
- Health indicators and COVID-19
- Insurance coverage and COVID-19 

The date ranges from 2020-01-21, when the first COVID-19 case was detected in the US, to 2020-12-04. All `.csv` files are the subsets of the original complete data or the aggregated dataset by states according to needs toward the specific tasks. Only the dates and corresponding counties when there was at least 1 case in the county are included. There are a total of 318 dates, more than 2400 counties, and 791582 data points in the COVID-19 dataset. Originally, there were 227 daily features and 181 county-level features. In our dataset, we target a subset of the features. Specifically, we will target COVID-19 features, including the number of COVID-19 cases, the number of COVID-19 deaths, and percent vaccinated. All of the COVID-19 features are in quantitative form. Besides, we include county-level weather features–average temperature, humidity, and wind speed, socioeconomic features– median household income, poverty rate, percent insured, and health indicators–smoking habits, obesity, diabetes, and sleep patterns. All of the county-level features are in quantitative form. 

Through exploratory analysis, we aim to visualize spatial and temporal patterns of the spread of COVID-19. This can be used to identify areas with severe COVID-19 spread based on weather, socioeconomic, and health-related factors. By coordinating the spatial distribution of COVID-19 cases and deaths with weather data, we can derive possible correlations between the spread of COVID-19 and different weather patterns, such as average temperature, humidity, and wind speed. We will also explore socioeconomic indicators to determine if they are associated with COVID-19 transmission. For example, we can explore the relationship between COVID-19 cases and poverty rates or insurance coverage at the county level to identify any health disparities within the US counties. Finally, exploring the correlation between COVID-19 cases and health-related factors such as smoking and drinking habits, obesity rate, and sleep patterns can provide insights into the potential contributors to the severity of COVID-19. Ultimately, our exploratory visualization helps provide an interactive context for exploring complex datasets related to COVID-19 spread and its potential risk factors. 
