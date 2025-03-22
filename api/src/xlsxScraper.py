import pandas as pd
import pathlib
import fastapi
from pandas.core.interchange.dataframe_protocol import DataFrame
from starlette.datastructures import UploadFile


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
    return