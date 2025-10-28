import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image, ImageOps
import numpy as np
from streamlit_drawable_canvas import st_canvas

# 🎤 Estilo Anuel
st.set_page_config(page_title="🎨🔥 Tablero Inteligente - Anuel Edition", layout="centered")

# 💥 Fondo degradado negro-rojo
st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(to bottom right, #000000, #8B0000);
        }
        [data-testid="stHeader"] {
            background: none;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #1a0000, #330000);
            color: white;
        }
        h1, h2, h3, h4, h5, h6, p, label {
            color: white !important;
        }
        .stButton>button {
            background-color: #ff0000 !important;
            color: white !important;
            border: 2px solid white;
            border-radius: 12px;
            font-weight: bold;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #000 !important;
            color: #ff0000 !important;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# 🎧 Título principal
st.title("🎨🔥 TABLERO INTELIGENTE - ANUEL AI MODE 🔥🎤")
st.markdown("**Dibuja tu boceto, deja que la IA lo interprete y crea una historia épica con flow.**")

with st.sidebar:
    st.subheader("💭 SOBRE ESTA VERSIÓN")
    st.markdown("""
    🎶 Inspirado en el estilo de Anuel:  
    IA, arte y música se fusionan en una experiencia visual 🔥  
    Dibuja, analiza y deja que la máquina narre tu historia 🧠🎤
    """)

# Parámetros del lienzo
drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('🎚️ Grosor del trazo', 1, 30, 5)
stroke_color = "#FFFFFF"  # Blanco para contraste
bg_color = '#000000'

# 🎨 Canvas interactivo
canvas_result = st_canvas(
    fill_color="rgba(255, 0, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=320,
    width=420,
    drawing_mode=drawing_mode,
    key="canvas",
)

# 🔑 Clave API
ke = st.text_input('🔐 Ingresa tu Clave OpenAI', type="password")
os.environ['OPENAI_API_KEY'] = ke
api_key = os.environ['OPENAI_API_KEY']

# Inicializar cliente
client = OpenAI(api_key=api_key)

# 🧠 Botón de análisis
analyze_button = st.button("🚀 Analizar Boceto", type="primary")

# Función para codificar imagen
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return "Error: La imagen no se encontró."

# 📷 Procesamiento del dibujo
if canvas_result.image_data is not None and api_key and analyze_button:
    with st.spinner("🔎 Analizando tu arte con flow..."):
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8')).convert('RGBA')
        input_image.save('img.png')

        base64_image = encode_image_to_base64("img.png")

        prompt_text = "Describe en español brevemente lo que se ve en el dibujo."

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                    ],
                }],
                max_tokens=500,
            )

            descripcion = response.choices[0].message.content
            st.markdown("### 🎤 Resultado del análisis:")
            st.markdown(f"**{descripcion}**")

            st.session_state.full_response = descripcion
            st.session_state.analysis_done = True

        except Exception as e:
            st.error(f"❌ Error: {e}")

# 📚 Crear historia si ya hay descripción
if st.session_state.get("analysis_done", False):
    st.divider()
    st.subheader("📖 ¿Quieres crear una historia con estilo Anuel?")
    if st.button("🔥 Crear historia con flow"):
        with st.spinner("🎶 Generando historia..."):
            story_prompt = (
                f"Basándote en esta descripción: '{st.session_state.full_response}', "
                f"crea una historia infantil con ritmo, creatividad y un toque de estilo urbano."
            )

            story_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": story_prompt}],
                max_tokens=600,
            )

            st.markdown("### 📖 Tu historia:")
            st.write(story_response.choices[0].message.content)

# ⚠️ Advertencia si falta API key
if not api_key:
    st.warning("🚨 Ingresa tu API key para activar el modo Anuel AI.")

