import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Título de la aplicación
st.title("📈 Reporte de Inversión - NASDAQ & S&P 500")

# Selección de índices
indices = {
    "NASDAQ": "^IXIC",
    "S&P 500": "^GSPC"
}

# Fecha actual
hoy = datetime.date.today()

# Descargar datos
data = {}
for nombre, ticker in indices.items():
    df = yf.download(ticker, period="5d", interval="1d")
    data[nombre] = df

# Mostrar datos
for nombre, df in data.items():
    st.subheader(f"{nombre} - Últimos 5 días")
    st.line_chart(df["Close"])
    st.write(df.tail(3))  # últimas 3 filas

# Informe automático
st.header("📊 Informe y Sugerencias")

for nombre, df in data.items():
    cambio = (df["Close"][-1] - df["Close"][-2]) / df["Close"][-2] * 100
    tendencia = "📉 Bajista" if cambio < 0 else "📈 Alcista"
    st.write(f"**{nombre}**: Último cierre = {df['Close'][-1]:.2f} USD")
    st.write(f"Tendencia del día: {tendencia} ({cambio:.2f}%)")

    if cambio > 0:
        st.success(f"Sugerencia: {nombre} muestra fuerza positiva, podría ser buen momento para evaluar entrada.")
    else:
        st.warning(f"Sugerencia: {nombre} está en retroceso, mejor esperar confirmación de tendencia.")

# Ranking simple
st.header("🏆 Ranking de Opciones")
ranking = sorted(
    [(nombre, (df["Close"][-1] - df["Close"][-2]) / df["Close"][-2] * 100) for nombre, df in data.items()],
    key=lambda x: x[1],
    reverse=True
)

ranking_df = pd.DataFrame(ranking, columns=["Índice", "Variación %"])
st.table(ranking_df)
