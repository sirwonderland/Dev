import streamlit as st
import pandas as pd
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go

countries = ['Argentina','Brazil','Canada','Colombia','Peru','Russia','United States','Ukraine']
intervals = ['Daily', 'Weekly', 'Monthly']

start_date = datetime.today()-timedelta(days=30)
end_date = datetime.today()

@st.cache
def consultar_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(stock=stock, country=country, from_date=from_date,
                                        to_date=to_date, interval=interval)
    return df

def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)

def plotCandleStick(df, acao='ticket'):
    tracel = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }

    data = [tracel]
    layout = go.Layout()

    fig = go.Figure(data=data, layout=layout)
    return fig

##BARRA LATERAL##

barra_lateral = st.sidebar.empty()

country_select = st.sidebar.selectbox("Selecione o país:", countries)

acoes = ip.get_stocks_list(country=country_select)

stock_select = st.sidebar.selectbox("Selecione o ativo financeiro:", acoes)

from_date = st.sidebar.date_input('De:', start_date)
to_date = st.sidebar.date_input('Até:', end_date)

interval_select = st.sidebar.selectbox("Selecione o intervalo de tempo:", intervals)

carregar_dados = st.sidebar.checkbox('Carregar dados do intervalo selecionado')

##ELEMENTOS CENTRAIS##

st.title('Monitor de ações | Stock Monitor')

st.header('Ações')

st.subheader('Visualização em gráfico')

grafico_candle = st.empty()
grafico_line = st.empty()

if from_date > to_date:
    st.sidebar.error('Data inicial maior que data final')
else:
    df = consultar_acao(stock_select, country_select, format_date(from_date), format_date(to_date), interval_select)
    try:
            fig = plotCandleStick(df)
            grafico_candle = st.plotly_chart(fig)
            grafico_line = st.line_chart(df.Close)

            if carregar_dados:
                st.subheader('Dados')
                dados = st.dataframe(df)
    except Exception as e:
            st.error(e)
