import re
import mysql.connector as msql
from mysql.connector import Error
from prettytable import PrettyTable
from prettytable import from_db_cursor
# This file contains our login information for the MySQL server
import credentials as C


def connect_sql():
    try:
        global conn
        conn = msql.connect(host = C.host_name, database = 'creditcard_capstone', 
                          user = C.user_name, password = C.password)
        if conn.is_connected():
            global cursor
            global record
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
    except Error as e:
        print('Error while connecting to MySQL',e)

def instructions():
    print("Please type in your selection and hit Enter. ")
    print("Type \033[33mexit\033[0m to escape the program or to return to the previous menu")
    # \033 is an ANSI escape character. [ starts the code you want to enter and 33 represents the
    # color code.  m is used for text color changes.  background and foreground color changes don't use m.
    # we need to close it out with \033[0m to stop the color change from spilling over into the rest of
    # the text.  0m in this case is the default color.

def main_menu():
    print("Possible selections are highlighted in yellow.")
    print(" ")
    print("\033[4mTransaction Details\033[0m")
    print("\033[33m1\033[0m Filter transactions by zip code")
    print("\033[33m2\033[0m Filter by type of transaction")
    print("\033[33m3\033[0m Filter total transactions by Branch Code")
    print(" ")
    print("\033[4mCustomer Details\033[0m")
    print("\033[33m4\033[0m Check account details of a customer")
    print("\033[33m5\033[0m Modify customer account details")
    print("\033[33m6\033[0m Generate monthly statement for a credit card")
    print("\033[33m6\033[0m Display total transactions between two dates from an individual")
    print("")

def end_of_options():
    print("You have exhausted all options.  Returning to previous page.")
def zip_sql(zip_code, month="%%", year="____"):
    sql = ( "SELECT cc.TIMEID, cc.TRANSACTION_VALUE, cc.TRANSACTION_TYPE, cc.CUST_CC_NO, "
            "c.FIRST_NAME, c.LAST_NAME,  cc.BRANCH_CODE, cc.TRANSACTION_ID "
            "FROM cdw_sapp_credit_card cc "
            "INNER JOIN cdw_sapp_customer c ON cc.CUST_SSN = c.SSN "
            f"WHERE c.CUST_ZIP = {zip_code} AND cc.TIMEID LIKE '____{month}%' "
            "ORDER BY cc.TIMEID DESC")
    cursor.execute(sql)   #cursor was assigned in the connect_sql() function
    result = cursor.fetchall()          #fetches all the results
    
    # if the zip code isn't in the records I want to terminate the lookup and display
    # procedure so we will return 0 and then handle the 0 value in zipcode_results()
    if len(result) == 0:
        return 0
    zip_tb = PrettyTable(["Time(YYYYMMDD)","Total","Type","CC Number",
                        "First Name","Last Name","Branch","Trans ID"])
    for i in result:
        zip_tb.add_row(i)
    
    # Another method to create the prettyTable is to asigned the cursor directly 
    # to the prettytable with the from_db_cursor() function.  But I can't control
    # the column names with this method.
    # zip_tb = from_db_cursor(cursor)
    return zip_tb

def zipcode_results(zip_code):
    zip_results = zip_sql(zip_code)
    # If the zip_sql() returns a 0 because the zip codes has no records then we will terminate
    # the process and the user will be returned to the beginning of the zipcode_search()
    if zip_results == 0:
        print("There are no transactions for the zip code you have selected. ")
    else:
        print("")
        print("Showing the top 10 results")
        print(zip_results[0:10])
        print("")
        # setting these to 0 indicates that the full results option hasn't been selected.
        # When the full results are being shown on screen I don't want the "Show full results"
        # option to be available.  error_raised gets set to 1 when the user starts at the 
        # top of the while due to an input error.  since there aren't any results on screen 
        # after such an error there should be no option to view the full results.
        full_results_shown = 0
        error_raised = 0

        while True:
            instructions()
            print("Possible selections are highlighted in yellow.")
            print(" ")
            #if the full results are being shown I want to block this option 
            if full_results_shown == 0 and error_raised == 0:
                print("\033[33m1\033[0m View full results")
            else:
                print("\033[30m1 View full results\033[0m")
            print("\033[33m2\033[0m Filter results by Month")
            print("\033[33m3\033[0m Filter results by Year")
            print("\033[33m4\033[0m Search another zip code")
            print(" ")
            choice = input("Your selection: ")

            if choice == "exit":
                error_raised = 0
                print("Going back to the previous page")
                break
            elif choice == "1" and full_results_shown == 0 and error_raised == 0:
                print(zip_results)
                error_raised = 0
                full_results_shown = 1
                continue
            elif choice == "2":
                month = input("Please enter the month's number (1-12): ")
                # Regex pattern: "^(0?[1-9]|1[0-2])$".  We need ^ to indicate that we are looking for 
                # the pattern at the start of a string, not in the middle of it.  Similar reason for the $ 
                # but for the end of the string.  0?[1-9] matches a single digit from 1-9 with an optional
                # leading zero.  | is an OR operator.  1[0-2] matches 10, 11, or 12.
                if bool(re.match(r"^(0?[1-9]|1[0-2])$", month)):
                    month = month.rjust(2,"0")  #padding a leading zero if single digit
                    print(zip_sql(zip_code, month))
                    # changing full_results_shown to 1 because results will be fully shown automatically
                    error_raised = 0
                    full_results_shown = 1
                elif month == "exit":
                    print("Returning to previous page")
                    print("")
                    continue
                else:
                    error_raised = 1
                    print("\033[31mERROR\033[0m You have made an invalid selection. 1-12 or 01-09 are valid.")
                    print("")
                continue
            elif choice == "3":
                year = input("Please enter the year (YYYY).  Hint: only 2018 data is available: ")
                if year == "2018":
                    print(zip_sql(zip_code, year=year))
                    # changing full_results_shown to 1 because results will be fully shown automatically
                    error_raised = 0
                    full_results_shown = 1
                elif year == "exit":
                    print("Returning to previous page")
                    print("")
                    continue
                else:
                    error_raised = 1
                    print("\033[31mERROR\033[0m You have made an invalid selection. Only 2018 is valid.")
                    print("")


                error_raised = 0
                continue
            elif choice == "4":
                error_raised = 0
                break
            else:
                error_raised = 1
                print("\033[31mERROR\033[0m You have made an invalid selection.  Please try again.")
                print("")
            


def run_zipcode_search():
    while True:
        print("")
        print("\033[4mTransactional Details by Zip Code\033[0m")
        instructions()
        print("")
        zip_code = input("Please enter a zip code: ")

        if zip_code == "exit":
            break
        elif bool(re.match(r"^\d{5}$", zip_code)):
            zipcode_results(zip_code)
        elif bool(re.match(r"^\d{5}$", zip_code)) == False:
            print(f"You entered {zip_code} which is not a correct zip code.")
            print("Remember zip codes have exactly 5 numbers and numbers only.")
        else:
            print("Congrats, you managed to break the application.  I have no idea how you did it.")
            break

def run_choice(choice):
    if choice == "1":
        run_zipcode_search()
    




def app():
    while True:
        instructions()
        main_menu()

        choice = input("Your selection: ")

        run_choice(choice)

        if choice == "exit":
            print("Closing program.  Come back next time.")
            break


connect_sql()
print("              ---")
print("Welcome to the Credit Card App")
print("              ---")
app()