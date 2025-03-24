import io
from io import BytesIO
from fastapi import FastAPI, File, UploadFile, HTTPException, Response, status, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
import os

from starlette.responses import JSONResponse, StreamingResponse

from . import xlsxScraper

app = FastAPI()

file_buffer : pd.DataFrame = None

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/xlsx/uploadFile")
async def upload_file(response: Response, file: UploadFile = File(...)):
    global file_buffer
    file_buffer = await file.read()
    return {"response": response}

@app.get("/api/xlsx/headers")
def get_file_headers():
    return pd.read_excel(file_buffer).columns

@app.get("/api/config/tool_cards")
def get_tool_cards():
    try:

        return json.load(open(os.getcwd()+"\\src\\config\\config.json", "rb"))
    except FileNotFoundError:
        return "ToolCards config not found"
    except Exception as E:
        return E

@app.post("/api/generateContacts/generate")
async def generate_contacts_generate(contactsData: str = Form(...)):
    filename, file_bytes = xlsxScraper.generateContacts(contactsData)
    media_type = "application/zip" if filename.endswith(".zip") else "text/vcard"
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return StreamingResponse(io.BytesIO(file_bytes), media_type=media_type, headers=headers)

@app.post("/api/generateContacts/uploadFile")
async def generate_contacts_file_upload(file: UploadFile = File(...)):
    file_contents = await file.read()
    file_bytes = BytesIO(file_contents)
    data_frame = pd.read_excel(file_bytes)
    data = xlsxScraper.processFile(data_frame)
    return JSONResponse(content={"fileName":file.filename, "data":data})