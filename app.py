import streamlit as st
import pickle
import pandas as pd
import time

# 1. Configuración de pantalla
st.set_page_config(page_title="Titanic Pipeline", layout="wide")

# 2. CSS Maestro (Corregido para evitar cuadros duplicados)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Contenedor Principal Central */
    .main-card {
        background-color: #1e1e1e;
        padding: 40px;
        border-radius: 20px;
        border: 2px solid #4A90E2;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.5);
        text-align: center;
        margin-top: 20px;
    }

    /* Limpiar bordes automáticos de Streamlit */
    [data-testid="stVerticalBlock"] > div { border: none !important; }
    
    h1, h2, h3, p { color: white !important; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    
    /* Botones Estilo Touch */
    .stButton>button {
        width: 100%;
        height: 3.5em;
        font-size: 20px;
        font-weight: bold;
        border-radius: 50px;
        background-color: #4A90E2 !important;
        color: white !important;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #357ABD !important;
        transform: scale(1.02);
    }
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
st.markdown("<h1 style='font-size: 45px;'>🚢 Pipeline de Datos: Predicción Titanic</h1>", unsafe_allow_html=True)

# 5. Estructura de Columnas
col_img_1, col_content, col_img_2 = st.columns([1, 2, 1])

with col_img_1:
    st.image("https://images.unsplash.com/photo-1569389397653-c04fe624e663?w=400", caption="El Puerto de Southampton")

with col_img_2:
    # Imagen de respaldo confiable (Iceberg)
    st.image("https://images.unsplash.com/photo-1551244072-5d12893278ab?w=400", caption="El Campo de Hielo")

with col_content:
    # USAMOS UN DIV HTML PARA EL MARCO AZUL ÚNICO
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    if st.session_state.paso == 1:
        st.subheader("Pregunta 1: ¿Cuál es tu nombre?")
        nombre = st.text_input("Nombre", label_visibility="collapsed", placeholder="Tu nombre aquí...")
        if st.button("Siguiente ➡️"):
            if nombre:
                st.session_state.datos['nombre'] = nombre
                st.session_state.paso += 1
                st.rerun()

    elif st.session_state.paso == 2:
        st.subheader(f"Hola {st.session_state.datos['nombre']}, ¿en qué clase viajarías?")
        clase = st.radio("Clase", [1, 2, 3], format_func=lambda x: f"Clase {x} - {'Lujo' if x==1 else 'Económica'}")
        if st.button("Siguiente ➡️"):
            st.session_state.datos['clase'] = clase
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 3:
        st.subheader("¿Cuál es tu género?")
        sexo = st.radio("Género", ["Mujer", "Hombre"])
        if st.button("Siguiente ➡️"):
            st.session_state.datos['es_hombre'] = 1 if sexo == "Hombre" else 0
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 4:
        st.subheader("¿Qué edad tienes?")
        edad = st.slider("Edad", 0, 90, 25)
        if st.button("Siguiente ➡️"):
            st.session_state.datos['edad'] = edad
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 5:
        st.subheader("Configuración Final")
        col_a, col_b = st.columns(2)
        with col_a:
            sib = st.number_input("Hermanos/Esposa", 0, 10, 0)
        with col_b:
            parch = st.number_input("Padres/Hijos", 0, 10, 0)
        fare = st.number_input("Precio Ticket", 0.0, 512.0, 32.0)
        
        if st.button("CALCULAR DESTINO 🚢"):
            st.session_state.datos.update({'sib': sib, 'parch': parch, 'fare': fare})
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 6:
        with st.status("Procesando datos del pasajero...", expanded=False):
            time.sleep(1)
            st.write("Estandarizando variables...")
            time.sleep(1)
            st.write("Ejecutando Inferencia...")
        
        d = st.session_state.datos
        # Generar predicción
        input_df = pd.DataFrame([[d['clase'], d['edad'], d['sib'], d['parch'], d['fare'], d['es_hombre'], 0, 1]], 
                                 columns=assets['columnas'])
        input_scaled = assets['escalador'].transform(input_df)
        prob = assets['modelo'].predict_proba(input_scaled)[0][1]
        
        st.markdown(f"<h2>{d['nombre']}, tu probabilidad es:</h2>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size: 100px; color: #FFD700;'>{prob*100:.1f}%</h1>", unsafe_allow_html=True)
        
        if prob > 0.5:
            st.balloons()
            st.success("¡FELICIDADES, SOBREVIVISTE!")
        else:
            st.error("LAMENTABLEMENTE NO SOBREVIVISTE.")
        
        if st.button("Intentar de nuevo 🔄"):
            st.session_state.paso = 1
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)