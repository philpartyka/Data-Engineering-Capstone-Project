# Data-Engineering-Capstone-Project
This is a capstone project for the Data Engineering course offered by Per Scholas.


requirements:

pip install mysql-connector-python
pip install prettytable
pip install pandas
pip install folium
pip install seaborn
pip install matplotlib
pip install geopandas

credential file has to be updated with user's mysql details


challenges:
-prettytable was dropping leading 0s. thats because the zip codes are stored as ints in the db.  althought zerofill is enabled as a constraint in the db, that only affects how the number is displayed, not how it is stored.  had to pad a 0 in python when pulling the zip code out of the db.





To Do List:

MUST

-can i upload credentials file but scramble the login details






IF I HAVE TIME
- add comments to all code

- chart of the transaction total value for each of the categories (part 1 of req 3)

- parse prettytables using these functions istead of using json https://legacy.python.org/scripts/ht2html/docutils/parsers/rst/tableparser.py

-in the modify customer details menu restrict the state to being changed to one of the actual states, so that just any two letters arent acceptable
-consider adding filters like month to the transaction type filter view
-in the 7th requirment, when inputting a ssn, see which cc's belong to the customer and if there are more than one, have the user choice which cc to procceed with



-change format to pages.  have the pages have a common structure and refer to each page by its name/variable like page_zip_menu

-automate and make the entire process into a pipeline