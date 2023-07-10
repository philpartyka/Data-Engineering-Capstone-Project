# Data Engineering Capstone Project
This is my data engineering capstone project for the boot camp course offered by Per Scholas.  The main goal of this project is to extract credit card transaction, cutomer, branch, and loan data from a dataset, clean it up, load it onto a database, provide analysis on the data, and build a front-end to interact with the data.

## Main Objectives and Tools Used
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

## Notes about the files in this repo
* The files with a leading number (1-5) corresspond to the nubmers outlined in the Main Objections section above.
* The source data directory contains the 3 datasets I was suplied with (files preceeded by cdw).  The area_codes.json file contains the cleaned up area code data that I used to generate the area codes for the customer's phone numbers.  The full_area_code_dataset.zip is the full area code dataset in a zipped up form because it was too big to be uploaded to github in its raw state.  The states.geojson file contains the US states geo data for use in the folium data visualization (section 3).
* The clean data directory contains the datasets after they had been transformed and cleaned in step 1.
* The cc_db.sql contains the sql script to create and populate the entire MySQL database that I created and loaded during the steps in this project.
* Credentials.py contains the login information for the MySQL database.  It isn't included in the repo because it contains sensitive information.  You will have to create your own credentials.py file with this format:
```
host_name = xxxxxx (for example, localhost was mine)
user_name = xxxxxx
password = xxxxxx
port = xxxxxx
```

## Technical Challenges

### 1. The Data
This may have been one of the worst datasets I have ever seen.  If I was given this data in a real situation I would give it back and tell them to give me better data.  There were so many issues and most had no viable solutions, because the data couldn't be possible in real life.

Major Issues:
* The bank branch data had incomplete zip codes because the leading 0 was dropped from the zip codes.  This wasn't difficult to solve using a spark dataframe.  The issue was that the mapping document (formatting guidelines for how the data was to be transformed and loaded into the db) wanted the zip codes to be stored as an INT data type.  Loading in the zip codes as INTs led to the leading 0s to be dropped again.  Not a big deal since there is an INT ZEROFILL constraint we can use to fill the number with 0s.  The problem is that this constraint doesn't actually changed the number that is stored, just how its displayed, so when we query zip code data from the db we will received incomplete zip codes again.  The best solution to avoid this entire mess would be to store the Zip Codes as strings, but you know, I was just following what I was instructed to do.
* Customer phone numbers were incomplete (only 7 digits) and there were nearly 50 duplicate phone numbers.  Since the branches' phone numbers all used 123 as an area code, initially, I was going to use that as the area code for the customers' phone numbers but I would still have duplicate numbers in that situation.  It not possible for two unrelated customers in different parts of the country to have the same phone number so I decided to add area codes based on the zip code of the customer.  To accomplish this, I needed a dataset with the area codes corresponding to a zip code, which proved suprisingly difficult to find (for free).  After finally finding a dataset, I thought it would be easy to just add an area code to each customer based on their zip codes but that proved to be false because many zip codes had multiple area codes that could be an option, not to mention the non geographic area zip codes that might be possible.  To solve this issue I cycled through the list of area codes for a specific zip codes so that the area codes would be evenly distributed among the customers that shared the same zip code.  This wasn't easy to accomplish using a spark dataframe, since overwriting a single cell in a spark df is incredible inefficient.  After I finally figured out how to do it, it took over 20 minutes and still wasn't done processing the data for a 950 row dataframe.  I changed it to a pandas dataframe and it took 6 seconds to finish.
* Customer email addresses also had 24 duplicates.  Since the emails were all formatted as FirstInitialLastName@, I added the middle initial to differentiate them further.  Emails really shouldn't be altered since they only function when written a single way, but since its been established that a lot of this data is made up anyways, then I think we can bend the laws of reality a bit here.

Minor Issues:
* The mapping document instructed me to add the Apt No after the street name.  The street names had no leading numbers that would indicate the house number where the customer lives.  Since each customer had an APT NO, I assumed that the APT NO was actually supposed to be the house number so I put it in front of the street name instead.  And since I can't be accussed of unfulfilling my mapping duties I also put the Apt No after the street name, like instructed.  I'll let the postman deal with this mess.
* The phone numbers for the branches all start with 123.  That's not possible since area codes start from 201 and up.
* While there were 46k+ credit card transactions, all the transactions were evenly distributed between all the categories, timespans, and customers.  This made analysis and visualization almost useless.


### 2. The front-end console application

While the console application wasn't challengeing for my programming abilities, it was challenging due to the all the "paths" I had to account for that the end user could go down.  I had to make sure the end user never got stuck on a section of the application where they had no way to back out. 
 I also had to make sure data was carried over from one section to another when necessary, also the data had to persist even if the user aborted or caused an error in a section of the application.  The really challenging part was keeping track of all the possible outcomes the end user might end up.  I wish I had outlined it ahead of time instead of tracking it in my head the entire time.  Also, I plan to revisit the code for this application in the future so I could make better use of UDFs to cut down on redundant code.  

 





