import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import time

st.title('Earthquake in Indonesia since 2008')

SOURCE = 'katalog_gempa.csv'

bar = st.progress(0)

@st.cache
def load_data(nrows):
    data = pd.read_csv(SOURCE, nrows=9288)
    for i in range(100):
        bar.progress(i+1)
        time.sleep(0.1)
    return data

data_load_state = st.text('Loading data...')
data = load_data(9288)
st.balloons()
data_load_state.text('Done! (using st.cache)')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

LOCATION = data[['lat', 'lon','mag']]

LOCATION.to_csv("map_data.csv")

SOURCE2 = 'map_data.csv'

location_data = pd.read_csv(SOURCE2)

st.subheader('Pydeck Chart')
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=-7.797068,
        longitude=110.370529,
        zoom=11,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=location_data,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
    ],
))

st.subheader('Map Chart')
st.map(location_data,
        latitude=-7.797068,
        longitude=110.370529,
        zoom= 6
        )


