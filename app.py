import streamlit as st
import pickle
import pandas as pd
import time

# 1. Configuración
st.set_page_config(page_title="Titanic Pipeline", layout="wide")

# 2. CSS para "Abrazar" solo la pregunta
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Centrado de la columna de contenido */
    [data-testid="stVerticalBlock"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Caja que SOLO abraza la pregunta */
    .question-card {
        background-color: #1e1e1e;
        padding: 25px 40px;
        border-radius: 20px;
        border: 2px solid #4A90E2;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4);
        text-align: center;
        width: 100%;
        margin-bottom: 30px; /* Espacio entre el marco y el botón */
    }

    /* Centrado del botón fuera del marco */
    .stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }

    .stButton>button {
        width: 50% !important;
        height: 3.5em;
        font-size: 18px;
        font-weight: bold;
        border-radius: 50px;
        background-color: #4A90E2 !important;
        color: white !important;
        border: none;
        box-shadow: 0px 5px 15px rgba(74, 144, 226, 0.3);
    }
    
    h1, h2, h3 { text-align: center; color: white !important; }
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

col_img_1, col_content, col_img_2 = st.columns([1, 2, 1])

with col_img_1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Titanic_at_Southampton%2C_England.JPG/400px-Titanic_at_Southampton%2C_England.JPG", caption="Southampton, 1912")

with col_img_2:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/St%C3%B6wer_Titanic.jpg/400px-St%C3%B6wer_Titanic.jpg", caption="Hundimiento del Titanic")

with col_content:
    # --- LOGICA DE PASOS ---
    
    # 1. El Marco Azul solo para la pregunta
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    
    if st.session_state.paso == 1:
        st.header("¿Cuál es tu nombre?")
        nombre = st.text_input("Nombre", label_visibility="collapsed", placeholder="Ej. Yosgar")
    elif st.session_state.paso == 2:
        st.header(f"{st.session_state.datos['nombre']}, ¿En qué clase viajas?")
        clase = st.selectbox("Clase:", [1, 2, 3], format_func=lambda x: f"Clase {x}")
    elif st.session_state.paso == 3:
        st.header("¿Cuál es tu género?")
        sexo = st.radio("Género:", ["Mujer", "Hombre"], horizontal=True)
    elif st.session_state.paso == 4:
        st.header("¿Qué edad tienes?")
        edad = st.slider("Edad:", 0, 95, 25)
    elif st.session_state.paso == 5:
        st.header("Configuración final")
        c1, c2 = st.columns(2)
        with c1: sib = st.number_input("Hermanos/Esposa:", 0, 10, 0)
        with c2: parch = st.number_input("Padres/Hijos:", 0, 10, 0)
        fare = st.number_input("Precio Ticket:", 0.0, 512.0, 32.0)
    elif st.session_state.paso == 6:
        st.header("Resultado del Análisis")
    
    st.markdown('</div>', unsafe_allow_html=True) # Cerramos el marco aquí (antes del botón)

    # 2. El Botón vive fuera del marco
    if st.session_state.paso < 5:
        if st.button("Siguiente ➡️"):
            if st.session_state.paso == 1 and nombre:
                st.session_state.datos['nombre'] = nombre
            elif st.session_state.paso == 2:
                st.session_state.datos['clase'] = clase
            elif st.session_state.paso == 3:
                st.session_state.datos['es_hombre'] = 1 if sexo == "Hombre" else 0
            elif st.session_state.paso == 4:
                st.session_state.datos['edad'] = edad
            
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 5:
        if st.button("CALCULAR DESTINO 🚢"):
            st.session_state.datos.update({'sib': sib, 'parch': parch, 'fare': fare})
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 6:
        # Lógica de predicción (igual a la anterior)
        d = st.session_state.datos
        input_df = pd.DataFrame([[d['clase'], d['edad'], d['sib'], d['parch'], d['fare'], d['es_hombre'], 0, 1]], 
                                 columns=assets['columnas'])
        input_scaled = assets['escalador'].transform(input_df)
        prob = assets['modelo'].predict_proba(input_scaled)[0][1]
        
        st.markdown(f"<h3>Probabilidad de supervivencia:</h3>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size: 80px; color: #FFD700;'>{prob*100:.1f}%</h1>", unsafe_allow_html=True)
        
        if prob > 0.5: st.success("¡SOBREVIVISTE!")
        else: st.error("NO SOBREVIVISTE.")
        
        if st.button("Reiniciar 🔄"):
            st.session_state.paso = 1
            st.rerun()