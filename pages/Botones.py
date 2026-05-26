import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# =========================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS VISUALES
# =========================================================
st.set_page_config(
    page_title="Guardian Vision - MQTT Control",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
/* Fondo general de la app */
.stApp {
    background-color: #ffffff !important;
}

/* Forzar textos legibles y oscuros */
html, body, [class*="css"], p, span {
    color: #1f2937 !important;
}

/* Banner superior */
.header-box {
    background: linear-gradient(90deg, #1e3a8a, #3b82f6);
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    color: white !important;
    margin-bottom: 25px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
}
.header-box h1, .header-box h3 {
    color: white !important;
    margin: 5px 0;
}

/* Contenedores tipo tarjeta */
.card {
    background-color: #f8fafc;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.03);
    margin-bottom: 25px;
}

/* Ajustes de botones para que se vean modernos */
div.stButton > button {
    width: 100%;
    border-radius: 10px !important;
    font-weight: bold !important;
    font-size: 16px !important;
    padding: 10px !important;
    border: none !important;
    transition: all 0.3s ease;
}

/* Personalización específica de botones por CSS inline en el layout */
</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNCIONES MQTT (SIN ALTERACIÓN)
# =========================================================
values = 0.0
act1="OFF"

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

broker="broker.mqttdashboard.com"
port=1883
client1= paho.Client("GIT-HUBA")
client1.on_message = on_message

# =========================================================
# INTERFAZ GRÁFICA MEJORADA
# =========================================================

# Encabezado elegante
st.markdown("""
<div class="header-box">
    <h1>⚡ PANEL DE CONTROL MQTT</h1>
    <h3>Guardian Vision | Comunicación IoT</h3>
</div>
""", unsafe_allow_html=True)

# Sección de estado del sistema (Metadata discreta)
col_info1, col_info2 = st.columns(2)
with col_info1:
    st.caption(f"🐍 **Entorno:** Python {platform.python_version()}")
with col_info2:
    st.caption(f"🌐 **Broker:** `{broker}:{port}`")

st.markdown("---")

# --- TARJETA 1: CONTROL DIGITAL (ALERTA) ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#1e3a8a;'>🚨 Control de Alarma (Estados Digitales)</h4>", unsafe_allow_html=True)

# Colocamos los botones de encendido y apagado lado a lado para optimizar espacio
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    # Hack de estilo para botón verde con HTML inyectado simulado por streamlit nativo
    if st.button('🟢 ENCENDER'):
        act1="ENCIENDE ALARMA"
        client1= paho.Client("GIT-HUBA")                                           
        client1.on_publish = on_publish                                          
        client1.connect(broker,port)  
        message =json.dumps({"gesto":act1})
        ret= client1.publish("Guardian_vision", message)
        st.success("Comando enviado: ENCIENDE ALARMA")
    else:
        st.write('')

with col_btn2:
    if st.button('🔴 APAGAR'):
        act1="APAGAR ALARMA"
        client1= paho.Client("GIT-HUBA")                                           
        client1.on_publish = on_publish                                          
        client1.connect(broker,port)  
        message =json.dumps({"gesto":act1})
        ret= client1.publish("Guardian_vision", message)
        st.error("Comando enviado: APAGAR ALARMA")
    else:
        st.write('')

st.markdown('</div>', unsafe_allow_html=True)

# --- TARJETA 2: CONTROL ANALÓGICO ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#1e3a8a;'>🎛️ Control Analógico (Potenciómetro / Umbral)</h4>", unsafe_allow_html=True)

# Desplazable estético
values = st.slider('Selecciona el rango de valores', 0.0, 100.0, step=0.5)

# Contenedor para el botón de envío analógico
st.markdown("<br>", unsafe_allow_html=True)
if st.button('🔵 Enviar valor analógico'):
    client1= paho.Client("GIT-HUBA")                                           
    client1.on_publish = on_publish                                          
    client1.connect(broker,port)   
    message =json.dumps({"Analog": float(values)})
    ret= client1.publish("Guardian_vision", message)
    st.info(f"Valor analógico publicado: {values}")
else:
    st.write('')

st.markdown('</div>', unsafe_allow_html=True)

# Footer del equipo
st.markdown("""
<p style='text-align: center; color: #6b7280 !important; font-size: 13px; margin-top: 50px;'>
    Guardian Vision © Interfaces Multimodales
</p>
""", unsafe_allow_html=True)
