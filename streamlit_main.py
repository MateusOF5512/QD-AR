import cv2
import numpy as np
from cv2 import aruco
import streamlit as st

# Função para desenhar texto na imagem
def put_text(img, text, pos):
    font = cv2.FONT_HERSHEY_COMPLEX
    font_scale = 0.5
    font_thickness = 1
    color = (255, 255, 255)
    cv2.putText(img, text, pos, font, font_scale, color, font_thickness, cv2.LINE_AA)


st.set_page_config(page_title="Monitor de Consumo de Energia", layout="wide")

def main():

    st.title('Monitor de Consumo de Energia')

    st.markdown('---')

    col1, col2 = st.columns([1, 1])
    col1.text('')
    start = col1.button("Começar gravação")
    stop = col2.button("Parar gravação")
    st.markdown('---')


    stframe = st.empty()

    if start:
        cap = cv2.VideoCapture(0)
        fps = 30
        cap.set(cv2.CAP_PROP_FPS, fps)

        dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        param = aruco.DetectorParameters_create()

        while (cap.isOpened()) and not stop:
            ret, frame = cap.read()

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, _ = cv2.aruco.detectMarkers(gray_frame, dict, parameters=param)


            if ids is not None and len(ids) > 0:
                for i in range(len(ids)):
                    voltage = 220.55  # Substitua pelo valor da tensão associado ao marcador
                    current = 5.35  # Substitua pelo valor da corrente associado ao marcador
                    power = round(voltage * current, 2)  # Cálculo da potência associado ao marcador

                    marker_corners = corners[i][0].astype(int)

                    x, y, w, h = cv2.boundingRect(marker_corners)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), -1)

                    put_text(frame, "Consumo de energia atual:", (x + 10, y + 30))
                    put_text(frame, f"Tensao: {voltage} V", (x + 15, y + 60))
                    put_text(frame, f"Corrente: {current} A", (x + 15, y + 90))
                    put_text(frame, f"Potencia: {power} W", (x + 15, y + 120))

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            cv2.imshow("frame", frame)

            with stframe.container():
                col1, col2, col3 = st.columns([1, 2, 1])
                col1.text('')
                col2.image(frame_rgb, channels="RGB")
                col3.text('')


            if cv2.waitKey(1) & 0xFF == ord('q') or stop:
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
