import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model

# =====================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS (CSS)
# =====================================================
st.set_page_config(page_title="Cerradura Inteligente", page_icon="🔐", layout="centered")

# Inyección de CSS para diseño profesional en Azules, Negro y Blanco
st.markdown("""
    <style>
    /* Fondo de la app y color de texto principal */
    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
    }
    
    /* Contenedor principal de tarjetas */
    .css-1r6il7b, .stMainBlockContainer {
        padding: 2rem 3rem;
    }
    
    /* Título Principal */
    .main-title {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #FFFFFF;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        color: #38BDF8;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Estilos para las alertas de reconocimiento */
    .alert-box {
        padding: 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 1.25rem;
        text-align: center;
        margin-top: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .alert-success {
        background-color: #064E3B;
        color: #34D399;
        border: 1px solid #059669;
    }
    .alert-danger {
        background-color: #7F1D1D;
        color: #FCA5A5;
        border: 1px solid #DC2626;
    }
    
    /* Ajustes para el componente de cámara de Streamlit */
    div[data-testid="stCameraInput"] button {
        background-color: #1D4ED8 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
    }
    div[data-testid="stCameraInput"] button:hover {
        background-color: #2563EB !important;
    }
    </style>
""", unsafe_allow_html=True)

max_prob = 0

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("APP_CERR")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker, port)

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

# Títulos estilizados con HTML/CSS
st.markdown('<h1 class="main-title">🔐 Cerradura Inteligente</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Sistema de Control de Acceso por Reconocimiento Facial</p>', unsafe_allow_html=True)

img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    # To read image file buffer as a PIL Image:
    img = Image.open(img_file_buffer)

    newsize = (224, 224)
    img = img.resize(newsize)
    # To convert PIL Image to numpy array:
    img_array = np.array(img)

    # Normalize the image
    normalized_image_array = (img_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    prediction = model.predict(data)

    print(prediction)
    isa_prob   = prediction[0][0] * 100
    salo_prob  = prediction[0][1] * 100
    angie_prob = prediction[0][2] * 100
    max_prob = max(isa_prob, salo_prob, angie_prob)

    # =====================================================
    # DESCONOCIDO (Menor a 85%)
    # =====================================================
    if max_prob < 85:
        st.markdown(
            f'<div class="alert-box alert-danger">🚨 PERSONA DESCONOCIDA<br><span style="font-size:1rem; font-weight:normal;">Probabilidad: {max_prob:.2f}%</span></div>', 
            unsafe_allow_html=True
        )

        client1.publish(
            "Guardian_vision",
            "{'gesto':'desconocido'}",
            qos=0,
            retain=False
        )

    # =====================================================
    # ISA
    # =====================================================
    elif isa_prob == max_prob:
        st.markdown(
            f'<div class="alert-box alert-success">✅ ISA RECONOCIDA<br><span style="font-size:1rem; font-weight:normal;">Probabilidad: {isa_prob:.2f}%</span></div>', 
            unsafe_allow_html=True
        )

        client1.publish(
            "Guardian_vision",
            "{'gesto':'isa'}",
            qos=0,
            retain=False
        )

    # =====================================================
    # SALO
    # =====================================================
    elif salo_prob == max_prob:
        st.markdown(
            f'<div class="alert-box alert-success">✅ SALO RECONOCIDA<br><span style="font-size:1rem; font-weight:normal;">Probabilidad: {salo_prob:.2f}%</span></div>', 
            unsafe_allow_html=True
        )

        client1.publish(
            "Guardian_vision",
            "{'gesto':'salo'}",
            qos=0,
            retain=False
        )

    # =====================================================
    # ANGIE
    # =====================================================
    elif angie_prob == max_prob:
        st.markdown(
            f'<div class="alert-box alert-success">✅ ANGIE RECONOCIDA<br><span style="font-size:1rem; font-weight:normal;">Probabilidad: {angie_prob:.2f}%</span></div>', 
            unsafe_allow_html=True
        )

        client1.publish(
            "Guardian_vision",
            "{'gesto':'angie'}",
            qos=0,
            retain=False
        )
