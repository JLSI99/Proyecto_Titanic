import streamlit as st
import pickle
import pandas as pd
import os

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Titanic Simulation", layout="wide")

# ==========================================
# 2. CSS PERSONALIZADO (Blindado para Centrado Absoluto)
# ==========================================
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* 1. Subheader (Caja de Pregunta) */
    .stElementContainer h3 {
        background-color: #1e1e1e !important;
        color: #4A90E2 !important;
        padding: 30px !important;
        border-radius: 20px !important;
        border: 2px solid #4A90E2 !important;
        text-align: center !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.4);
        margin-bottom: 20px !important;
        width: 100% !important;
    }

    /* 2. Centrar las opciones de Género (Radio Buttons) */
    .stRadio {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important; 
        width: 100% !important;
    }
    
    /* Centrar el texto "Selecciona:" del Radio */
    .stRadio label {
        display: flex !important;
        justify-content: center !important;
        text-align: center !important;
        width: 100% !important;
    }

    /* Centrar los circulitos de Mujer / Hombre */
    .stRadio div[role="radiogroup"] {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        margin: 0 auto !important;
    }

    /* 3. Centrar TODOS los Botones (Siguiente, Calcular, Reiniciar) */
    .stButton {
        display: flex !important;
        justify-content: center !important; /* Fuerza el contenedor al centro */
        width: 100% !important;
        margin: 0 auto !important;
    }

    /* Diseño del botón en sí */
    .stButton button {
        width: 280px !important;
        max-width: 100% !important;
        height: 3.5em !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        background-color: #4A90E2 !important;
        color: white !important;
        border: none !important;
        transition: 0.3s !important;
        margin: 0 auto !important; /* Margen auto bloquea el elemento en el centro */
        display: block !important;
    }
    
    .stButton button:hover {
        background-color: #357ABD !important;
        transform: scale(1.02) !important;
    }

    /* 4. Título Principal */
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
st.markdown("<h1>🚢 Simulación de Jani: Titanic</h1>", unsafe_allow_html=True)

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
            st.markdown(f"<h1 style='font-size: 80px; color: #FFD700; text-align: center;'>{prob*100:.1f}%</h1>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center; border: none !important; box-shadow: none !important; background-color: transparent !important;'>Probabilidad de sobrevivir</h3>", unsafe_allow_html=True)
            
            if prob > 0.5:
                st.balloons()
                st.success("✨ ¡SOBREVIVISTE! Lograste llegar a un bote salvavidas.")
            else:
                st.error("❄️ EL DESTINO NO FUE FAVORABLE. Te has hundido con el Titanic.")
            
            if st.button("Reiniciar Simulador 🔄"):
                st.session_state.paso = 1
                st.session_state.datos = {}
                st.rerun()