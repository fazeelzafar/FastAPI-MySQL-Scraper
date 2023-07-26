from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
import mysql.connector

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
success_logger = logging.getLogger('success_logger')
failure_logger = logging.getLogger('failure_logger')
success_handler = logging.FileHandler('success.log')
failure_handler = logging.FileHandler('failure.log')
success_logger.addHandler(success_handler)
failure_logger.addHandler(failure_handler)

# MySQL Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'toor',
    'database': 'scraped_data',
}

# Create MySQL table if not exists
CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS scraped_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Symbols VARCHAR(255),
    Names VARCHAR(255),
    Last_Price VARCHAR(255),
    Price_Change VARCHAR(255),
    Percentage_Change VARCHAR(255),
    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
"""

connection = mysql.connector.connect(**DB_CONFIG)
cursor = connection.cursor()
cursor.execute(CREATE_TABLE_QUERY)
cursor.close()
connection.close()


def get_column_data(driver, xpath):
    return [element.text for element in driver.find_elements(By.XPATH, xpath)]


def scrape_and_store_data():
    try:
        # Set up ChromeOptions for headless browsing
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run Chrome in headless mode
        chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (for headless mode to work)

        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://finance.yahoo.com/lookup')

        Symbols = get_column_data(driver, '//a[@class="Fw(b)"]')
        Names = get_column_data(driver, '//td[@class="data-col1 Ta(start) Pstart(10px) Miw(80px)"]')
        Last_Price = get_column_data(driver, '//td[@class="data-col2 Ta(end) Pstart(20px)"]')
        Change = get_column_data(driver, "//td[@class='data-col3 Ta(end) Pstart(20px)']//span")
        Prcnt_Change = get_column_data(driver, '//td[@class="data-col4 Ta(start) Pstart(20px) Pend(6px) W(130px)"]')

        data = zip(Symbols, Names, Last_Price, Change, Prcnt_Change)

        # Store the data in the MySQL database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        insert_query = "INSERT INTO scraped_data (Symbols, Names, Last_Price, Price_Change, Percentage_Change, Timestamp) VALUES (%s, %s, %s, %s, %s, %s)"

        # Convert zip object to a list of tuples
        data_list = [(symbol, name, price, change, prcnt_change, datetime.now()) for symbol, name, price, change, prcnt_change in data]

        cursor.executemany(insert_query, data_list)
        connection.commit()
        cursor.close()
        connection.close()

        driver.quit()

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        success_logger.info(f"[{timestamp}] Data scraped and stored successfully!")

    except Exception as e:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        failure_logger.error(f"[{timestamp}] Failed to scrape and store data. Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/fetch-data/")
def fetch_data():
    scrape_and_store_data()
    return {"message": "Scraping and storing process triggered successfully! To see scraped data use the'/get-all-data/' API endpoint"}


@app.get("/get-all-data/")
def get_all_data():
    try:
        # Retrieve data from the MySQL database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM scraped_data")
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
