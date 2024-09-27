import pandas as pd
import numpy as np
import sqlite3
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
JSON_OUTPUT_FILE = "Countries_by_GDP.json"
LOG_FILE = "etl_project_log.txt"
DATABASE_NAME = "World_Economies.db"
DATABASE_TABLE_NAME = "Countries_by_GDP"
TABLE_COLUMNS = ["Country", "GDP_USD_billion"]

def log_message(message):
    now = datetime.now()
    current_timestamp = now.strftime("%m-%d-%Y %H:%M:%S")

    timestamped_message = f"{current_timestamp} --- {message}"

    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamped_message}\n")

    print(timestamped_message)

def extract_html_table_to_dataframe():
    log_message("** Initializing data extraction process **")
    # load from webpage
    html_page = requests.get(URL).text
    data = BeautifulSoup(html_page, "html.parser")

    countries_gdp_dict = {
        "Country": [],
        "GDP_USD_billion": []
    }

    try:
        tables = data.find_all("table", class_="wikitable sortable static-row-numbers plainrowheaders srn-white-background")
        countries_gdp_table = tables[0]

        rows = countries_gdp_table.find_all("tr")
        countries_gdp_rows = rows[0]

        log_message
                
    except IndexError:
        message = "The table was not found or the incorrect table was selected."
        log_message(f"ERROR: {message}")
        print(message)



    ### HEADERS
    log_message("** Extracting column headers **")
    headers_tags = countries_gdp_rows.find_all("th")
    headers = []

    for th in headers_tags:
        header_text = th.text
        
        # exclude any bracketed annotations from header text (e.g. [1])
        pattern = r"[\[][\d+].*[\]]"
        bracketed_annotations = re.findall(pattern, header_text)
        if len(bracketed_annotations) > 0:
            header_text = header_text.replace(bracketed_annotations[0], "")

        # remove new line escape character    
        header_text = header_text.replace("\n", "")
        
        headers.append(header_text)

    ### ADD ROWS TO DICTIONARY
    log_message("** Extracting rows **")
    for row in rows:
        # exclude header rows
        class_list = row.get_attribute_list("class")
        if len(class_list) > 0 and class_list[0] == "static-row-header":
            continue

        row_data = row.find_all("td")

        country_name = row_data[0].text.strip()
        gdp_imf = row_data[2].text
        
        countries_gdp_dict["Country"].append(country_name)
        countries_gdp_dict["GDP_USD_billion"].append(gdp_imf)

    log_message("** Data extraction process complete **")

    return pd.DataFrame(countries_gdp_dict)


def transform_dataframe(countries_gdp_df):
    log_message("** Initializing data transformation process **")
    # remove commas from GDP_USD_billion column
    log_message("** Remove commas from GDP_USD_billion column **")
    countries_gdp_df["GDP_USD_billion"] = countries_gdp_df["GDP_USD_billion"].str.replace(",", "")

    # temporarily replace the null values with 0
    log_message("** Temporarily replace the null values with 0 **")
    countries_gdp_df["GDP_USD_billion"] = countries_gdp_df["GDP_USD_billion"].str.replace("—", "0")

    # convert data type of GDP_USD_billion column from string to float
    log_message("** Convert data type of GDP_USD_billion column from string to float **")
    countries_gdp_df["GDP_USD_billion"] = countries_gdp_df["GDP_USD_billion"].astype(float)

    # convert GDP_USD_billion column from millions to billions
    log_message("** Convert GDP_USD_billion column from millions to billions **")
    countries_gdp_df["GDP_USD_billion"] = countries_gdp_df["GDP_USD_billion"] * 0.001

    # round GDP_USD_billion column to 2 decimal places
    log_message("** Round GDP_USD_billion column to 2 decimal places **")
    countries_gdp_df["GDP_USD_billion"] = np.round(countries_gdp_df["GDP_USD_billion"], 2)

    # re-ininstate null values
    log_message("** Re-ininstate null values **")
    countries_gdp_df.loc[countries_gdp_df["GDP_USD_billion"] == 0, "GDP_USD_billion"] = "-"

    log_message("** Data transformation process complete **")

    return countries_gdp_df

def export_dataframe(countries_gdp_df):
    log_message("** Initializing data loading process **")
    load_dataframe_to_json(countries_gdp_df)
    load_dataframe_to_database(countries_gdp_df)
    log_message("** Data loading process complete**")

def load_dataframe_to_json(countries_gdp_df):
    log_message(f"** Loading data to JSON file: {JSON_OUTPUT_FILE} **")
    countries_gdp_df.to_json(JSON_OUTPUT_FILE, indent=4, orient="records")

def load_dataframe_to_database(countries_gdp_df):
    log_message(f"** Loading data to SQLite Database: {DATABASE_NAME} **")
    conn = sqlite3.connect(DATABASE_NAME)
    countries_gdp_df.to_sql(DATABASE_TABLE_NAME, conn, if_exists="replace", index=False)

def main():
    ### EXTRACT
    log_message("START: EXTRACT HTML table of GDP of various countries to Pandas DataFrame")
    countries_gdp_df = extract_html_table_to_dataframe()
    log_message("END: EXTRACT HTML table of GDP of various countries to Pandas DataFrame")

    ### TRANSFORM
    log_message("START: TRANSFORM GDP column of Pandas DataFrame")
    countries_gdp_df = transform_dataframe(countries_gdp_df)
    log_message("END: TRANSFORM GDP column of Pandas DataFrame")

    ### LOAD
    log_message("START: LOAD Pandas DataFrame to JSON and SQLite Database")
    export_dataframe(countries_gdp_df)
    log_message("END: LOAD Pandas DataFrame to JSON and SQLite Database")

    ### QUERY (Countries that have  > 100 Billion GDP)
    log_message("START: Querying countries that have greater than 100 billion in GDP")
    conn = sqlite3.connect(DATABASE_NAME)
    query = f"SELECT * FROM {DATABASE_TABLE_NAME} WHERE CAST(GDP_USD_billion AS decimal) > 100"
    output = pd.read_sql(query, conn)
    print(f"QUERY EXECUTED: {query}\nOUTPUT:\n{output}")
    log_message("END: Querying countries that have greater than 100 billion in GDP")

if __name__ == "__main__":
    main()