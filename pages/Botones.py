# =========================================================
# GUARDIAN VISION - SISTEMA UNIFICADO 2026-1
# =========================================================

import streamlit as st
import paho.mqtt.client as mqtt
import paho.mqtt.client as paho  # Se mantienen ambos nombres por tus funciones
import json
import time
import platform
from PIL import Image
from bokeh.models import Button, CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

# =========================================================
# CONFIGURACIÓN GENERAL Y ESTILOS (HOVER + CONTRASTE TOTAL)
# =========================================================
st.set_page_config(
    page_title="Guardian Vision",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Fondo global de la aplicación (Fondo blanco limpio) */
.stApp {
    background-color: #ffffff !important;
}

/* CONTRASTE ALTO: Forzar texto negro/oscuro en toda la app para lectura clara */
html, body, [class*="css"], p, span, label, .stMarkdown {
    color: #111827 !important;
}

/* Sidebar estilizado con texto de alto contraste */
section[data-testid="stSidebar"] {
    background-color: #f3f4f6 !important;
    border-right: 1px solid #e5e7eb;
}
section[data-testid="stSidebar"] * {
    color: #111827 !important;
}

/* Banner de encabezado principal */
.header-box {
    background: linear-gradient(90deg, #0f172a, #1d4ed8);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    color: white !important;
    margin-bottom: 25px;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
}
.header-box h1, .header-box h3 {
    color: #ffffff !important;
    margin: 5px 0;
}

/* Tarjetas contenedoras de componentes */
.card {
    background-color: #ffffff;
    padding: 25px;
    border-radius: 18px;
    border: 2px solid #e5e7eb;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}

/* Pestañas (Tabs) con diseño unificado y coherente */
button[data-baseweb="tab"] {
    font-size: 18px !important;
    font-weight: bold !important;
    color: #4b5563 !important;
}
button[aria-selected="true"] {
    color: #1d4ed8 !important;
    border-bottom-color: #1d4ed8 !important;
}

/* =========================================================
   ESTILOS DE BOTONES CON EFECTO HOVER (PASAR EL CURSOR)
   ========================================================= */
/* Estilo base para todos los botones de Streamlit de la app */
.stButton > button {
    width: 100%;
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 12px !important;
    margin-top: 8px !important;
    transition: all 0.3s ease-in-out !important; /* Animación suave */
    cursor: pointer;
}

/* Identificadores CSS simulados mediante el orden o clases nativas para Hover diferenciado */
/* Botón Encender (Verde) */
div.stButton:nth-of-type(1) > button {
    background-color: #16a34a !important;
}
div.stButton:nth-of-type(1) > button:hover {
    background-color: #15803d !important; /* Se oscurece al pasar el cursor */
    transform: translateY(-2px); /* Pequeño salto estético */
    box-shadow: 0px 5px 12px rgba(22, 163, 74, 0.3);
}

/* Botón Apagar (Rojo) */
div.stButton:nth-of-type(2) > button {
    background-color: #dc2626 !important;
}
div.stButton:nth-of-type(2) > button:hover {
    background-color: #b91c1c !important; /* Se oscurece al pasar el cursor */
    transform: translateY(-2px);
    box-shadow: 0px 5px 12px rgba(220, 38, 38, 0.3);
}

/* Botones genéricos / de envío (Azul) */
div.stButton > button {
    background-color: #2563eb !important;
}
div.stButton > button:hover {
    background-color: #1d4ed8 !important;
    transform: translateY(-2px);
    box-shadow: 0px 5px 12px rgba(37, 99, 235, 0.3);
}

/* Ajuste específico para el contenedor del botón de Bokeh */
div.bk-root {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    margin-top: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER UNIFICADO (COHERENCIA DE MARCA)
# =========================================================
st.markdown("""
<div class="header-box">
    <h1>🛡️ GUARDIAN VISION</h1>
    <h3>Ecosistema Inteligente de Seguridad Multimodal</h3>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR GENERAL
# =========================================================
with st.sidebar:
    st.markdown("<h2 style='margin-top:0;'>📘 Info del Sistema</h2>", unsafe_allow_html=True)
    st.write(f"🐍 **Python:** v{platform.python_version()}")
    st.write("🌐 **Broker:** `broker.mqttdashboard.com`")
    st.write("📌 **Topic:** `Guardian_vision`")
    st.markdown("---")
    st.write("### 🎙️ Guía de Voz (Pestaña App)")
    st.caption("Presiona ESCUCHAR y di: 'enciende la alarma' o 'apaga la alarma'.")

# =========================================================
# CREACIÓN DE PESTAÑAS COHERENTES
# =========================================================
tab_app, tab_botones = st.tabs(["📱 Aplicación Principal (Voz + Cámara)", "🎛️ Panel de Control (MQTT Puro)"])

# ==============================================================================
# PESTAÑA 1: APLICACIÓN PRINCIPAL (VOZ + CÁMARA)
# ==============================================================================
with tab_app:
    
    # --- LOGICA INTERNA MQTT APP 1 ---
    BROKER_APP = "broker.mqttdashboard.com"
    PORT_APP = 1883
    TOPIC_APP = "Guardian_vision"

    @st.cache_resource
    def setup_mqtt_app():
        client = mqtt.Client(client_id="ANGIE_GUARD")
        try:
            client.connect(BROKER_APP, PORT_APP, 60)
        except:
            pass
        return client

    mqtt_client_app = setup_mqtt_app()

    if "alarma_activa" not in st.session_state:
        st.session_state.alarma_activa = False
    if "ultimo_comando" not in st.session_state:
        st.session_state.ultimo_comando = "Sin comandos aún"

    def enviar_mqtt_app(mensaje):
        try:
            payload = json.dumps({"Act1": mensaje})
            mqtt_client_app.publish(TOPIC_APP, payload)
        except:
            pass

    # --- LAYOUT PESTAÑA 1 ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; text-align:center;'>🎙️ Control por Voz</h3>", unsafe_allow_html=True)
        
        # Botón Bokeh de Voz
        stt_button = Button(label="🎙️ ESCUCHAR COMANDO", width=260, height=60)
        stt_button.js_on_event("button_click", CustomJS(code="""
            var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                alert("El navegador no soporta reconocimiento de voz");
            } else {
                var recognition = new SpeechRecognition();
                recognition.lang = 'es-ES';
                recognition.continuous = false;
                recognition.interimResults = false;
                recognition.onresult = function(e) {
                    var value = e.results[0][0].transcript;
                    document.dispatchEvent(new CustomEvent("GET_TEXT", { detail: value }));
                };
                recognition.start();
            }
        """))

        result = streamlit_bokeh_events(
            stt_button, events="GET_TEXT", key="listen",
            refresh_on_update=False, override_height=80, debounce_time=0
        )

        if result and "GET_TEXT" in result:
            comando = result.get("GET_TEXT", "").strip().lower()
            st.session_state.ultimo_comando = comando
            st.info(f"🎤 Se escuchó: {comando}")

            if any(x in comando for x in ["enciende la alarma", "activar alarma", "enciende alarma", "activar", "encender"]):
                st.session_state.alarma_activa = True
                enviar_mqtt_app("activado")
                st.success("🟢 Alarma ACTIVADA por voz")
            elif any(x in comando for x in ["apaga la alarma", "desactiva la alarma", "apaga alarma", "desactivar", "apagar"]):
                st.session_state.alarma_activa = False
                enviar_mqtt_app("desactivado")
                st.warning("🔴 Alarma DESACTIVADA por voz")
            else:
                st.error("⚠️ Comando no reconocido.")

        st.markdown('</div>', unsafe_allow_html=True)

        # Botones Manuales de la App 1
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0; text-align:center;'>🔘 Mandos Directos</h3>", unsafe_allow_html=True)
        
        if st.button("🟢 ENCENDER ALARMA (Manual)"):
            st.session_state.alarma_activa = True
            st.session_state.ultimo_comando = "Encendido manual"
            enviar_mqtt_app("activado")
            
        if st.button("🔴 APAGAR ALARMA (Manual)"):
            st.session_state.alarma_activa = False
            st.session_state.ultimo_comando = "Apagado manual"
            enviar_mqtt_app("desactivado")
        st.markdown('</div>', unsafe_allow_html=True)

        # Recuadro Dinámico del Estado actual de la alarma
        if st.session_state.alarma_activa:
            st.markdown('<div style="background-color:#dcfce7; padding:15px; border-radius:12px; border:2px solid #16a34a; text-align:center;"><b style="color:#166534 !important;">ESTADO: ALARMA ACTIVADA</b></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background-color:#fee2e2; padding:15px; border-radius:12px; border:2px solid #dc2626; text-align:center;"><b style="color:#991b1b !important;">ESTADO: ALARMA DESACTIVADA</b></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>📸 Cámara de Vigilancia</h3>", unsafe_allow_html=True)
        
        foto = st.camera_input("Captura de seguridad")
        if foto is not None:
            imagen = Image.open(foto)
            st.image(imagen, caption="Captura actual", use_container_width=True)
            if st.session_state.alarma_activa:
                st.error("🚨 ALERTA: Presencia detectada")
                enviar_mqtt_app("intruso")
            else:
                st.success("✅ Monitoreo realizado (alarma apagada)")
        else:
            st.markdown("<h4 style='color:#6b7280; text-align:center; padding:30px;'>📷 Esperando captura...</h4>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# PESTAÑA 2: PANEL DE CONTROL (MQTT PURO Y BOTONES ALTERNOS)
# ==============================================================================
with tab_botones:
    
    # --- LOGICA INTERNA MQTT APP 2 (SIN ALTERAR NINGÚN NOMBRE NI PARÁMETRO) ---
    values = 0.0
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

    # --- LAYOUT PESTAÑA 2 ---
    col_bot1, col_bot2 = st.columns(2)

    with col_bot1:
        st.markdown('<div class="card" style="min-height: 280px;">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>🚨 Comandos de Gesto Digital</h3>", unsafe_allow_html=True)
        
        if st.button('ENCENDER'):
            act1 = "ENCIENDE ALARMA"
            client1 = paho.Client("GIT-HUBA")                                           
            client1.on_publish = on_publish                                          
            client1.connect(broker, port)  
            message = json.dumps({"gesto": act1})
            ret = client1.publish("Guardian_vision", message)
            st.success("Published: ENCIENDE ALARMA")
        else:
            st.write('')

        if st.button('APAGAR'):
            act1 = "APAGAR ALARMA"
            client1 = paho.Client("GIT-HUBA")                                           
            client1.on_publish = on_publish                                          
            client1.connect(broker, port)  
            message = json.dumps({"gesto": act1})
            ret = client1.publish("Guardian_vision", message)
            st.error("Published: APAGAR ALARMA")
        else:
            st.write('')
        st.markdown('</div>', unsafe_allow_html=True)

    with col_bot2:
        st.markdown('<div class="card" style="min-height: 280px;">', unsafe_allow_html=True)
        st.markdown("<h3 style='margin-top:0;'>🎛️ Transmisión de Señal Analógica</h3>", unsafe_allow_html=True)
        
        values = st.slider('Selecciona el rango de valores', 0.0, 100.0)
        st.write('Values:', values)

        if st.button('Enviar valor analógico'):
            client1 = paho.Client("GIT-HUBA")                                           
            client1.on_publish = on_publish                                          
            client1.connect(broker, port)   
            message = json.dumps({"Analog": float(values)})
            ret = client1.publish("Guardian_vision", message)
            st.info(f"Published Analog: {values}")
        else:
            st.write('')
        st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FOOTER CON CRÉDITOS EXPLICITADOS (2026-1)
# =========================================================
st.markdown("---")
st.markdown("""
<p style='color:#111827; text-align:center; font-weight: bold; font-size:15px;'>
    🛡️ Guardian Vision © Proyecto de Interfaces Multimodales | Semestre 2026-1
</p>
<p style='color:#4b5563; text-align:center; font-size:14px; margin-top:-10px;'>
    Desarrollado con orgullo por: <b>Isabella Saldarriaga</b> — <b>Salome Rivero</b> — <b>Angie Vargas</b>
</p>
""", unsafe_allow_html=True)
