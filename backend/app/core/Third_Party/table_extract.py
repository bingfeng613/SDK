# -*- coding: utf-8 -*-

import os
import json
from bs4 import BeautifulSoup

def process_html_files(folder_path):
    html_files_with_tables = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".html"):
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
                soup = BeautifulSoup(html_content, "html.parser")
                tables = soup.find_all("table")

                if len(tables) > 0:
                    html_files_with_tables.append(filename)

    json_data = {
        "num_files_with_tables": len(html_files_with_tables),
        "html_files_with_tables": html_files_with_tables
    }

    json_file_path = "table_files.json"
    with open(json_file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)

if __name__ == '__main__':
    folder_path = "sdk_html_temp"
    process_html_files(folder_path)
