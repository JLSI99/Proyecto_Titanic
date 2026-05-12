import streamlit as st
import pickle
import pandas as pd
import time

# 1. Configuración de pantalla
st.set_page_config(page_title="Titanic Pipeline", layout="wide")

# 2. CSS Blindado (Sin depender de etiquetas HTML externas para widgets)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    /* Estilizamos los contenedores nativos de Streamlit */
    [data-testid="stVerticalBlock"] > div:has(div.stButton) {
        background: #1e1e1e;
        padding: 30px;
        border-radius: 20px;
        border: 2px solid #4A90E2;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    h1, h2, h3, p { color: white !important; text-align: center; }
    .stButton>button {
        width: 100%;
        height: 3.5em;
        font-size: 20px;
        font-weight: bold;
        border-radius: 25px;
        background-color: #4A90E2 !important;
        color: white !important;
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
st.markdown("<h1>🚢 Pipeline de Datos: Supervivencia Titanic</h1>", unsafe_allow_html=True)
st.write("---")

# 5. Diseño de Columnas
col_img_1, col_content, col_img_2 = st.columns([1, 2, 1])

with col_img_1:
    # Imagen local o de fuente ultra-confiable (Placehold.jp para pruebas)
    st.image("https://images.unsplash.com/photo-1500077423678-25eead48513a?w=400", caption="El Puerto")

with col_img_2:
    # Usamos una imagen de una fuente que no bloquea (NASA o similar)
    st.image("https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2022/03/iceberg_a-76a/24031644-1-eng-GB/Iceberg_A-76A_article_inline.jpg", caption="El Peligro")

# 6. Lógica de Navegación (Usando st.container para el diseño de caja)
with col_content:
    with st.container():
        if st.session_state.paso == 1:
            st.subheader("Paso 1: ¿Cuál es tu nombre?")
            nombre = st.text_input("Nombre:", placeholder="Ej. Jorge", label_visibility="hidden")
            if st.button("Siguiente ➡️"):
                if nombre:
                    st.session_state.datos['nombre'] = nombre
                    st.session_state.paso += 1
                    st.rerun()

        elif st.session_state.paso == 2:
            st.subheader(f"Hola {st.session_state.datos['nombre']}, ¿en qué clase viajarías?")
            clase = st.radio("Selecciona clase:", [1, 2, 3], format_func=lambda x: f"Clase {x} (Lujo)" if x==1 else f"Clase {x}")
            if st.button("Siguiente ➡️"):
                st.session_state.datos['clase'] = clase
                st.session_state.paso += 1
                st.rerun()

        elif st.session_state.paso == 3:
            st.subheader("¿Cuál es tu género?")
            sexo = st.radio("Género:", ["Mujer", "Hombre"])
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
            st.subheader("Casi terminamos...")
            st.session_state.datos['sib'] = st.number_input("Hermanos / Esposa:", 0, 10, 0)
            st.session_state.datos['parch'] = st.number_input("Padres / Hijos:", 0, 10, 0)
            st.session_state.datos['fare'] = st.number_input("Precio del Ticket:", 0.0, 500.0, 32.0)
            if st.button("CALCULAR DESTINO 🚢"):
                st.session_state.paso += 1
                st.rerun()

        elif st.session_state.paso == 6:
            with st.status("Ejecutando Pipeline de Datos...", expanded=True) as status:
                st.write("Estandarizando valores con StandardScaler...")
                time.sleep(1)
                st.write("Pasando datos por la Función Sigmoide...")
                time.sleep(1)
                status.update(label="Análisis Completo!", state="complete", expanded=False)
            
            d = st.session_state.datos
            input_df = pd.DataFrame([[d['clase'], d['edad'], d['sib'], d['parch'], d['fare'], d['es_hombre'], 0, 1]], 
                                     columns=assets['columnas'])
            input_scaled = assets['escalador'].transform(input_df)
            prob = assets['modelo'].predict_proba(input_scaled)[0][1]
            
            st.balloons()
            st.markdown(f"<h2>{d['nombre']}, tu probabilidad es:</h2>", unsafe_allow_html=True)
            st.markdown(f"<h1 style='color: #FFD700; font-size: 80px;'>{prob*100:.2f}%</h1>", unsafe_allow_html=True)
            
            if prob > 0.5:
                st.success("¡SOBREVIVISTE!")
            else:
                st.error("NO SOBREVIVISTE.")
            
            if st.button("Reiniciar"):
                st.session_state.paso = 1
                st.rerun()