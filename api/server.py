from __future__ import annotations

import uvicorn
import io
import cv2

import numpy as np

from typing import List
from fastapi import FastAPI, File, UploadFile, status
from fastapi.responses import JSONResponse

from models import Unet, ConvNeXtV2

model = Unet('path/to/Unet/weights')
cls = ConvNeXtV2('path/to/ConvNeXtV2/weights')

app = FastAPI()


@app.get("/")
async def index():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": "Success"})


@app.post("/processing")
async def processing(files: List[UploadFile] = File(...)):

    try:
        error = False
        results = []
        for file in files:
            try:
                contents = file.file.read()
                img_stream = io.BytesIO(contents)
                img = cv2.imdecode(np.frombuffer(img_stream.read(), dtype="uint8"), 1)

                res = cls(model())

                results.append({"filename": file.filename,
                                "result": "Success",
                                "data": res})

            except Exception as e:
                error = True
                results.append({"filename": file.filename,
                                "result": f"ERROR {e.__class__.__name__} {e}",
                                "data": None})
            finally:
                file.file.close()

        if error:
            return JSONResponse(status_code=status.HTTP_424_FAILED_DEPENDENCY, content={"result": results})

        return JSONResponse(status_code=status.HTTP_200_OK, content={"result": results})

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"result": f"ERROR {e.__class__.__name__} {e}"})


def main():
    uvicorn.run(app, host="localhost", port=8000)


if __name__ == "__main__":
    main()
