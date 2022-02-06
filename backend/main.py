import config
import model_runner
import numpy as np
import uvicorn

from fastapi import File, FastAPI, UploadFile
from PIL import Image


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
    path = model_runner.run(model, image)
    
    # remove the style that we've done from the list and async do the rest
    del models[style]
    model_runner.run_async(models, image, path)
    
    # return the file path
    return {"path": path}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080)

