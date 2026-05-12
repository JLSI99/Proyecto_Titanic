import streamlit as st
import pickle
import pandas as pd
import time

# 1. Configuración
st.set_page_config(page_title="Titanic Pipeline", layout="wide")

# 2. CSS Avanzado para Centrado y Diseño
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Centrado de la columna de contenido */
    [data-testid="stVerticalBlock"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    /* Caja de la pregunta */
    .main-card {
        background-color: #1e1e1e;
        padding: 40px;
        border-radius: 25px;
        border: 2px solid #4A90E2;
        box-shadow: 0px 15px 35px rgba(0,0,0,0.6);
        text-align: center;
        width: 100%;
        margin-bottom: 20px;
    }

    /* Forzar centrado de botones de Streamlit */
    .stButton {
        display: flex;
        justify-content: center;
    }

    .stButton>button {
        width: 60% !important; /* Más elegante que el 100% */
        height: 3.5em;
        font-size: 20px;
        font-weight: bold;
        border-radius: 50px;
        background-color: #4A90E2 !important;
        color: white !important;
        transition: 0.3s;
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

# 5. Estructura de Columnas
col_img_1, col_content, col_img_2 = st.columns([1, 2, 1])

with col_img_1:
    # Imagen: El Titanic en el puerto
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Titanic_at_Southampton%2C_England.JPG/400px-Titanic_at_Southampton%2C_England.JPG", caption="Puerto de Southampton, 1912")

with col_img_2:
    # Imagen: Pintura del hundimiento (Representativa)
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/St%C3%B6wer_Titanic.jpg/400px-St%C3%B6wer_Titanic.jpg", caption="Representación del hundimiento")

with col_content:
    # Contenedor visual
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    if st.session_state.paso == 1:
        st.header("¿Cuál es tu nombre?")
        nombre = st.text_input("Escribe tu nombre", label_visibility="collapsed", placeholder="Ej. Yosgar")
        if st.button("Siguiente ➡️"):
            if nombre:
                st.session_state.datos['nombre'] = nombre
                st.session_state.paso += 1
                st.rerun()

    elif st.session_state.paso == 2:
        st.header(f"{st.session_state.datos['nombre']}, ¿En qué clase viajas?")
        clase = st.selectbox("Clase:", [1, 2, 3], format_func=lambda x: f"Clase {x} - {'Primera' if x==1 else ('Segunda' if x==2 else 'Tercera')}")
        if st.button("Siguiente ➡️"):
            st.session_state.datos['clase'] = clase
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 3:
        st.header("¿Cuál es tu género?")
        sexo = st.radio("Género:", ["Mujer", "Hombre"], horizontal=True) # Centrado horizontal
        if st.button("Siguiente ➡️"):
            st.session_state.datos['es_hombre'] = 1 if sexo == "Hombre" else 0
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 4:
        st.header("¿Qué edad tienes?")
        edad = st.slider("Ajusta tu edad:", 0, 95, 25)
        if st.button("Siguiente ➡️"):
            st.session_state.datos['edad'] = edad
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 5:
        st.header("Configuración final")
        c1, c2 = st.columns(2)
        with c1:
            sib = st.number_input("Hermanos/Esposa:", 0, 10, 0)
        with c2:
            parch = st.number_input("Padres/Hijos:", 0, 10, 0)
        fare = st.number_input("Precio del Ticket (Libras):", 0.0, 512.0, 32.0)
        
        if st.button("CALCULAR DESTINO 🚢"):
            st.session_state.datos.update({'sib': sib, 'parch': parch, 'fare': fare})
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 6:
        with st.status("Ejecutando Pipeline...", expanded=False):
            time.sleep(1)
            st.write("Estandarizando datos...")
            time.sleep(0.5)
            st.write("Consultando Regresión Logística...")
        
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
            st.error("EL DESTINO NO FUE FAVORABLE.")
        
        if st.button("Reiniciar 🔄"):
            st.session_state.paso = 1
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)