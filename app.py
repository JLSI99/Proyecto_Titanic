import streamlit as st
import pickle
import pandas as pd
import os

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Titanic Simulation", layout="wide")

# ==========================================
# 2. CSS PERSONALIZADO (Estilo Dark, Moderno y Centrado Absoluto)
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Centrado de la columna central */
    [data-testid="stColumn"]:nth-of-type(2) {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Estilo para la Caja de la Pregunta (Subheader) */
    .stElementContainer h3 {
        background-color: #1e1e1e !important;
        color: #4A90E2 !important;
        padding: 30px !important;
        border-radius: 20px !important;
        border: 2px solid #4A90E2 !important;
        text-align: center !important;
        width: 100% !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        margin-bottom: 20px !important;
    }

    /* Centrar estrictamente los contenedores principales de inputs */
    div[data-testid="stTextInput"], 
    div[data-testid="stSelectbox"], 
    div[data-testid="stSlider"], 
    div[data-testid="stNumberInput"] {
        width: 100% !important;
        max-width: 450px !important;
        margin: 0 auto !important; 
    }

    /* 🔥 CORRECCIÓN: Centrado absoluto del Campo de Género (Radio Buttons) */
    div[data-testid="stRadio"] {
        width: 100% !important;
        max-width: 450px !important;
        margin: 0 auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important; /* Centra el texto de "Selecciona:" y los botones */
    }
    
    div[role="radiogroup"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
    }

    /* 🔥 CORRECCIÓN: Centrado absoluto de TODOS los Botones */
    div[data-testid="stButton"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin-top: 15px !important;
    }

    /* Diseño del botón interno */
    div[data-testid="stButton"] > button {
        display: block !important;
        margin: 0 auto !important; /* Margen automático para forzarlo al medio */
        width: 100% !important;
        max-width: 280px !important;
        height: 3.5em !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        background-color: #4A90E2 !important;
        color: white !important;
        border: none !important;
        transition: 0.3s !important;
    }
    
    div[data-testid="stButton"] > button:hover {
        background-color: #357ABD !important;
        transform: scale(1.02) !important;
    }

    h1 { text-align: center; color: white !important; padding-bottom: 20px; }
    
    /* Ajuste para las imágenes */
    [data-testid="stImage"] {
        border-radius: 15px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LÓGICA DE ACTIVOS (Modelo e IA)
# ==========================================
@st.cache_resource
def load_assets():
    file_path = 'modelo_titanic.pkl'
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    return None

assets = load_assets()

# Inicializar estado de la sesión
if 'paso' not in st.session_state:
    st.session_state.paso = 1
    st.session_state.datos = {}

# ==========================================
# 4. ESTRUCTURA VISUAL (Layout)
# ==========================================
st.markdown("<h1>🚢 Simulación de Supervivencia: Titanic</h1>", unsafe_allow_html=True)

# Tres columnas: [Imagen Izq] [Contenido] [Imagen Der]
col_izq, col_centro, col_der = st.columns([1, 2, 1])

# --- Columna Izquierda ---
with col_izq:
    if os.path.exists("Titanic.jpg"):
        st.image("Titanic.jpg", caption="Titanic, 1912", use_container_width=True)
    else:
        st.info("📷 Sube 'Titanic.jpg' a tu repo")

# --- Columna Derecha ---
with col_der:
    if os.path.exists("Iceberg.jpeg"):
        st.image("Iceberg.jpeg", caption="El Destino Final", use_container_width=True)
    else:
        st.info("📷 Sube 'Iceberg.jpeg' a tu repo")

# --- Columna Central (Lógica de la App) ---
with col_centro:
    if assets is None:
        st.error("⚠️ No se encontró 'modelo_titanic.pkl'. Por favor, súbelo al repositorio.")
    else:
        # PASO 1: NOMBRE
        if st.session_state.paso == 1:
            st.subheader("¿Cuál es tu nombre?")
            nombre = st.text_input("Nombre", label_visibility="collapsed", placeholder="Escribe tu nombre aquí...")
            if st.button("Siguiente ➡️"):
                if nombre:
                    st.session_state.datos['nombre'] = nombre
                    st.session_state.paso += 1
                    st.rerun()
                else:
                    st.warning("Necesitamos un nombre para el manifiesto.")

        # PASO 2: CLASE
        elif st.session_state.paso == 2:
            st.subheader(f"Hola {st.session_state.datos['nombre']}, ¿en qué clase viajas?")
            clase = st.selectbox("Clase:", [1, 2, 3], format_func=lambda x: f"Clase {x} - {'Lujo' if x==1 else 'Económica'}")
            if st.button("Siguiente ➡️"):
                st.session_state.datos['clase'] = clase
                st.session_state.paso += 1
                st.rerun()

        # PASO 3: GÉNERO
        elif st.session_state.paso == 3:
            st.subheader("¿Cuál es tu género?")
            sexo = st.radio("Selecciona:", ["Mujer", "Hombre"], horizontal=True)
            if st.button("Siguiente ➡️"):
                st.session_state.datos['es_hombre'] = 1 if sexo == "Hombre" else 0
                st.session_state.paso += 1
                st.rerun()

        # PASO 4: EDAD
        elif st.session_state.paso == 4:
            st.subheader("¿Qué edad tienes?")
            edad = st.slider("Edad:", 0, 95, 25)
            if st.button("Siguiente ➡️"):
                st.session_state.datos['edad'] = edad
                st.session_state.paso += 1
                st.rerun()

        # PASO 5: TARIFA
        elif st.session_state.paso == 5:
            st.subheader("Configuración Final")
            fare = st.number_input("Precio del Ticket (en Libras de 1912):", 0.0, 512.0, 32.0)
            if st.button("CALCULAR DESTINO 🚢"):
                st.session_state.datos.update({'fare': fare, 'sib': 0, 'parch': 0})
                st.session_state.paso += 1
                st.rerun()

        # PASO 6: RESULTADO
        elif st.session_state.paso == 6:
            d = st.session_state.datos
            
            # Preparación de datos para el modelo
            input_df = pd.DataFrame([[d['clase'], d['edad'], d['sib'], d['parch'], d['fare'], d['es_hombre'], 0, 1]], 
                                     columns=assets['columnas'])
            
            input_scaled = assets['escalador'].transform(input_df)
            prob = assets['modelo'].predict_proba(input_scaled)[0][1]
            
            st.subheader(f"Resultado para {d['nombre']}")
            st.markdown(f"<h1 style='font-size: 80px; color: #FFD700;'>{prob*100:.1f}%</h1>", unsafe_allow_html=True)
            st.write("### Probabilidad de sobrevivir")
            
            if prob > 0.5:
                st.balloons()
                st.success("✨ ¡SOBREVIVISTE! Lograste llegar a un bote salvavidas.")
            else:
                st.error("❄️ EL DESTINO NO FUE FAVORABLE. Te has hundido con el Titanic.")
            
            if st.button("Reiniciar Simulador 🔄"):
                st.session_state.paso = 1
                st.session_state.datos = {}
                st.rerun()