import cv2
from pathlib import Path

import torch
from models.unet import Unet

from albumentations import (Normalize, Compose)
from albumentations.pytorch import ToTensorV2


def main():
    data_path = Path("C:/Datasets/Трубы/DATASET")
    im = "imgs/3.bmp"
    img = cv2.imread(im)

    # Initialize mode and load trained weights
    ckpt_path = "severstal_models/unet.pth"
    device = torch.device("cuda")
    model = Unet("resnet18", encoder_weights=None, classes=4, activation=None)
    model.to(device)
    model.eval()
    state = torch.load(ckpt_path, map_location=lambda storage, loc: storage)
    model.load_state_dict(state["state_dict"])

    # transform init
    mean = (0.485, 0.456, 0.406)
    std = (0.229, 0.224, 0.225)
    transform = Compose(
        [
            Normalize(mean=mean, std=std, p=1),
            ToTensorV2(),
        ]
    )

    # inference
    with torch.no_grad():
        x = transform(image=img)['image']
        x = x[:, 24:, :]
        x = torch.unsqueeze(x, 0)

        out = model(x.cuda())
        out = torch.sigmoid(out)
        out = out.cpu().numpy()[0, 2]

    img[24:, :, 2][out > 0.05] = img[24:, :, 2][out > 0.05] * (1 - out[out > 0.05]) + out[out > 0.05] * 255

    x = 0


if __name__ == '__main__':
    main()
