# webscrap
webscrap application for retrieving data from used-car platform. Data stored into a postgresql internal DB.
Flask web application to query scraped data. The web application also includes a price prediciton model.

- autocasion_scrapv2.py --> python web scraping application.
- autocasion220519.csv --> csv file with large data set to test the web application.
- application.py --> flask application.
- offer.py --> class offer for creating postgresql table.
- create_table.py --> create offers table in postrgesql DB.
- load_data.py --> load data into offers table.
- models.py --> price predicion model.
- templates --> front end files --> html files "index.html" and "resultados.html" both running javascript code.
static --> css files.

1. Run webscrap application --> run autocasion_scrapv2.py. 30 pages scrap by default. Modify var. "pages" to scrap more/less data.
2. Create table psql DB --> run create_table.py. Modify import csv file name by "autocasion220519.csv".
3. Load_data into psql DB --> run load_data.py.
4. run web application --> run application.py with flask.
