# Data Engineering Capstone Project
This is my data engineering capstone project for the boot camp course offered by Per Scholas.  The main goal of this project is to extract credit card transaction, cutomer, branch, and loan data from a dataset, clean it up, load it onto a database, provide analysis on the data, and build a front-end to interact with the data.

## Main objectives and Tools Used
1. Extract data from 3 provided datasets, clean data, and load into a database.  The datasets cover Credit Card Transactions, Bank Branch information, and Customer information.  Tools used:
   * PySpark for extracting and cleaning
   * MySQL database
2. Build a front end python console application to pull up and modify data from the db based on front end user parameters.
   * MySQL connector library
   * PrettyTable library
3. Provide visualizations of data based on sample analysis scenarios
   * Seaborn
   * MatPlotLib
   * Folium and GeoPandas
4. Pull Loan Application data from an API endpoint and store it in the database
   * PySpark SQL
   * MySQL database
5. Provide visualizations based on sample analysis scenarios using loan data loaded in from step 4 
   * Pandas
   * Seaborn
   * MatPlotLib  


## Requirements to run this repo
* The requirements.txt file contains all the python libraries needed to run this project in a virtual environment.  I would recommend running the project in a venv in order to avoid any version and installation conflicts.
* While the requirements.txt files contains that pyspark 3.4 library, you will need to install spark on your system in order for this library to function.
* The credentials.py file contains the information needed to log into the MySQL db.  These will need to be changed to accomodate your database.
* I used an area code dataset that was too big of a filesize to upload to this repo but it can be downloaded from here: https://github.com/djbelieny/geoinfo-dataset/blob/master/full_dataset_json.zip

## Technical Challenges

### 1. The Data
This may have been one of the worst datasets I have ever seen.  If I was given this data in a real situation I would give it back and tell them to give me better data.  There were so many issues and most had no viable solutions, because the data couldn't be possible in real life.

Major Issues:
* The bank branch data had incomplete zip codes because the leading 0 was dropped from the zip codes.  This wasn't difficult to solve using a spark dataframe.  The issue was that the mapping document (formatting guidelines for how the data was to be transformed and loaded into the db) wanted the zip codes to be stored as an INT data type.  Loading in the zip codes as INTs led to the leading 0s to be dropped again.  Not a big deal since there is an INT ZEROFILL constraint we can use to fill the number with 0s.  The problem is that this constraint doesn't actually changed the number that is stored, just how its displayed, so when we query zip code data from the db we will received incomplete zip codes again.  The best solution to avoid this entire mess would be to store the Zip Codes as strings, but you know, I was just following what I was instructed to do.
* Customer phone numbers were incomplete (only 7 digits) and there were nearly 50 duplicate phone numbers.  Since the branches' phone numbers all used 123 as an area code, initially, I was going to use that as the area code for the customers' phone numbers but I would still have duplicate numbers in that situation.  It not possible for two unrelated customers in different parts of the country to have the same phone number so I decided to add area codes based on the zip code of the customer.  To accomplish this, I needed a dataset with the area codes corresponding to a zip code, which proved suprisingly difficult to find (for free).  After finally finding a dataset, I thought it would be easy to just add an area code to each customer based on their zip codes but that proved to be false because many zip codes had multiple area codes that could be an option, not to mention the non geographic area zip codes that might be possible.  To solve this issue I cycled through the list of area codes for a specific zip codes so that the area codes would be evenly distributed among the customers that shared the same zip code.  This wasn't easy to accomplish using a spark dataframe, since overwriting a single cell in a spark df is incredible inefficient.  After I finally figured out how to do it, it took over 20 minutes and still wasn't done processing the data for a 950 row dataframe.  I changed it to a pandas dataframe and it took 6 seconds to finish.
* 


Minor Issues:
* The phone numbers for the branches all start with 123.  That's not possible since area codes start from 201 and up.
* While there were 46k+ credit card transactions, all the transactions were evenly distributed between all the categories, timespans, and customers.  This made analysis and visualization almost useless.
* 



challenges:
-prettytable was dropping leading 0s. thats because the zip codes are stored as ints in the db.  althought zerofill is enabled as a constraint in the db, that only affects how the number is displayed, not how it is stored.  had to pad a 0 in python when pulling the zip code out of the db.





To Do List:

MUST

-can i upload credentials file but scramble the login details






IF I HAVE TIME
- add comments to all code

- figure out how to zip big data file

- chart of the transaction total value for each of the categories (part 1 of req 3)

- parse prettytables using these functions istead of using json https://legacy.python.org/scripts/ht2html/docutils/parsers/rst/tableparser.py

-in the modify customer details menu restrict the state to being changed to one of the actual states, so that just any two letters arent acceptable
-consider adding filters like month to the transaction type filter view
-in the 7th requirment, when inputting a ssn, see which cc's belong to the customer and if there are more than one, have the user choice which cc to procceed with



-change format to pages.  have the pages have a common structure and refer to each page by its name/variable like page_zip_menu

-automate and make the entire process into a pipeline

-docker to containerize the entire environment

