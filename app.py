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
# ISA
# =====================================================
if prediction[0][0] > 0.5:
    client1.publish("Guardian_vision", "{'gesto':'isa'}",qos=0, retain=False)
    probabilidad = round(prediction[0][0] * 100, 2)

    st.header(
        '✅ ISA reconocida, Probabilidad: '
        + str(probabilidad) + '%'
    )

# =====================================================
# SALO
# =====================================================
elif prediction[0][1] > 0.5:
    client1.publish("Guardian_vision", "{'gesto':'salo'}",qos=0, retain=False)
    probabilidad = round(prediction[0][1] * 100, 2)

    st.header(
        '✅ SALO reconocida, Probabilidad: '
        + str(probabilidad) + '%'
    )

# =====================================================
# ANGIE
# =====================================================
elif prediction[0][2] > 0.5:
    client1.publish("Guardian_vision", "{'gesto':'angie'}",qos=0, retain=False)
    probabilidad = round(prediction[0][2] * 100, 2)

    st.header(
        '✅ ANGIE reconocida, Probabilidad: '
        + str(probabilidad) + '%'
    )

# =====================================================
# DESCONOCIDO
# =====================================================
elif prediction[0][2] > 0.1:
    client1.publish("Guardian_vision", "{'gesto':'desconocido'}",qos=0, retain=False)
    probabilidad = round(prediction[0][2] * 100, 2)

    st.header(
        'Persona desconocida, Probabilidad: '
        + str(probabilidad) + '%'
    )




else:

    mayor_probabilidad = round(max(prediction[0]) * 100, 2)

    st.header(
        '🚨 PERSONA DESCONOCIDA | Probabilidad máxima: '
        + str(mayor_probabilidad) + '%'
    )





    
