import streamlit as st

-- Nombre
st.title("Mi primera aplicación Streamlit")
nombre = st.text_input("¿Cuál es tu nombre?")
if nombre:
    st.success(f"Hola {nombre}, ¡bienvenido a tu app web!")

-- Factoriales
def factorial(n):
    return 1 if n == 0 else n * factorial(n-1)

st.title("Calculadora de factoriales")
numero = st.number_input("Ingresa un número:", min_value=0, step=1)
if st.button("Calcular"):
    st.success(f"El factorial es {factorial(numero)}")


