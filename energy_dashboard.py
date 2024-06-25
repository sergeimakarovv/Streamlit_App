import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import os
import warnings
warnings.filterwarnings('ignore')

# The datatset
# os.chdir(r'C:\Users\makar\OneDrive\Desktop\UE_Applied_Sciences\2 semester\Data Visualization\Final project')
df = pd.read_csv(r'Energy Data (2000-2020).csv')

# Configure the page
st.set_page_config(page_title = 'Sustainable Energy', page_icon = ':globe_with_meridians:', layout = 'wide')
st.title(':globe_with_meridians: World Energy Data')

# Filter the data based on the selected continent
continents = df['continent'].unique().tolist()
continents.insert(0, 'World')
st.sidebar.write('## Select the continent:')
continent = st.sidebar.selectbox('continent', continents)

if not continent or continent == 'World':
    df_continent = df.copy()
else:
    df_continent = df.loc[df['continent'] == continent]

# A map of distribution of the amount of renewable energy
st.subheader(f'Energy production map of {continent}')
# Choose the year
year = st.slider('Choose the year', min_value=2000, max_value=2020, value=2000, step=1)
df_continent_year = df_continent.loc[df_continent['year'] == year]

# Type of energy
st.sidebar.write('## Select the type of energy:')
fossil = st.sidebar.checkbox('fossil fuels', value=True)
nuclear = st.sidebar.checkbox('nuclear energy', value=True)
renewable = st.sidebar.checkbox('renewable energy', value=True)

# Filter the data based on the type of energy selected
if fossil and nuclear and renewable:
    electricity = df_continent_year['fossil_electricity'] + df_continent_year['nuclear_electricity'] + df_continent_year['renewable_electricity']
elif fossil and nuclear:
    electricity = df_continent_year['fossil_electricity'] + df_continent_year['nuclear_electricity']
elif fossil and renewable:
    electricity = df_continent_year['fossil_electricity'] + df_continent_year['renewable_electricity']
elif nuclear and renewable:
    electricity = df_continent_year['nuclear_electricity'] + df_continent_year['renewable_electricity']
elif fossil:
    electricity = df_continent_year['fossil_electricity']
elif nuclear:
    electricity = df_continent_year['nuclear_electricity']
elif renewable:
    electricity = df_continent_year['renewable_electricity']
else:
    electricity = pd.Series([np.nan] * len(df_continent_year['renewable_electricity']))

# Plot a coloured map
fig = px.choropleth(data_frame=df_continent_year,
                    locations='country',
                    locationmode='country names',
                    color=electricity,
                    labels = {'color': 'Amount of electricity (TWh)',
                              'renewable_electricity': 'Amount of electricity (TWh)',
                              'nuclear_electricity': 'Amount of electricity (TWh)',
                              'fossil_electricity': 'Amount of electricity (TWh)'},
                    height = 600,
                    color_continuous_scale='viridis')
fig.update_geos(fitbounds='locations', showframe=False)
st.plotly_chart(fig, use_container_width=True)

# Create a table for energy distribution using pd.melt
df_pie = pd.melt(df_continent_year, id_vars=['country', 'continent'], value_vars=['renewable_electricity', 'nuclear_electricity', 'fossil_electricity'])
types_dict = {
    'renewable_electricity' : 'Renewable',
    'nuclear_electricity' : 'Nuclear',
    'fossil_electricity': 'Fossil fuels'
}
df_pie['variable'] = df_pie['variable'].replace(types_dict)
df_pie = df_pie.rename(columns={'variable': 'type', 'value': 'amount of energy (TWh)'})

# Scatter plot and pie chart
col1, col2 = st.columns((2))
with col1:
    st.subheader(f'Energy distribution in {continent}')
    fig = px.pie(df_pie, values='amount of energy (TWh)', names='type', hole=0.5)
    st.plotly_chart(fig, use_container_width=True)

# Append the electricity column to the data
df_top_prod = df_continent_year.copy()
df_top_prod['amount of energy'] = electricity.round(2)
df_top_prod = df_top_prod.sort_values(by='amount of energy', ascending=False).reset_index(drop=True)[:5]

# Barplot of top 5 countries by the amount of energy produced
with col2:
    st.subheader(f'Top 5 energy producers in {continent}')
    fig = px.bar(df_top_prod, x='country', y='amount of energy',
                 color='amount of energy', color_continuous_scale='viridis')
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("")
st.sidebar.write("Dataset from [Kaggle](https://www.kaggle.com/datasets/anshtanwar/global-data-on-sustainable-energy)")