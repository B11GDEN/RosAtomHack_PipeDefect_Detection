from __future__ import annotations

import time
import cv2

import streamlit as st
import numpy as np

from models import Unet, ConvNeXtV2
from types import NoneType

st.set_page_config(layout="wide")


def main():
    model = Unet('path/to/Unet/weights')
    cls = ConvNeXtV2('path/to/ConvNeXtV2/weights')
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
                res = cls(model(opencv_image))
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


def plot():
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    import plotly.express as px

    from skimage import data, filters, measure

    from pathlib import Path
    from os import listdir
    from os.path import isfile, join

    vis_idx = ['first', 'second']

    label2color = {
        1: 'darkviolet',
        2: 'lightblue',
        3: 'lime',
        4: 'silver',
        5: 'pink'
    }

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=vis_idx
    )

    img_dir = Path(__file__).absolute().parents[1] / 'imgs'
    img_names = [f for f in listdir(img_dir) if isfile(join(img_dir, f))]
    imgs = []
    for img_name in img_names:
        imgs.append(cv2.imread(str(img_dir / img_name)))

    mask_dir = Path(__file__).absolute().parents[1] / 'masks'
    mask_names = [f for f in listdir(mask_dir) if isfile(join(mask_dir, f))]
    masks = []
    for mask_name in mask_names:
        masks.append(cv2.imread(str(mask_dir / mask_name)))

    for i, idx in enumerate(vis_idx):
        img = imgs[i]
        img = img[24:, :]
        mask = masks[i]
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)


        fig.add_trace(px.imshow(img).data[0], row=1+i//2, col=1+i%2)

        for label in range(1, 6):
            contours = measure.find_contours(mask, 0.5)
            hoverinfo = "<br>".join([f"label: {label}"])

            for contour in contours:
                y, x = contour.T
                fig.add_scatter(
                    x=x,
                    y=y,
                    mode="lines",
                    fill="toself",
                    fillcolor=label2color[label],
                    showlegend=False,
                    opacity=0.5,
                    hovertemplate=hoverinfo,
                    hoveron="points+fills",
                    row=1 + i // 2, col=1 + i % 2
                )

    fig.update_layout(height=800, width=800)

    st.title("Segmentation Mask")
    st.plotly_chart(fig, use_container_width=True)



if __name__ == "__main__":

    st.title("Let's detect pipe defect!")

    main()
    plot()
