import streamlit as st
import pickle
import pandas as pd
import time

# 1. Configuración
st.set_page_config(page_title="Titanic Pipeline", layout="wide")

# 2. CSS Maestro (Corregido y Limpio)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Estilo para la caja de la pregunta (solo abraza el contenido) */
    .question-card {
        background-color: #1e1e1e;
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #4A90E2;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        text-align: center;
        margin: 20px auto;
        max-width: 600px; /* Evita que se estire demasiado */
    }

    /* Centrado real para el botón sin deformarlo */
    .stButton > button {
        display: block;
        margin: 20px auto !important;
        width: 250px !important;
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
    
    /* Evitar que las imágenes se vean mal */
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
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

# 4. Título Principal
st.markdown("<h1>🚢 Simulación de Supervivencia: Titanic</h1>", unsafe_allow_html=True)

# 5. Columnas para el Layout
col_1, col_2, col_3 = st.columns([1, 2, 1])

with col_1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Titanic_at_Southampton%2C_England.JPG/400px-Titanic_at_Southampton%2C_England.JPG", caption="Southampton, 1912")

with col_3:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/St%C3%B6wer_Titanic.jpg/400px-St%C3%B6wer_Titanic.jpg", caption="Hundimiento del Titanic")

with col_2:
    # --- CONTENIDO CENTRAL ---
    
    # Abrimos el marco azul
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    
    if st.session_state.paso == 1:
        st.subheader("¿Cuál es tu nombre?")
        nombre = st.text_input("Nombre", label_visibility="collapsed", placeholder="Escribe aquí...")
    elif st.session_state.paso == 2:
        st.subheader(f"{st.session_state.datos['nombre']}, ¿En qué clase viajas?")
        clase = st.selectbox("Selecciona:", [1, 2, 3], format_func=lambda x: f"Clase {x}")
    elif st.session_state.paso == 3:
        st.subheader("¿Cuál es tu género?")
        sexo = st.radio("Género:", ["Mujer", "Hombre"], horizontal=True)
    elif st.session_state.paso == 4:
        st.subheader("¿Qué edad tienes?")
        edad = st.slider("Edad:", 0, 95, 25)
    elif st.session_state.paso == 5:
        st.subheader("Últimos datos")
        fare = st.number_input("Precio del Ticket:", 0.0, 512.0, 32.0)
        sib = 0; parch = 0 # Simplificado para el demo
    elif st.session_state.paso == 6:
        st.subheader("Resultado Final")
    
    st.markdown('</div>', unsafe_allow_html=True) # Cerramos el marco

    # --- BOTONES FUERA DEL MARCO ---
    if st.session_state.paso == 1:
        if st.button("Siguiente ➡️"):
            if nombre:
                st.session_state.datos['nombre'] = nombre
                st.session_state.paso += 1
                st.rerun()
    elif st.session_state.paso < 5:
        if st.button("Siguiente ➡️"):
            if st.session_state.paso == 2: st.session_state.datos['clase'] = clase
            if st.session_state.paso == 3: st.session_state.datos['es_hombre'] = 1 if sexo == "Hombre" else 0
            if st.session_state.paso == 4: st.session_state.datos['edad'] = edad
            st.session_state.paso += 1
            st.rerun()
    elif st.session_state.paso == 5:
        if st.button("CALCULAR DESTINO 🚢"):
            st.session_state.datos.update({'fare': fare, 'sib': 0, 'parch': 0})
            st.session_state.paso += 1
            st.rerun()
    elif st.session_state.paso == 6:
        # Lógica de IA
        d = st.session_state.datos
        input_df = pd.DataFrame([[d['clase'], d['edad'], d['sib'], d['parch'], d['fare'], d['es_hombre'], 0, 1]], 
                                 columns=assets['columnas'])
        input_scaled = assets['escalador'].transform(input_df)
        prob = assets['modelo'].predict_proba(input_scaled)[0][1]
        
        st.markdown(f"<h3>Probabilidad:</h3>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='font-size: 80px; color: #FFD700;'>{prob*100:.1f}%</h1>", unsafe_allow_html=True)
        
        if prob > 0.5: st.success("¡SOBREVIVISTE!")
        else: st.error("NO SOBREVIVISTE.")
        
        if st.button("Reiniciar 🔄"):
            st.session_state.paso = 1
            st.rerun()