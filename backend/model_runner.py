import asyncio
import cv2
import inference
import uuid

from concurrent.futures import ProcessPoolExecutor
from functools import partial


def run(model, image):
    output, _ = inference.inference(model, image)
    
    # write the resulting image to a file
    path = f"/storage/{str(uuid.uuid4())}.jpg"
    cv2.imwrite(path, output)

    return path


def run_async(models, image, path: str):
    asyncio.create_task(generate_remaining_models(models, image, path))


async def generate_remaining_models(models, image, path: str):
    executor = ProcessPoolExecutor()
    event_loop = asyncio.get_event_loop()
    await event_loop.run_in_executor(
        executor, partial(process_image, models, image, path)
    )


def process_image(models, image, path: str):
    for model in models:
        output, _ = inference.inference(models[model], image)
        path = path.split(".")[0]
        path = f"{path.split('_')[0]}_{models[model]}.jpg"
        cv2.imwrite(path, output)
