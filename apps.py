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

""" INICIO DE MODULO ANTERIOR # Informe automático
st.header("📊 Informe y Sugerencias")

for nombre, df in data.items():
    if not df.empty and len(df) > 1:
        ultimo = df["Close"].iloc[-1]
        penultimo = df["Close"].iloc[-2]
        cambio = (ultimo - penultimo) / penultimo * 100
        tendencia = "📉 Bajista" if cambio < 0 else "📈 Alcista"

        st.write(f"**{nombre}**: Último cierre = {ultimo:.2f} USD")
        st.write(f"Tendencia del día: {tendencia} ({cambio:.2f}%)")

        if cambio > 0:
            st.success(f"Sugerencia: {nombre} muestra fuerza positiva, podría ser buen momento para evaluar entrada.")
        else:
            st.warning(f"Sugerencia: {nombre} está en retroceso, mejor esperar confirmación de tendencia.")
    else:
        st.error(f"No hay suficientes datos para {nombre}") FINAL DE MODULO ANTERIOR """

# INICIO DE LA ACTUALIZACIÓN
import matplotlib.pyplot as plt

# Informe automático
st.header("📊 Informe y Sugerencias")

for nombre, df in data.items():
    if not df.empty and len(df) > 1:
        # Caso: Close es DataFrame con varias columnas
        if isinstance(df["Close"], pd.DataFrame):
            cambios = []
            for col in df["Close"].columns:
                ultimo = float(df["Close"][col].iloc[-1])
                penultimo = float(df["Close"][col].iloc[-2])
                cambio = (ultimo - penultimo) / penultimo * 100
                cambios.append(cambio)
                tendencia = "📉 Bajista" if cambio < 0 else "📈 Alcista"

                st.subheader(f"{nombre} - {col}")
                st.write(f"Último cierre = {ultimo:.2f} USD")
                st.write(f"Tendencia del día: {tendencia} ({cambio:.2f}%)")

                if cambio > 0:
                    st.success(f"Sugerencia: {col} muestra fuerza positiva, podría ser buen momento para evaluar entrada.")
                else:
                    st.warning(f"Sugerencia: {col} está en retroceso, mejor esperar confirmación de tendencia.")

                # 📈 Gráfico de evolución
                fig, ax = plt.subplots()
                df["Close"][col].plot(ax=ax, title=f"Evolución de {col}")
                ax.set_ylabel("Precio (USD)")
                st.pyplot(fig)

            # Informe agregado (promedio de variaciones)
            promedio_cambio = sum(cambios) / len(cambios)
            tendencia_global = "📉 Bajista" if promedio_cambio < 0 else "📈 Alcista"
            st.info(f"**Resumen {nombre}**: Tendencia global = {tendencia_global} ({promedio_cambio:.2f}%)")

        else:
            # Caso normal: Close es Serie
            ultimo = float(df["Close"].iloc[-1])
            penultimo = float(df["Close"].iloc[-2])
            cambio = (ultimo - penultimo) / penultimo * 100
            tendencia = "📉 Bajista" if cambio < 0 else "📈 Alcista"

            st.subheader(nombre)
            st.write(f"Último cierre = {ultimo:.2f} USD")
            st.write(f"Tendencia del día: {tendencia} ({cambio:.2f}%)")

            if cambio > 0:
                st.success(f"Sugerencia: {nombre} muestra fuerza positiva, podría ser buen momento para evaluar entrada.")
            else:
                st.warning(f"Sugerencia: {nombre} está en retroceso, mejor esperar confirmación de tendencia.")

            # 📈 Gráfico de evolución
            fig, ax = plt.subplots()
            df["Close"].plot(ax=ax, title=f"Evolución de {nombre}")
            ax.set_ylabel("Precio (USD)")
            st.pyplot(fig)
    else:
        st.error(f"No hay suficientes datos para {nombre}")

# FIN DE LA ACTUALIZACION

# Ranking simple
st.header("🏆 Ranking de Opciones")

ranking = []
for nombre, df in data.items():
    if not df.empty and len(df) > 1:
        ultimo = df["Close"].iloc[-1]
        penultimo = df["Close"].iloc[-2]
        variacion = (ultimo - penultimo) / penultimo * 100
        ranking.append((nombre, variacion))
    else:
        st.warning(f"No se pudo calcular ranking para {nombre} (datos insuficientes)")

if ranking:
    ranking_df = pd.DataFrame(ranking, columns=["Índice", "Variación %"])
    ranking_df = ranking_df.sort_values(by="Variación %", ascending=False)
    st.table(ranking_df)
else:
    st.error("No se pudo generar el ranking porque no hay datos disponibles.")
