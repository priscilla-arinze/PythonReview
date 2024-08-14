import pandas as pd
import numpy as np
import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def extract(url, table_attribs):
    """ This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. """

    # set up dictionary with table column names (attributes) and initialize to empty list
    top_banks_dict = dict()

    for attr in table_attribs:
        top_banks_dict[attr] = []

    # extract html page & table
    html_page = requests.get(url).text
    soup = BeautifulSoup(html_page, "html.parser")

    tables = soup.find_all("table", {"class": "wikitable sortable mw-collapsible"})
    top_banks_table = tables[0]
    
    # extract rows & data
    rows = top_banks_table.find_all("tr")
    
    for row in rows:
        cell_data = row.find_all("td")
        
        
        if len(cell_data) > 0:
            for i in range(len(table_attribs)):
                current_column_name = table_attribs[i]
                current_cell_data_index = i+1 # skip first column (Rank)
                current_cell_data = None

                # extract bank name
                if current_cell_data_index == 1:
                    current_cell_data = cell_data[1].find_all("a")[1].text
                else:
                    current_cell_data = cell_data[current_cell_data_index].contents[0]

                # slightly clean text (remove new line escape character, strip)
                current_cell_data = str(current_cell_data).strip()
                current_cell_data = current_cell_data.replace("\n", "")

                top_banks_dict[current_column_name].append(current_cell_data)
    
    df = pd.DataFrame(top_banks_dict)

    return df


def transform(df, csv_path, additional_columns):
    """ This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies. """

    usd_market_cap_column_name = "MC_USD_Billion"

    # update data type of MC_USD_Billion column from string to float
    df[usd_market_cap_column_name] = df[usd_market_cap_column_name].astype(float)

    # extract exchange rate csv to DataFrame
    df_exchange_rates = pd.read_csv(csv_path)

    # inner helper function
    def get_exchange_rate(df: pd.DataFrame, currency: str):
        return df.loc[df["Currency"] == currency]["Rate"].iloc[0]

    gbp_rate = get_exchange_rate(df_exchange_rates, "GBP")
    eur_rate = get_exchange_rate(df_exchange_rates, "EUR")
    inr_rate = get_exchange_rate(df_exchange_rates, "INR")
    
    # add 3 new columns for GBP, EUR, and INR currencies
    for col in additional_columns:
        if "GBP" in col:
            df[col] = np.round(df[usd_market_cap_column_name] * gbp_rate, 2)
        elif "EUR" in col:
            df[col] = np.round(df[usd_market_cap_column_name] * eur_rate, 2)
        elif "INR" in col:
            df[col] = np.round(df[usd_market_cap_column_name] * inr_rate, 2)

    return df


def load_to_csv(df: pd.DataFrame, output_path):
    """ This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing. """
    df.to_csv(f"{os.getcwd()}\\{output_path}", index=False)

def load_to_db(df: pd.DataFrame, sql_connection, table_name):
    """ This function saves the final data frame to a database
    table with the provided name. Function returns nothing. """
    df.to_sql(table_name, sql_connection, if_exists="replace", index=False)


def run_query(query_statement, sql_connection):
    """ This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. """
    output = pd.read_sql(query_statement, sql_connection)

    print(f"QUERY EXECUTED: {query_statement}")
    print(f"OUTPUT:\n{output}")


def log_progress(message):
    """ This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing. """
    
    now = datetime.now()
    timestamp = now.strftime("%m-%d-%Y %H:%M:%S")

    full_log_message = f"{timestamp} -- {message}"

    with open(f"{os.getcwd()}\\code_log.txt", "a") as f:
        f.write(f"{full_log_message}\n")

    print(full_log_message)


def main():
    URL = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks"
    DATABASE_NAME = "Banks.db"
    DATABASE_TABLE_NAME = "Largest_banks"
    INITIAL_TABLE_ATTRIBUTES = ["Name", "MC_USD_Billion"]
    ADDITIONAL_TABLE_ATTRIBUTES = ["MC_GBP_Billion", "MC_EUR_Billion", "MC_INR_Billion"]
    EXCHANGE_RATE_CSV_FILE = "exchange_rate.csv"
    OUTPUT_CSV_FILE = "Largest_banks_data.csv"
    
    log_progress("Preliminaries complete. Initiating ETL process")

    ### EXTRACT    
    banks_df = extract(URL, INITIAL_TABLE_ATTRIBUTES)
    log_progress("Data extraction complete. Initiating Transformation process")

    ### TRANSFORM
    full_exchange_rates_csv_path = f"{os.getcwd()}\\{EXCHANGE_RATE_CSV_FILE}"
    banks_df = transform(banks_df, full_exchange_rates_csv_path, ADDITIONAL_TABLE_ATTRIBUTES)
    log_progress("Data transformation complete. Initiating Loading process")

    ### LOAD
    load_to_csv(banks_df, OUTPUT_CSV_FILE)
    log_progress("Data saved to CSV file")
    
    log_progress("SQL Connection initiated")
    conn = sqlite3.connect(DATABASE_NAME)
    load_to_db(banks_df, conn, DATABASE_TABLE_NAME)
    log_progress("Data loaded to Database as a table, Executing queries")

    ### QUERY
    run_query(f"SELECT * FROM {DATABASE_TABLE_NAME}", conn)
    log_progress("Process Complete")


    conn.close()
    log_progress("Server Connection closed")


if __name__ == "__main__":
    main()