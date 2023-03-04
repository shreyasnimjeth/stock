import numpy as np
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import yfinance as yf
from keras.models import load_model
import streamlit as st

def app():
    yf.pdr_override()
    
    start = dt.datetime(2010,1,1)
    end = dt.datetime(2019,12,31)
    
    
    st.title('Stock Treand Prediction')
    
    user_input = st.text_input('Enter Stock Ticker', 'AAPL')
    df = web.get_data_yahoo(user_input, start, end)
    
    #describing data
    st.subheader('Data from 2010 - 2019')
    st.write(df.describe())

    #Visualization
    st.subheader('Closing Price vs Time chart')
    fig = plt.figure(figsize = (12,6))
    plt.plot(df.Close)
    st.pyplot(fig)

    st.subheader('Closing Price vs Time chart with 100MA')
    ma100 = df.Close.rolling(100).mean()
    fig = plt.figure(figsize = (12,6))
    plt.plot(ma100)
    plt.plot(df.Close)
    st.pyplot(fig)
    
    st.subheader('Closing Price vs Time chart with 100MA & 200MA')
    ma100 = df.Close.rolling(100).mean()
    ma200 = df.Close.rolling(200).mean()
    fig = plt.figure(figsize = (12,6))
    plt.plot(ma100, 'r')
    plt.plot(ma200, 'g')
    plt.plot(df.Close, 'b')
    st.pyplot(fig)
    
    #spliting data into tranning and testing

    data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
    data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])


    
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler(feature_range=(0,1))
    
    data_training_array = scaler.fit_transform(data_training)
       
    
    #load my model
    model = load_model('keras_model.h5')
    
    
    
    #testing part
    
    past_100_days = data_training.tail(100)
    final_df = past_100_days.append(data_testing, ignore_index=True)
    input_data = scaler.fit_transform(final_df)
    
    
    x_test = []
    y_test = []

    for i in range(100, input_data.shape[0]):
        x_test.append(input_data[i-100: i])
        y_test.append(input_data[i, 0])
        
    x_test, y_test = np.array(x_test), np.array(y_test)
    
    # making predictions
    y_predicted = model.predict(x_test)
    scaler = scaler.scale_
    
    scale_factor = 1/scaler[0]
    y_predicted = y_predicted * scale_factor
    y_test = y_test * scale_factor
    
    #final graph
    
    st.subheader('Pridictions vs Original')
    fig2 = plt.figure(figsize=(12,6))
    plt.plot(y_test, 'b', label = 'Orignal Price')
    plt.plot(y_predicted, 'r', label = 'Predicted Price')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot(fig2)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    