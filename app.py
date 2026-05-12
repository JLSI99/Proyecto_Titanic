import streamlit as st
import pickle
import pandas as pd
import time

# 1. Configuración de página
st.set_page_config(page_title="Titanic Pipeline", layout="wide")

# 2. CSS Maestro (Optimizado para evitar cuadros vacíos)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Estilo para los subheaders (Preguntas) */
    .stElementContainer h3 {
        text-align: center;
        color: #4A90E2 !important;
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #4A90E2;
        margin-bottom: 20px;
    }

    /* Botón Siguiente Centrado y Grande */
    .stButton > button {
        display: block;
        margin: 0 auto !important;
        width: 300px !important;
        height: 3.5em;
        font-size: 20px;
        font-weight: bold;
        border-radius: 50px;
        background-color: #4A90E2 !important;
        color: white !important;
        border: none;
        box-shadow: 0px 8px 15px rgba(74, 144, 226, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0px 12px 20px rgba(74, 144, 226, 0.3);
    }

    /* Centrado de inputs y radio buttons */
    [data-testid="stVerticalBlock"] > div {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    h1 { text-align: center; color: white !important; margin-bottom: 50px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Cargar activos (Mochila Técnica)
@st.cache_resource
def load_assets():
    with open('modelo_titanic.pkl', 'rb') as f:
        return pickle.load(f)

assets = load_assets()

if 'paso' not in st.session_state:
    st.session_state.paso = 1
    st.session_state.datos = {}

# 4. Título Principal
st.markdown("<h1>🚢 Simulación de Supervivencia: Titanic</h1>", unsafe_allow_html=True)

# 5. Layout de Columnas
col_1, col_2, col_3 = st.columns([1, 2, 1])

with col_1:
    st.image("https://images.unsplash.com/photo-1516652491258-2079df6566cd?w=400", caption="El Puerto")

with col_3:
    st.image("https://images.unsplash.com/photo-1551244072-5d12893278ab?w=400", caption="El Iceberg")

with col_2:
    # --- LOGICA DE NAVEGACIÓN ---
    
    if st.session_state.paso == 1:
        st.subheader("¿Cuál es tu nombre?")
        nombre = st.text_input("Nombre", label_visibility="collapsed", placeholder="Escribe aquí...")
        if st.button("Siguiente ➡️"):
            if nombre:
                st.session_state.datos['nombre'] = nombre
                st.session_state.paso += 1
                st.rerun()

    elif st.session_state.paso == 2:
        st.subheader(f"Hola {st.session_state.datos['nombre']}, ¿en qué clase viajarías?")
        clase = st.selectbox("Clase:", [1, 2, 3], format_func=lambda x: f"Clase {x}")
        if st.button("Siguiente ➡️"):
            st.session_state.datos['clase'] = clase
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 3:
        st.subheader("¿Cuál es tu género?")
        sexo = st.radio("Género:", ["Mujer", "Hombre"], horizontal=True)
        if st.button("Siguiente ➡️"):
            st.session_state.datos['es_hombre'] = 1 if sexo == "Hombre" else 0
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 4:
        st.subheader("¿Qué edad tienes?")
        edad = st.slider("Edad:", 0, 100, 25)
        if st.button("Siguiente ➡️"):
            st.session_state.datos['edad'] = edad
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 5:
        st.subheader("Costo del pasaje")
        fare = st.number_input("Precio Ticket (Libras):", 0.0, 500.0, 32.0)
        if st.button("CALCULAR DESTINO 🚢"):
            st.session_state.datos.update({'fare': fare, 'sib': 0, 'parch': 0})
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 6:
        # PROCESO DE IA
        d = st.session_state.datos
        input_df = pd.DataFrame([[d['clase'], d['edad'], d['sib'], d['parch'], d['fare'], d['es_hombre'], 0, 1]], 
                                 columns=assets['columnas'])
        input_scaled = assets['escalador'].transform(input_df)
        prob = assets['modelo'].predict_proba(input_scaled)[0][1]
        
        st.markdown(f"<h3>{d['nombre']}, tu probabilidad es:</h3>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size: 100px; color: #FFD700;'>{prob*100:.1f}%</h1>", unsafe_allow_html=True)
        
        if prob > 0.5:
            st.balloons()
            st.success("¡SOBREVIVISTE!")
        else:
            st.error("NO SOBREVIVISTE.")
        
        if st.button("Reiniciar 🔄"):
            st.session_state.paso = 1
            st.rerun()