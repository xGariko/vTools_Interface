from fastapi import FastAPI, File, UploadFile, HTTPException, Response, status
import pandas as pd

app = FastAPI()

file_buffer : pd.DataFrame = None


@app.post("/xlsx/uploadFile")
async def upload_file(response: Response, file: UploadFile = File(...)):
    global file_buffer
    file_buffer = await file.read()
    return {"response": response}

@app.get("xlsx/headers")
def get_file_headers():
    return pd.read_excel(file_buffer).columns