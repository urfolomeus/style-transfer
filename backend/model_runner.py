import asyncio
import cv2
import inference

from concurrent.futures import ProcessPoolExecutor
from functools import partial


def run(model, image, base_path):
    output, _ = inference.inference(model, image)
    
    # write the resulting image to a file
    path = f"{base_path}_{model}.jpg"
    cv2.imwrite(path, output)

    return path


def run_async(models, image, base_path: str):
    asyncio.create_task(generate_remaining_models(models, image, base_path))


async def generate_remaining_models(models, image, base_path: str):
    executor = ProcessPoolExecutor()
    event_loop = asyncio.get_event_loop()
    await event_loop.run_in_executor(
        executor, partial(process_image, models, image, base_path)
    )


def process_image(models, image, base_path: str):
    for model in models.values():
        run(model, image, base_path)
