## FastAPI Scraper with MySQL Integration and Logging

This project demonstrates a FastAPI web application that serves as a scraper for financial data from Yahoo Finance. The scraped data is then stored in a MySQL database, and the project utilizes logging to track the success and failure of the scraping and storing process.

### Prerequisites

Before running the application, make sure you have the following installed on your system:

- Python 3.9.x
- FastAPI
- uvicorn
- selenium
- mysql-connector-python

You can install the required packages using the following command:

```
pip install fastapi uvicorn selenium mysql-connector-python
```

### Setup

1. Clone the repository:

   ```
   git clone https://github.com/fazeelzafar/FastAPI-MySQL-Scraper.git
   ```

2. Change into the project directory:

   ```
   cd fastapi-mysql-scraper
   ```

3. Create a virtual environment (optional but recommended):

   ```
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```
     source venv/bin/activate
     ```

5. Update the database configuration in the `selenium_bot.py` file:

   Replace `'your_mysql_host'`, `'your_mysql_username'`, `'your_mysql_password'`, and `'your_mysql_database'` with your actual MySQL connection details in the `DB_CONFIG` dictionary.

### Running the Application

To run the FastAPI application, use the following command:

```
uvicorn selenium_bot:app --reload
```

The application will start the ASGI server and make the FastAPI app accessible at `http://127.0.0.1:8000`.

### API Endpoints

1. `/fetch-data/`: This endpoint triggers the scraper, scrapes the financial data from Yahoo Finance, and stores it in the MySQL database. The logs for success and failure are stored in `success.log` and `failure.log`, respectively.

2. `/get-all-data/`: This endpoint retrieves all the data from the MySQL database and returns it as a JSON response.

### Usage

1. To trigger the scraper and store data in the MySQL database, access the `/fetch-data/` endpoint in your web browser or use `curl` or Postman:

   ```
   curl http://127.0.0.1:8000/fetch-data/
   ```

2. To retrieve all the data stored in the MySQL database, access the `/get-all-data/` endpoint in your web browser or use `curl` or Postman:

   ```
   curl http://127.0.0.1:8000/get-all-data/
   ```

### Logging

The application uses the `logging` module to log the success and failure events of the scraping and storing process. The logs are stored in `success.log` and `failure.log` files, respectively.

### Cleanup

When you are done using the application, you can deactivate the virtual environment:

```
deactivate
```

---
That's it! You now have a FastAPI project that performs web scraping, stores data in a MySQL database, and uses logging to track the success and failure of the process. Feel free to customize the project as per your needs and requirements.