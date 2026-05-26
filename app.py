import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model

# =====================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS AVANZADOS (CSS)
# =====================================================
st.set_page_config(page_title="Cerradura Inteligente 360", page_icon="🔐", layout="centered")

# Inyección de CSS para diseño Premium basado en la referencia (Azul Cyber, Cyan y Fondos Fluidos)
st.markdown("""
    <style>
    /* Fondo principal con degradado sutil y oscuro de alta tecnología */
    .stApp {
        background: radial-gradient(circle at top right, #0A192F 0%, #020C1B 100%);
        color: #E2E8F0;
        font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Contenedor principal */
    .stMainBlockContainer {
        padding: 3rem 2rem;
    }
    
    /* Header Principal Estilo Landing Page */
    .header-container {
        text-align: center;
        margin-bottom: 2.5rem;
        padding: 1.5rem;
        border-bottom: 1px solid rgba(56, 189, 248, 0.1);
    }
    
    .main-title {
        color: #FFFFFF;
        font-size: 2.8rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
    }
    
    .subtitle {
        color: #38BDF8;
        font-size: 1.1rem;
        font-weight: 300;
        letter-spacing: 0.5px;
        opacity: 0.9;
    }
    
    /* Tarjetas de Alerta de Reconocimiento Estilizadas */
    .alert-box {
        padding: 2rem;
        border-radius: 16px;
        font-size: 1.3rem;
        text-align: center;
        margin-top: 2rem;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    .alert-success {
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.8) 0%, rgba(2, 44, 34, 0.9) 100%);
        color: #34D399;
        border: 1px solid #059669;
        box-shadow: 0 0 25px rgba(52, 211, 153, 0.15);
    }
    
    .alert-danger {
        background: linear-gradient(135deg, rgba(127, 29, 29, 0.8) 0%, rgba(69, 10, 10, 0.9) 100%);
        color: #FCA5A5;
        border: 1px solid #DC2626;
        box-shadow: 0 0 25px rgba(220, 38, 38, 0.15);
    }
    
    .alert-title {
        font-weight: 800;
        letter-spacing: 1.5px;
        margin-bottom: 0.4rem;
    }
    
    .alert-meta {
        font-size: 0.95rem;
        font-weight: 400;
        opacity: 0.85;
        background: rgba(0,0,0,0.2);
        padding: 0.3rem 1rem;
        border-radius: 20px;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    /* Optimización del input de Cámara de Streamlit para acoplarse al diseño */
    div[data-testid="stCameraInput"] {
        border: 2px dashed rgba(56, 189, 248, 0.25) !important;
        border-radius: 16px !important;
        padding: 10px !important;
        background: rgba(13, 27, 42, 0.4) !important;
    }
    
    div[data-testid="stCameraInput"] button {
        background: linear-gradient(90deg, #00D4FF 0%, #0076FF 100%) !important;
        color: white !important;
        border-radius: 30px !important;
        border: none !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        padding: 0.6rem 2rem !important;
        box-shadow: 0 4px 15px rgba(0, 118, 255, 0.4) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    
    div[data-testid="stCameraInput"] button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.6) !important;
    }
    
    /* Footer corporativo sutil */
    .custom-footer {
        text-align: center;
        font-size: 0.8rem;
        color: #475569;
        margin-top: 4rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 1.5rem;
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

# Encabezado Premium con estilo limpio y tecnológico
st.markdown("""
    <div class="header-container">
        <div class="main-title">🔒 CERRADURA INTELIGENTE 360</div>
        <div class="subtitle">SISTEMA DE CONTROL DE ACCESO POR RECONOCIMIENTO FACIAL</div>
    </div>
""", unsafe_allow_html=True)

img_file_buffer = st.camera_input("Identifíquese frente a la cámara")

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
            f'''
            <div class="alert-box alert-danger">
                <div class="alert-title">🚨 ACCESO DENEGADO</div>
                <div>PERSONA DESCONOCIDA</div>
                <div class="alert-meta">Fiabilidad: {max_prob:.2f}%</div>
            </div>
            ''', 
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
            f'''
            <div class="alert-box alert-success">
                <div class="alert-title">🔓 ACCESO AUTORIZADO</div>
                <div>BIENVENIDA, ISA</div>
                <div class="alert-meta">Compatibilidad: {isa_prob:.2f}%</div>
            </div>
            ''', 
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
            f'''
            <div class="alert-box alert-success">
                <div class="alert-title">🔓 ACCESO AUTORIZADO</div>
                <div>BIENVENIDA, SALO</div>
                <div class="alert-meta">Compatibilidad: {salo_prob:.2f}%</div>
            </div>
            ''', 
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
            f'''
            <div class="alert-box alert-success">
                <div class="alert-title">🔓 ACCESO AUTORIZADO</div>
                <div>BIENVENIDA, ANGIE</div>
                <div class="alert-meta">Compatibilidad: {angie_prob:.2f}%</div>
            </div>
            ''', 
            unsafe_allow_html=True
        )

        client1.publish(
            "Guardian_vision",
            "{'gesto':'angie'}",
            qos=0,
            retain=False
        )

# Footer estético al final de la página
st.markdown('<div class="custom-footer">🔒 Guardian Vision AI Engine • Sistema de Seguridad Encriptado</div>', unsafe_allow_html=True)
