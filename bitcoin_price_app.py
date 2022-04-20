# -*- coding: utf-8 -*-
# Importing libraries
import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Setting title for the app.
st.title('Bitcoin Price Viewer')

# Setting slider to give number of days.
days = st.slider('No of Days', 2, 365, 90)

# Setting radio buttons to select currency.
currency = st.radio(
     "Currency",
     ('USD', 'CAD', 'INR', 'EUR'))

# Requesting data from URL.
r = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?', 
                  params={'vs_currency': currency, 'days':days,'interval':'daily'})


# Formatting data for chart once request is successful.
if r.status_code == 200:
    data = r.json()
    
    df1 = pd.DataFrame.from_dict(data['prices'])
    df1.columns = ["Date", "Price"]
    df1.Date = pd.to_datetime(df1["Date"],unit='ms')
    df1.set_index('Date', inplace=True)

# Creating line chart for the prices.
fig = px.line(df1, title = "Bitcoin price in {0} over last {1} days".format(currency,days))

# Plotting chart.
st.plotly_chart(fig, use_container_width=True)

# Displaying mean value of the price.
st.write("Average price during this time was ", (df1['Price'].mean()),currency)