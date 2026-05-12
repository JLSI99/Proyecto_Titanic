import streamlit as st
import pickle
import pandas as pd
import time

# 1. Configuración de pantalla ancha
st.set_page_config(page_title="Titanic Pipeline", layout="wide")

# 2. Estilos CSS para animaciones y diseño táctil
st.markdown("""
    <style>
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    .question-box {
        animation: slideIn 0.5s ease-out;
        padding: 30px;
        background: #1e1e1e;
        border-radius: 20px;
        border: 2px solid #4A90E2;
    }
    .stButton>button {
        width: 100%;
        height: 3.5em;
        font-size: 20px;
        border-radius: 25px;
        background-color: #4A90E2;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Cargar la "Mochila" (Modelo + Escalador)
@st.cache_resource
def load_assets():
    with open('modelo_titanic.pkl', 'rb') as f:
        return pickle.load(f)

assets = load_assets()

# 4. Control de flujo (Estado de la App)
if 'paso' not in st.session_state:
    st.session_state.paso = 1
    st.session_state.datos = {}

# 5. Diseño: Imágenes laterales y contenido central
st.markdown("<h1 style='text-align: center;'>🚢 Pipeline de Datos: Supervivencia Titanic</h1>", unsafe_allow_html=True)

col_img_1, col_content, col_img_2 = st.columns([1, 2, 1])

with col_img_1:
    st.image("https://images.unsplash.com/photo-1500077423678-25eead48513a?w=400", caption="El Puerto de Salida")

with col_img_2:
    st.image("https://images.unsplash.com/photo-1599427303058-f06cbdf4290e?w=400", caption="El Iceberg")

# 6. Preguntas secuenciales
with col_content:
    st.markdown("<div class='question-box'>", unsafe_allow_html=True)
    
    if st.session_state.paso == 1:
        st.subheader("Pregunta 1: ¿Cuál es tu nombre?")
        nombre = st.text_input("Escribe aquí:", placeholder="Tu nombre...")
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
        sexo = st.radio("Selecciona:", ["Mujer", "Hombre"])
        if st.button("Siguiente ➡️"):
            st.session_state.datos['es_hombre'] = 1 if sexo == "Hombre" else 0
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 4:
        st.subheader("¿Qué edad tienes?")
        edad = st.slider("Selecciona tu edad:", 0, 100, 25)
        if st.button("Siguiente ➡️"):
            st.session_state.datos['edad'] = edad
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 5:
        st.subheader("Últimos detalles de tu viaje:")
        sib = st.number_input("Hermanos / Esposa a bordo:", 0, 10, 0)
        parch = st.number_input("Padres / Hijos a bordo:", 0, 10, 0)
        fare = st.number_input("Precio del Ticket (Libras):", 0.0, 500.0, 32.0)
        if st.button("CALCULAR DESTINO 🚢"):
            st.session_state.datos['sib'] = sib
            st.session_state.datos['parch'] = parch
            st.session_state.datos['fare'] = fare
            st.session_state.paso += 1
            st.rerun()

    elif st.session_state.paso == 6:
        st.header("Calculando probabilidades...")
        progreso = st.progress(0)
        for i in range(100):
            time.sleep(0.02) # Total 2 segundos
            progreso.progress(i + 1)
        
        # PROCESO DE IA (Pipeline)
        d = st.session_state.datos
        # 1. Crear DataFrame
        input_df = pd.DataFrame([[d['clase'], d['edad'], d['sib'], d['parch'], d['fare'], d['es_hombre'], 0, 1]], 
                                 columns=assets['columnas'])
        
        # 2. Escalar datos (Traducción)
        input_scaled = assets['escalador'].transform(input_df)
        
        # 3. Predicción (Sigmoide)
        prob = assets['modelo'].predict_proba(input_scaled)[0][1]
        
        st.divider()
        st.balloons()
        st.markdown(f"## {d['nombre']}, tus probabilidades son:")
        st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{prob*100:.2f}%</h1>", unsafe_allow_html=True)
        
        if prob > 0.5:
            st.success("¡SOBREVIVISTE! Te rescató el Carpathia.")
        else:
            st.error("EL DESTINO ES CRUEL. No lograste llegar a los botes.")
            
        if st.button("Reiniciar Simulador"):
            st.session_state.paso = 1
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)