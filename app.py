import streamlit as st
import pickle
import pandas as pd
import time

# 1. Configuración
st.set_page_config(page_title="Titanic Pipeline", layout="wide")

# 2. CSS Maestro - Versión Final Blindada
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Contenedor central de la columna 2 */
    [data-testid="stColumn"]:nth-of-type(2) [data-testid="stVerticalBlock"] {
        align-items: center !important;
        display: flex;
        flex-direction: column;
    }

    /* Estilo del Marco de la Pregunta */
    .stElementContainer h3 {
        width: 100% !important;
        max-width: 500px;
        background-color: #1e1e1e !important;
        color: #ffffff !important;
        padding: 30px !important;
        border-radius: 20px !important;
        border: 2px solid #4A90E2 !important;
        text-align: center !important;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4);
        margin-bottom: 20px !important;
    }

    /* Estilo del Botón Centrado */
    .stButton > button {
        width: 280px !important;
        height: 3.5em;
        font-size: 18px;
        font-weight: bold;
        border-radius: 50px;
        background-color: #4A90E2 !important;
        color: white !important;
        border: none;
        box-shadow: 0px 5px 15px rgba(74, 144, 226, 0.3);
        margin-top: 10px;
    }
    
    /* Centrado de los inputs */
    .stTextInput, .stSelectbox, .stSlider, .stRadio {
        width: 100% !important;
        max-width: 400px;
    }

    h1 { text-align: center; color: white !important; margin-bottom: 40px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Cargar activos
@st.cache_resource
def load_assets():
    with open('modelo_titanic.pkl', 'rb') as f:
        return pickle.load(f)

assets = load_assets()

if 'paso' not in st.session_state:
    st.session_state.paso = 1
    st.session_state.datos = {}

# 4. Título
st.markdown("<h1>🚢 Simulación de Supervivencia: Titanic</h1>", unsafe_allow_html=True)

# 5. Layout
col_1, col_2, col_3 = st.columns([1, 2, 1])

with col_1:
    # Imagen estable 1
    st.image("https://cdn.pixabay.com/photo/2012/03/01/01/42/ship-20333_1280.jpg", caption="El Titanic")

with col_3:
    # Imagen estable 2
    st.image("https://cdn.pixabay.com/photo/2015/12/07/10/55/ice-1080554_1280.jpg", caption="Aguas del Atlántico")

with col_2:
    if st.session_state.paso == 1:
        st.subheader("¿Cuál es tu nombre?")
        nombre = st.text_input("Nombre", label_visibility="collapsed", placeholder="Tu nombre...")
        if st.button("Siguiente ➡️"):
            if nombre:
                st.session_state.datos['nombre'] = nombre
                st.session_state.paso += 1
                st.rerun()

    elif st.session_state.paso == 2:
        st.subheader(f"Hola {st.session_state.datos['nombre']}, ¿en qué clase viajas?")
        clase = st.selectbox("Clase:", [1, 2, 3], format_func=lambda x: f"Clase {x}")
        if st.button("Siguiente ➡️"):
            st.session_state.datos['clase'] = clase
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 3:
        st.subheader("¿Cuál es tu género?")
        sexo = st.radio("Selecciona:", ["Mujer", "Hombre"], horizontal=True)
        if st.button("Siguiente ➡️"):
            st.session_state.datos['es_hombre'] = 1 if sexo == "Hombre" else 0
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 4:
        st.subheader("¿Qué edad tienes?")
        edad = st.slider("Edad:", 0, 95, 25)
        if st.button("Siguiente ➡️"):
            st.session_state.datos['edad'] = edad
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 5:
        st.subheader("Detalles del Viaje")
        fare = st.number_input("Precio Ticket:", 0.0, 500.0, 30.0)
        if st.button("CALCULAR DESTINO 🚢"):
            st.session_state.datos.update({'fare': fare, 'sib': 0, 'parch': 0})
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 6:
        d = st.session_state.datos
        input_df = pd.DataFrame([[d['clase'], d['edad'], d['sib'], d['parch'], d['fare'], d['es_hombre'], 0, 1]], 
                                 columns=assets['columnas'])
        input_scaled = assets['escalador'].transform(input_df)
        prob = assets['modelo'].predict_proba(input_scaled)[0][1]
        
        st.subheader(f"Resultado para {d['nombre']}")
        st.markdown(f"<h1 style='font-size: 80px; color: #FFD700;'>{prob*100:.1f}%</h1>", unsafe_allow_html=True)
        
        if prob > 0.5:
            st.balloons()
            st.success("¡SOBREVIVISTE!")
        else:
            st.error("NO SOBREVIVISTE.")
        
        if st.button("Reiniciar 🔄"):
            st.session_state.paso = 1
            st.rerun()