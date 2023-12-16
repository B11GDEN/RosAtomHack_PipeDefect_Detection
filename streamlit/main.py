from __future__ import annotations

import time
import cv2

import streamlit as st
import numpy as np

from types import NoneType

st.set_page_config(layout="wide")


def main():
    main_form = st.form("main_form", clear_on_submit=True)

    with main_form:
        image = st.file_uploader("Choose a image", accept_multiple_files=False, type=['jpg', 'png', 'bmp'])

        submitted = st.form_submit_button("Submit")

    if submitted:
        if type(image) is NoneType:
            st.error('You have to choose an image!', icon="🚨")

        else:
            file_bytes = np.asarray(bytearray(image.read()), dtype="uint8")

            opencv_image = cv2.imdecode(file_bytes, 1)
            original = opencv_image.copy()

            with st.spinner('Wait for it...'):
                start = time.time()
                # TODO: we need the model
                # res = model(opencv_image)
                time.sleep(10)
                res = np.zeros((600, 600, 3), dtype="uint8")
                end = time.time() - start

            show_result(original, res, end)


def show_result(original, result, time):

    st.header("Results")

    col1, col2 = st.columns(2)

    with col1:
        st.image(original, channels="BGR")
        st.image(result, channels="BGR")

    with col2:
        st.text("Original image and the detected defects")
        st.text(f"Elapsed time: {time}")


if __name__ == "__main__":

    st.title("Let's detect pipe defect!")

    main()
