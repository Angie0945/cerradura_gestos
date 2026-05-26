import paho.mqtt.client as paho
import time
import json
import streamlit as st
import cv2
import numpy as np
#from PIL import Image
from PIL import Image as Image, ImageOps as ImagOps
from keras.models import load_model

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

        


broker="broker.hivemq.com"
port=1883
client1= paho.Client("APP_CERR")
client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker,port)

model = load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

st.title("Cerradura Inteligente")

img_file_buffer = st.camera_input("Toma una Foto")

if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
   #To read image file buffer as a PIL Image:
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

# =====================================================
# OBTENER PROBABILIDADES
# =====================================================
isa_prob   = prediction[0][0] * 100
salo_prob  = prediction[0][1] * 100
angie_prob = prediction[0][2] * 100

# =====================================================
# MAYOR PROBABILIDAD
# =====================================================
max_prob = max(isa_prob, salo_prob, angie_prob)

# =====================================================
# DESCONOCIDO
# =====================================================
if max_prob < 40:

    st.header(
        f'🚨 PERSONA DESCONOCIDA | Probabilidad: {max_prob:.2f}%'
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

    st.header(
        f'✅ ISA reconocida | Probabilidad: {isa_prob:.2f}%'
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

    st.header(
        f'✅ SALO reconocida | Probabilidad: {salo_prob:.2f}%'
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

    st.header(
        f'✅ ANGIE reconocida | Probabilidad: {angie_prob:.2f}%'
    )

    client1.publish(
        "Guardian_vision",
        "{'gesto':'angie'}",
        qos=0,
        retain=False
    )
