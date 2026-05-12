import streamlit as st
import pickle
import pandas as pd
import os

# 1. Configuración de pantalla
st.set_page_config(page_title="Titanic Pipeline", layout="wide")

# 2. CSS Optimizado
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Centrado exclusivo de la columna central */
    [data-testid="stColumn"]:nth-of-type(2) > div {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* Estilo para la Caja de la Pregunta */
    .stElementContainer h3 {
        background-color: #1e1e1e !important;
        color: #4A90E2 !important;
        padding: 30px !important;
        border-radius: 20px !important;
        border: 2px solid #4A90E2 !important;
        text-align: center !important;
        width: 100% !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
    }

    /* Botón Siguiente */
    .stButton > button {
        display: block;
        margin: 25px auto !important;
        width: 100% !important;
        max-width: 300px;
        height: 3.5em;
        font-size: 20px;
        font-weight: bold;
        border-radius: 50px;
        background-color: #4A90E2 !important;
        color: white !important;
        border: none;
        box-shadow: 0px 8px 15px rgba(74, 144, 226, 0.3);
    }

    /* Ajuste para inputs */
    .stTextInput, .stSelectbox, .stSlider, .stRadio {
        width: 100% !important;
        max-width: 450px;
    }

    h1 { text-align: center; color: white !important; margin-bottom: 40px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Cargar Activos de IA (con manejo de error para Cloud)
@st.cache_resource
def load_assets():
    file_path = 'modelo_titanic.pkl'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None

assets = load_assets()

if 'paso' not in st.session_state:
    st.session_state.paso = 1
    st.session_state.datos = {}

# 4. Título Principal
st.markdown("<h1>🚢 Simulación de Supervivencia: Titanic</h1>", unsafe_allow_html=True)

# 5. Diseño de 3 Columnas
col_izq, col_centro, col_der = st.columns([1, 2, 1])

with col_izq:
    # URL directa de Wikimedia Commons
    st.image("https://upload.wikimedia.org/wikipedia/commons/a/af/Titanic_at_Southampton%2C_England.JPG", 
             caption="Southampton, 1912", use_container_width=True)

with col_der:
    # URL directa de Wikimedia Commons
    st.image("https://upload.wikimedia.org/wikipedia/commons/6/6e/St%C3%B6wer_Titanic.jpg", 
             caption="Hundimiento (Representación)", use_container_width=True)

with col_centro:
    if assets is None:
        st.error("Error: No se encontró el archivo 'modelo_titanic.pkl'. Asegúrate de subirlo a tu repositorio de GitHub.")
    else:
        # Lógica de Navegación
        if st.session_state.paso == 1:
            st.subheader("¿Cuál es tu nombre?")
            nombre = st.text_input("Nombre", label_visibility="collapsed", placeholder="Tu nombre...")
            if st.button("Siguiente ➡️"):
                if nombre:
                    st.session_state.datos['nombre'] = nombre
                    st.session_state.paso += 1
                    st.rerun()
                else:
                    st.warning("Por favor, introduce tu nombre.")

        elif st.session_state.paso == 2:
            st.subheader(f"Hola {st.session_state.datos['nombre']}, ¿en qué clase viajas?")
            clase = st.selectbox("Clase:", [1, 2, 3], format_func=lambda x: f"Clase {x} - {'Lujo' if x==1 else 'Económica'}")
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
            st.subheader("Configuración Final")
            fare = st.number_input("Precio del Ticket (Libras):", 0.0, 512.0, 32.0)
            if st.button("CALCULAR DESTINO 🚢"):
                st.session_state.datos.update({'fare': fare, 'sib': 0, 'parch': 0})
                st.session_state.paso += 1
                st.rerun()

        elif st.session_state.paso == 6:
            d = st.session_state.datos
            # Ajusta los nombres de las columnas según tu modelo
            input_df = pd.DataFrame([[d['clase'], d['edad'], d['sib'], d['parch'], d['fare'], d['es_hombre'], 0, 1]], 
                                     columns=assets['columnas'])
            
            input_scaled = assets['escalador'].transform(input_df)
            prob = assets['modelo'].predict_proba(input_scaled)[0][1]
            
            st.subheader(f"Resultado para {d['nombre']}")
            st.markdown(f"<h1 style='font-size: 100px; color: #FFD700;'>{prob*100:.1f}%</h1>", unsafe_allow_html=True)
            
            if prob > 0.5:
                st.balloons()
                st.success("¡FELICIDADES, SOBREVIVISTE!")
            else:
                st.error("EL DESTINO NO FUE FAVORABLE.")
            
            if st.button("Reiniciar 🔄"):
                st.session_state.paso = 1
                st.session_state.datos = {}
                st.rerun()