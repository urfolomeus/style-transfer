import asyncio
import cv2
import inference
import uuid

from concurrent.futures import ProcessPoolExecutor
from functools import partial


def run(model, image):
    output, _ = inference.inference(model, image)
    
    # write the resulting image to a file
    name = f"/storage/{str(uuid.uuid4())}.jpg"
    cv2.imwrite(name, output)

    return name


def run_async(models, image, name: str):
    asyncio.create_task(generate_remaining_models(models, image, name))


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
