import zipfile
import pandas as pd
import pathlib
import json
import math
import io

from pandas import Timestamp


# Loads an Excel file into a DataFrame if the file exists.
def load_worksheet_file(inputPath: str) -> pd.DataFrame:
    inputPath = pathlib.Path(inputPath)
    if not inputPath.is_file():
        raise FileNotFoundError(f"File {inputPath} not found")
    return pd.read_excel(inputPath)


# Returns a specific sheet from a DataFrame containing multiple sheets.
def read_sheet(worksheet: pd.DataFrame, sheetName: str) -> pd.DataFrame:
    return worksheet[sheetName]


# Returns the column headers of a DataFrame.
def get_sheet_headers(sheet: pd.DataFrame) -> list:
    return list(sheet.columns)


# Returns the column headers from an Excel file or an existing DataFrame.
# Ensures only one of `inputPath` or `worksheet` is provided.
def read_sheet_headers(
        inputPath: str | None = None,
        worksheet: pd.DataFrame | None = None,
        sheetName: str | None = None
) -> list:

    if not ((worksheet is None) ^ (inputPath is None)):
        raise ValueError("Provide either a file path or a DataFrame, not both")

    if worksheet is None:
        worksheet = load_worksheet_file(inputPath)

    return get_sheet_headers(read_sheet(worksheet, sheetName)) if sheetName else get_sheet_headers(worksheet)


# Returns all values from a specified column.
def get_column_data(columnName: str, sheet: pd.DataFrame) -> list:
    return sheet[columnName].to_list()


# Adds a suffix to each item in a list.
def add_suffix(namesList: list, suffix: str) -> list:
    return [f"{name} {suffix}" for name in namesList]

def add_prefix(namesList: list, prefix: str) -> list:
    return [f"{prefix} {name}" for name in namesList]

def processFile(data_frame: pd.DataFrame):
    columnsNames = get_sheet_headers(data_frame)
    columnsData = {}
    for col in columnsNames:
        col_data = get_column_data(col, data_frame)
        if type(col_data[0]) == Timestamp:
            columnsNames.remove(col)
            continue
        if isinstance(col_data, pd.Series):
            col_data = col_data.fillna("").tolist()
            columnsData[col] = col_data

        else:
            col_data = ["" if pd.isna(x) else x for x in col_data]
            columnsData[col] = col_data

    assembledData = {
        "headers": columnsNames,
        "columnsData": columnsData
    }
    return assembledData

def create_vcard(name: str, number: str) -> str:
    return (
        "BEGIN:VCARD\r\n"
        "VERSION:3.0\r\n"
        f"N:;{name};;;\r\n"
        f"FN:{name}\r\n"
        f"TEL;TYPE=CELL:{number}\r\n"
        "END:VCARD\r\n"
    )

def generateContacts(contactsData: str):
    data = json.loads(contactsData)
    numbers = data["selectedMobile"]
    names = data["formattedNames"]
    vCardName = data["vCardName"]
    nFile = data["nFile"]

    if nFile < 1:
        nFile = 1

    chunk_size = math.ceil(len(names) / nFile)

    if nFile == 1:
        vcf_content = ""
        for name, number in zip(names, numbers):
            vcf_content += create_vcard(name, number)
        file_bytes = vcf_content.encode('utf-8')
        filename = vCardName if vCardName.endswith(".vcf") else vCardName + ".vcf"
        return filename, file_bytes

    else:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_index in range(nFile):
                start_index = file_index * chunk_size
                end_index = (file_index + 1) * chunk_size
                names_chunk = names[start_index:end_index]
                numbers_chunk = numbers[start_index:end_index]
                vcf_content = ""
                for name, number in zip(names_chunk, numbers_chunk):
                    vcf_content += create_vcard(name, number)
                file_name = f"{vCardName} - {file_index + 1}.vcf"
                zipf.writestr(file_name, vcf_content.encode('utf-8'))
        zip_buffer.seek(0)
        filename = vCardName if vCardName.endswith(".zip") else vCardName + ".zip"
        return filename, zip_buffer.read()

