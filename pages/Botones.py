import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# =====================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS (CSS)
# =====================================================
st.set_page_config(page_title="MQTT Control", page_icon="🎛️", layout="centered")

# Inyección de CSS para diseño profesional en Azules, Negro y Blanco
st.markdown("""
    <style>
    /* Fondo de la app y color de texto principal */
    .stApp {
        background-color: #0B0F19;
        color: #F8FAFC;
    }
    
    /* Contenedor principal */
    .stMainBlockContainer {
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
        margin-bottom: 2.5rem;
        font-weight: 400;
    }

    /* Info de versión sutil al pie o arriba */
    .version-text {
        color: #64748B;
        font-size: 0.85rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Estilos específicos para los botones de Streamlit */
    /* Botón ENCENDER (Primer botón en el flujo) */
    div.element-container:nth-of-type(4) button {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: 1px solid #3B82F6 !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 0.75rem !important;
        font-size: 1.1rem !important;
        transition: background-color 0.3s ease;
    }
    div.element-container:nth-of-type(4) button:hover {
        background-color: #2563EB !important;
    }
    
    /* Botón APAGAR (Segundo botón en el flujo) */
    div.element-container:nth-of-type(6) button {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border-radius: 8px !important;
        border: 1px solid #475569 !important;
        font-weight: bold !important;
        width: 100% !important;
        padding: 0.75rem !important;
        font-size: 1.1rem !important;
        transition: background-color 0.3s ease;
    }
    div.element-container:nth-of-type(6) button:hover {
        background-color: #334155 !important;
    }

    /* Mensajes de estado debajo de los botones */
    .status-msg {
        text-align: center;
        background-color: #1E293B;
        padding: 0.5rem;
        border-radius: 6px;
        margin-top: 0.5rem;
        color: #38BDF8;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Muestra la versión de Python de manera más integrada al diseño
st.markdown(f'<p class="version-text">Versión de Python en entorno: {platform.python_version()}</p>', unsafe_allow_html=True)

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

# Títulos estilizados con HTML
st.markdown('<h1 class="main-title">🎛️ MQTT Control</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Panel de Control Remoto de Alarmas</p>', unsafe_allow_html=True)

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
    st.markdown('<div class="status-msg">📡 Comando enviado: ENCIENDE ALARMA</div>', unsafe_allow_html=True)
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
    st.markdown('<div class="status-msg">📡 Comando enviado: APAGAR LA ALARMA</div>', unsafe_allow_html=True)
else:
    st.write('')
