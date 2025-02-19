from src import xlsxScraper
from src import config
from src.xlsxScraper import add_suffix


def main():
    worksheet = xlsxScraper.load_worksheet_file(f"{config.BASE_DIR}\\dummy.xlsx")
    headers = xlsxScraper.read_sheet_headers(worksheet=worksheet)
    names = xlsxScraper.get_column_data(headers[0], worksheet)
    suffixedNames = add_suffix(names, "CIAOO")
    print(suffixedNames)