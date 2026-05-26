import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform
# Necesario para integrar imágenes con base64 en CSS
import base64

# =====================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS AVANZADOS (CSS)
# =====================================================
st.set_page_config(page_title="MQTT Control Premium", page_icon="🎛️", layout="centered")

# Inyección de CSS premium basado en la referencia técnica
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
    
    /* Header Principal Estilo Panel de Control con Imagen */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 1.5rem;
        border-bottom: 1px solid rgba(56, 189, 248, 0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }
    
    .main-title {
        color: #FFFFFF;
        font-size: 2.6rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.2rem;
        text-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
    }
    
    .subtitle {
        color: #38BDF8;
        font-size: 1.1rem;
        font-weight: 300;
        letter-spacing: 0.5px;
        opacity: 0.9;
    }
    
    .control-hub-img {
        max-width: 150px; /* Ajusta el tamaño según sea necesario */
        height: auto;
        border-radius: 12px;
        border: 2px solid rgba(56, 189, 248, 0.15);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    }

    /* Info de versión sutil integrada arriba */
    .version-text {
        color: #475569;
        font-size: 0.85rem;
        text-align: center;
        margin-bottom: 1.5rem;
        background: rgba(13, 27, 42, 0.4);
        padding: 0.4rem 1rem;
        border-radius: 20px;
        display: inline-block;
        border: 1px solid rgba(56, 189, 248, 0.05);
    }
    
    .version-container {
        text-align: center;
    }
    
    /* Selector Robusto para Botones de Streamlit */
    div.stButton > button {
        width: 100% !important;
        border-radius: 30px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase;
    }

    /* Estilo específico para el botón ENCENDER */
    div.stButton > button:has(p:contains("ENCENDER")) {
        background: linear-gradient(90deg, #00D4FF 0%, #0076FF 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 118, 255, 0.3) !important;
    }
    
    div.stButton > button:has(p:contains("ENCENDER")):hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 212, 255, 0.5) !important;
    }

    /* Estilo específico para el botón APAGAR */
    div.stButton > button:has(p:contains("APAGAR")) {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #94A3B8 !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
    }
    
    div.stButton > button:has(p:contains("APAGAR")):hover {
        background: rgba(30, 41, 59, 0.9) !important;
        color: #F1F5F9 !important;
        border-color: rgba(148, 163, 184, 0.5) !important;
        transform: translateY(-2px);
    }

    /* Mensajes de estado debajo de los botones */
    .status-msg {
        text-align: center;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.6) 0%, rgba(30, 41, 59, 0.6) 100%);
        padding: 0.8rem;
        border-radius: 12px;
        margin-top: 0.8rem;
        color: #38BDF8;
        font-weight: 600;
        letter-spacing: 0.5px;
        border: 1px solid rgba(56, 189, 248, 0.15);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }
    
    /* Footer corporativo sutil */
    .custom-footer {
        text-align: center;
        font-size: 0.8rem;
        color: #475569;
        margin-top: 5rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Muestra la versión de Python de manera más integrada al diseño
st.markdown(f'<div class="version-container"><p class="version-text">⚙️ Python v{platform.python_version()}</p></div>', unsafe_allow_html=True)

act1 = "OFF"

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
client1 = paho.Client("GIT-HUBA")
client1.on_message = on_message

# Encabezado Premium con imagen integrada
# Abrimos la imagen Camara 2.png y la mostramos con base64 para CSS
with open("Camara 2.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

st.markdown(f"""
    <div class="header-container">
        <div class="main-title">MQTT CONTROL HUB</div>
        <div class="subtitle">CONTROL REMOTO DE ALARMAS</div>
        <img src="data:image/png;base64,{encoded_string}" class="control-hub-img" alt="Cámara 2">
    </div>
""", unsafe_allow_html=True)

# =====================================================
# BOTÓN ENCENDER
# =====================================================
if st.button('ENCENDER'):
    act1 = "ENCIENDE ALARMA"
    client1 = paho.Client("GIT-HUBA")                            
    client1.on_publish = on_publish                          
    client1.connect(broker, port)  
    message = json.dumps({"gesto": act1})
    ret = client1.publish("Guardian_vision", message)
    st.markdown('<div class="status-msg">📡 TRANSMITIENDO: ENCIENDE ALARMA</div>', unsafe_allow_html=True)
else:
    st.write('')

# Separador estético sutil
st.markdown('<br>', unsafe_allow_html=True)

# =====================================================
# BOTÓN APAGAR
# =====================================================
if st.button('APAGAR'):
    act1 = "APAGAR ALARMA"
    client1 = paho.Client("GIT-HUBA")                            
    client1.on_publish = on_publish                          
    client1.connect(broker, port)  
    message = json.dumps({"gesto": act1})
    ret = client1.publish("Guardian_vision", message)
    st.markdown('<div class="status-msg">📡 TRANSMITIENDO: APAGAR LA ALARMA</div>', unsafe_allow_html=True)
else:
    st.write('')

# Footer estético al final de la página
st.markdown('<div class="custom-footer">🔒 Guardian Vision AI Engine • Sistema de Control Encriptado por: Isa, Salo y Angie </div>', unsafe_allow_html=True)
