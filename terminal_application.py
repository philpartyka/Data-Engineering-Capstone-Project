import re
import mysql.connector as msql
from mysql.connector import Error
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

def zipcode_results(zip_code):
    sql = (
        "SELECT cc.TIMEID, cc.TRANSACTION_VALUE, cc.TRANSACTION_TYPE, cc.CUST_CC_NO, "
        "c.FIRST_NAME, c.LAST_NAME,  cc.BRANCH_CODE, cc.TRANSACTION_ID "
        "FROM cdw_sapp_credit_card cc "
        "INNER JOIN cdw_sapp_customer c ON cc.CUST_SSN = c.SSN "
        f"WHERE c.CUST_ZIP = {zip_code} "
        "ORDER BY cc.TIMEID DESC")
    cursor.execute(sql)
    # Fetch all the records
    result = cursor.fetchall()
    for i in result:
        print(i)

def run_zipcode_search():
    print("")
    print("\033[4mTransactional Details by Zip Code\033[0m")
    instructions()
    print("")

    while True:
        zip_code = input("Please enter a zip code: ")


        if zip_code == "exit":
            break
        elif bool(re.match(r"^\d{5}$", zip_code)):
            instructions()
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