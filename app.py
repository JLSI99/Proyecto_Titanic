import streamlit as st
import pickle
import pandas as pd
import time

# 1. Configuración de pantalla ancha
st.set_page_config(page_title="Titanic Pipeline", layout="wide")

# 2. Estilos CSS corregidos
st.markdown("""
    <style>
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    /* Estilo para el contenedor de la pregunta */
    .question-box {
        animation: slideIn 0.5s ease-out;
        padding: 40px;
        background: #1e1e1e;
        border-radius: 20px;
        border: 2px solid #4A90E2;
        margin-top: 20px;
    }
    /* Ajuste para que los textos de Streamlit hereden el color */
    .question-box h3, .question-box label {
        color: white !important;
    }
    .stButton>button {
        width: 100%;
        height: 3.5em;
        font-size: 20px;
        border-radius: 25px;
        background-color: #4A90E2;
        color: white;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Cargar la "Mochila"
@st.cache_resource
def load_assets():
    with open('modelo_titanic.pkl', 'rb') as f:
        return pickle.load(f)

assets = load_assets()

if 'paso' not in st.session_state:
    st.session_state.paso = 1
    st.session_state.datos = {}

# 5. Diseño: Título e Imágenes
st.markdown("<h1 style='text-align: center;'>🚢 Pipeline de Datos: Supervivencia Titanic</h1>", unsafe_allow_html=True)

col_img_1, col_content, col_img_2 = st.columns([1, 2, 1])

with col_img_1:
    st.image("https://images.unsplash.com/photo-1500077423678-25eead48513a?w=400", caption="El Puerto de Salida")

with col_img_2:
    # IMAGEN CORREGIDA: Enlace directo a archivo
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/St%C3%B6wer_Titanic.jpg/400px-St%C3%B6wer_Titanic.jpg", caption="El Titanic en alta mar")

# 6. Preguntas secuenciales
with col_content:
    # Abrimos el contenedor ANTES de la lógica para que todo viva dentro
    st.markdown("<div class='question-box'>", unsafe_allow_html=True)
    
    if st.session_state.paso == 1:
        st.subheader("Pregunta 1: ¿Cuál es tu nombre?")
        nombre = st.text_input("Escribe aquí:", placeholder="Tu nombre...", label_visibility="collapsed")
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
            time.sleep(0.02)
            progreso.progress(i + 1)
        
        d = st.session_state.datos
        input_df = pd.DataFrame([[d['clase'], d['edad'], d['sib'], d['parch'], d['fare'], d['es_hombre'], 0, 1]], 
                                 columns=assets['columnas'])
        input_scaled = assets['escalador'].transform(input_df)
        prob = assets['modelo'].predict_proba(input_scaled)[0][1]
        
        st.divider()
        st.balloons()
        st.markdown(f"<h2 style='text-align: center;'>{d['nombre']}, tus probabilidades son:</h2>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='text-align: center; color: #FFD700;'>{prob*100:.2f}%</h1>", unsafe_allow_html=True)
        
        if prob > 0.5:
            st.success("¡SOBREVIVISTE! Te rescató el Carpathia.")
        else:
            st.error("EL DESTINO ES CRUEL. No lograste llegar a los botes.")
            
        if st.button("Reiniciar Simulador"):
            st.session_state.paso = 1
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)