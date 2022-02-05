import asyncio
import config
import cv2
import inference
import model_runner
import numpy as np
import uvicorn

from concurrent.futures import ProcessPoolExecutor
from fastapi import File, FastAPI, UploadFile
from functools import partial
from PIL import Image


async def generate_remaining_models(models, image, name: str):
    executor = ProcessPoolExecutor()
    event_loop = asyncio.get_event_loop()
    await event_loop.run_in_executor(
        executor, partial(process_image, models, image, name)
    )


def process_image(models, image, name: str):
    for model in models:
        output, _ = inference.inference(models[model], image)
        name = name.split(".")[0]
        name = f"{name.split('_')[0]}_{models[model]}.jpg"
        cv2.imwrite(name, output)


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome from the API"}


@app.post("/{style}")
async def get_image(style: str, file: UploadFile = File(...)):
    models = config.STYLES.copy()

    # call the model
    model = models[style]
    image = np.array(Image.open(file.file))
    name = model_runner.run(model, image)
    
    # remove the style that we've done from the list and async do the rest
    del models[style]
    asyncio.create_task(generate_remaining_models(models, image, name))
    
    # return the file name
    return {"name": name}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)

