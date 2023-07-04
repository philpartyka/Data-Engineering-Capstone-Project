import time
import re
import json
import mysql.connector as msql
from mysql.connector import Error
from prettytable import PrettyTable
from prettytable import from_db_cursor
# This file contains our login information for the MySQL server
import credentials as C

def startup_sequence():
    print(".")
    time.sleep(0.5)
    print("..")
    time.sleep(0.5)
    print("Starting up application..")
    time.sleep(0.8)
    print("Importing required python libraries")
    time.sleep(1)
    print("Libraries fulled loaded")
    time.sleep(1)
    print("Checking to see if the stove was left on")
    time.sleep(1)
    print("Checking if there are any updates to the application")
    time.sleep(0.8)
    print(".")
    time.sleep(0.4)
    print("..")
    time.sleep(0.4)
    print("JK, there is no update check feature")
    time.sleep(1)
    print("Connecting to the database")
    time.sleep(1)
    connect_sql()

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

def welcome_title():
    pad = "        "
    print("")
    print(pad + " _____________________________________ ")
    print(pad + "|                                     |")
    print(pad + "|                                     |")
    print(pad + "|                                     |")
    print(pad + "|  CREDIT CARD APPLI CATION           |")
    print(pad + "|                                     |")
    print(pad + "|  EST 07/23                          |")
    print(pad + "|  PHILIP PARTYKA              BISA   |")
    print(pad + "|_____________________________________|")
    print("")
    
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
    print("\033[33m3\033[0m Filter by States of Branches")
    print(" ")
    print("\033[4mCustomer Details\033[0m")
    print("\033[33m4\033[0m Check account details of an individual customer")
    print("\033[33m5\033[0m Modify customer account details")
    print("\033[33m6\033[0m Generate monthly statement for a credit card")
    print("\033[33m7\033[0m Display total transactions between two dates from an individual")
    print("")

def end_of_options():
    print("You have exhausted all options.  Returning to previous page.")

def zip_sql(zip_code, month="%%", year="____"):
    sql = ( "SELECT cc.TIMEID, cc.TRANSACTION_VALUE, cc.TRANSACTION_TYPE, cc.CUST_CC_NO, "
            "c.FIRST_NAME, c.LAST_NAME,  cc.BRANCH_CODE, cc.TRANSACTION_ID "
            "FROM cdw_sapp_credit_card cc "
            "INNER JOIN cdw_sapp_customer c ON cc.CUST_SSN = c.SSN "
            f"WHERE c.CUST_ZIP = {zip_code} AND cc.TIMEID LIKE '____{month}%' "
            f"AND cc.TIMEID LIKE '{year}%' "
            "ORDER BY cc.TIMEID DESC")
    cursor.execute(sql)   #cursor was assigned in the connect_sql() function
    result = cursor.fetchall()          #fetches all the results
    
    # if the zip code isn't in the records I want to terminate the lookup and the display
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
                print("Returning to previous page")
                break
            elif choice == "1" and full_results_shown == 0 and error_raised == 0:
                print(zip_results)
                error_raised = 0
                full_results_shown = 1
                continue
            elif choice == "2":
                while True:
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
                        break
                    else:
                        error_raised = 1
                        print("\033[31mERROR\033[0m You have made an invalid selection. 1-12 or 01-09 are valid.")
                        print("")
                continue
            elif choice == "3":
                while True:
                    year = input("Please enter the year (YYYY).  Hint: only 2018 data is available: ")
                    if year == "2018":
                        print(zip_sql(zip_code, year=year))
                        # changing full_results_shown to 1 because results will be fully shown automatically
                        error_raised = 0
                        full_results_shown = 1
                    elif year == "exit":
                        print("Returning to previous page")
                        print("")
                        break
                    else:
                        error_raised = 1
                        print("\033[31mERROR\033[0m You have made an invalid selection. Only 2018 is valid.")
                        print("") 
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
            print("")
            break
        elif bool(re.match(r"^\d{5}$", zip_code)):
            zipcode_results(zip_code)
        elif bool(re.match(r"^\d{5}$", zip_code)) == False:
            print("You have entered an invalid zip code.")
            print("Remember zip codes have exactly 5 numbers and numbers only.")
        else:
            print("Congrats, you managed to break the application.  I have no idea how you did it.")
            break

def run_type_filter():
    print("")
    print("\033[4mTransactional Details by Transaction Type\033[0m")
    print("")

    type_count_sql=("SELECT TRANSACTION_TYPE, count(TRANSACTION_TYPE), sum(TRANSACTION_VALUE) "
                    "FROM cdw_sapp_credit_card "
                    "GROUP BY TRANSACTION_TYPE "
                    "ORDER BY TRANSACTION_TYPE")
    cursor.execute(type_count_sql)   #cursor was assigned in the connect_sql() function
    result = cursor.fetchall()  
    type_display_table = PrettyTable(["", "Type", "Transactions", "Total"])

    for i,row in enumerate(result):
        # unpacking the row (its a tuple) so that I can modify the individual elements
        type, transactions, total = row
        # below formats the total into a currency format.  The $ is a literal dollar sign.
        # the : indicates the start of the format specification.  The , indicates that 
        # a comma should be used as a thousand separator, and the .2f indicates we
        # want only two decimals places
        formatted_total = '${:,.2f}'.format(total)
        type_display_table.add_row([i+1,type, transactions, formatted_total])
    
    print(type_display_table)
    print("")

def branch_full_table(state=None, branch_code=None):
    branch_full_sql = ("SELECT b.BRANCH_CODE, b.BRANCH_NAME, b.BRANCH_CITY, b.BRANCH_STATE, "
                        "b.BRANCH_ZIP, b.BRANCH_PHONE, sum(c.TRANSACTION_VALUE), "
                        "count(c.TRANSACTION_VALUE) "  
                        "FROM cdw_sapp_branch b " 
                        "JOIN cdw_sapp_credit_card c USING (BRANCH_CODE) "
                        "GROUP BY b.BRANCH_CODE, b.BRANCH_NAME, b.BRANCH_CITY, b.BRANCH_STATE, " 
                        "b.BRANCH_ZIP, b.BRANCH_PHONE "
                        "ORDER BY b.BRANCH_CODE")
    cursor.execute(branch_full_sql)   #cursor was assigned in the connect_sql() function
    result = cursor.fetchall()

    branch_tb = PrettyTable(["Branch Code","Name","City","State","Zip Code","Phone No",
                             "Total","Transactions"])
    for row in result:
        # unpacking the row (its a tuple) so that I can modify the individual elements
        code, name, city, state, zip, phone, total, trans = row
        
        # padding a leading 0 to the zip code(needs to be converted from int to string)
        zip = str(zip).rjust(5,"0")
        
        # below formats the total into a currency format.  The $ is a literal dollar sign.
        # the : indicates the start of the format specification.  The , indicates that 
        # a comma should be used as a thousand separator, and the .2f indicates we
        # want only two decimals places
        formatted_total = '${:,.2f}'.format(total)
        branch_tb.add_row([code, name, city, f"\033[33m{state}\033[0m", zip, phone, total, trans])
    
    return branch_tb      

def branch_state_table(state):
    state = state.upper()
    branch_state_sql = ("SELECT b.BRANCH_STATE, sum(c.TRANSACTION_VALUE), count(c.TRANSACTION_VALUE) "  
                        "FROM cdw_sapp_branch b " 
                        "JOIN cdw_sapp_credit_card c USING (BRANCH_CODE) "
                        f"WHERE b.BRANCH_STATE = '{state}' "
                        "GROUP BY b.BRANCH_STATE")
    cursor.execute(branch_state_sql)    #cursor was assigned in the connect_sql() function
    result = cursor.fetchall()          #fetches all the results
    
    # if the state isn't in the records I want to terminate the lookup and the display
    # procedure so we will return 0 and then handle the 0 value in zipcode_results()
    if len(result) == 0:
        return 0
    
    branch_state_tb = PrettyTable(["State","Total","Transactions"])

    for row in result:

        # unpacking the tuple (row) so I can manipulate each element of the row
        st, tot, trans = row

        # below formats the total into a currency format.  The $ is a literal dollar sign.
        # the : indicates the start of the format specification.  The , indicates that 
        # a comma should be used as a thousand separator, and the .2f indicates we
        # want only two decimals places
        formatted_tot = '${:,.2f}'.format(tot)
        branch_state_tb.add_row([st,formatted_tot,trans])
    
    return branch_state_tb

def run_branch_filter():
    print("")
    print("\033[4mTransactional Details for Branches\033[0m")
    instructions()
    print("")
    branch_full_results_shown = 0

    while True:
            print("Possible selections are highlighted in yellow.")
            print("")

            if branch_full_results_shown == 0:
                print("\033[33m1\033[0m View full list of Branches")
            else:
                print("\033[30m1 View full list of Branches\033[0m")
            print("\033[33m2\033[0m View transactions by State")
            branch_choice = input("Your selection: ")

            if branch_choice == "exit":
                print("Returning to previous page")
                print("")
                break
            elif branch_choice == "1" and branch_full_results_shown == 0:
                print(branch_full_table())
                branch_full_results_shown = 1
            elif branch_choice == "2":
                while True:
                    branch_full_results_shown = 0
                    state_choice = input("Please enter a state abbreviation: ")
                    
                    if bool(re.match(r"^[A-Za-z]{2}$", state_choice)):
                        #assigning to variable so I dont run query twice
                        state_results = branch_state_table(state_choice)
                        if state_results == 0:
                            print("Sorry there are no branches in that state.")
                            continue
                        else:
                            print(state_results)
                    elif state_choice == 'exit':
                        break
                    else:
                        print("\033[31mERROR\033[0m Sorry that was an invalid selection.")
            else:
                print("\033[31mERROR\033[0m You have made an invalid selection.  Please try again.")
                print("")

def cust_details_sql(ssn=None,cc_num_last4=None,cc_num_full=None,l_name=None,cust_state=None,zip_code=None):
    # I will alter the sql query based on which search parameter is supplied.  Only one param
    # is supplied at a time so the rest will be None by default.
    if ssn:
        search_param = f"WHERE SSN = {ssn}"
    elif cc_num_last4:
        search_param = f"WHERE Credit_card_no LIKE '____________{cc_num_last4}'"
    elif cc_num_full:
        search_param = f"WHERE Credit_card_no = {cc_num_full}"
    elif l_name:
        search_param = f"WHERE LAST_NAME = '{l_name}'"
    elif cust_state:
        search_param = f"WHERE CUST_STATE = '{cust_state}'"
    elif zip_code:
        search_param = f"WHERE CUST_ZIP = {zip_code}"

    cust_details_sql = ("SELECT * "
                        "FROM cdw_sapp_customer "
                        f"{search_param}")
    cursor.execute(cust_details_sql)    #cursor was assigned in the connect_sql() function
    result = cursor.fetchall()          #fetches all the results
    
    # if the ssn isn't in the records I want to terminate the lookup and the display
    # procedure so we will return 0 and then handle the 0 value in zipcode_results()
    if len(result) == 0:
        return 0
    
    cust_details_tb = PrettyTable(["SSN","First","Middle","Last","CC Num","Street Address",
                                   "City","State","Country","Zip Code","Phone Num","Email","Last Updated"])
    for i in result:
        # need to convert tuple to list in order to change individual elements
        i = list(i)
        # padding a leading 0 to the zip code(needs to be converted from int to string)
        i[9] = str(i[9]).rjust(5,"0")
        cust_details_tb.add_row(i)
    
    return cust_details_tb

def run_cust_details(modify=False):
    while True:
        print("")
        # I am using this same function in run_modify_cust_details() but I don't 
        # want to change the title and instructions when its in that function
        if modify == False:
            print("\033[4mIndividual Customer Details\033[0m")
        else:
            print("\033[4mModify Customer Details\033[0m")
            print("Please choose a customer to modify.  Search for the customer via one of the methods below.")
            print("")
        instructions()
        print("Possible selections are highlighted in yellow.")
        print("")

        print("\033[33m1\033[0m Search by SSN")
        print("\033[33m2\033[0m Search by last four digits of CC No.")
        print("\033[33m3\033[0m Search by Last Name")
        print("\033[33m4\033[0m Search by State")
        print("\033[33m5\033[0m Search by Zip Code")
        print(" ")
        cust_choice = input("Your selection: ")
        
        # need to make this variable global for the modify function to be able to use it
        global return_results
        global exit_from_cust_details
        exit_from_cust_details = 0
        break_from_function = 0

        if cust_choice == "exit":
            print("Returning to previous page")
            print("")
            exit_from_cust_details = 1
            break
        elif cust_choice == "1":
            while True:
                ssn_input = input("Please enter the customer's SSN: ")
                # We need to put the exit break statement here because we are eliminating non digit chars in the next step
                if ssn_input == "exit":
                    print("Returning to previous page")
                    break
                # below replaces any non digit characters (\D) with an empty string ""
                # essentially removing non digit chars
                ssn_input = re.sub(r"\D", "", ssn_input)
                
                #need to convert ssn_input to a string because int doesnt have a length function
                if len(str(ssn_input)) == 9:
                    #saving the sql query to a variable so we dont have to run it twice
                    ssn_results = cust_details_sql(ssn=ssn_input)
                    if ssn_results == 0:
                        print("There is no customer with the given SSN.")
                        print("")
                    else:
                        print(ssn_results)
                        # when running in the modify customers page we want to export the results table 
                        # to be used in that function.  Also we want to make sure its only the record of a
                        # single customer and not more than 1
                        if modify == True:
                            # We need to check if the results have more than 1 customer.  It's an ugly solution
                            # but ssn_results[1:][0] returns an error when there is only 1 result
                            try: 
                                ssn_results[1:][0]
                                print("\033[31mERROR\033[0m Your selection returns more than one customer.  You can only proceed with one customer.")
                            except:
                                return_results = ssn_results
                                break_from_function = 1
                                break
                else:
                    print("\033[31mERROR\033[0m You have made an invalid selection.  Remember SSNs have 9 digits.")
                    print("")
        elif cust_choice == "2":
            while True:
                cc_input = input("Please enter the last four digits of the CC number: ")
                # We need to put the exit break statement here because we are eliminating non digit chars in the next step
                if cc_input == "exit":
                    print("Returning to previous page")
                    break
                # below replaces any non digit characters (\D) with an empty string ""
                # essentially removing non digit chars
                cc_input = re.sub(r"\D", "", cc_input)
                
                #need to convert ssn_input to a string because int doesnt have a length function
                if len(str(cc_input)) == 4:
                    #saving the sql query to a variable so we dont have to run it twice
                    cust_results = cust_details_sql(cc_num_last4=cc_input)
                    if cust_results == 0:
                        print("There is no customer with the given last four CC digits.")
                        print("")
                    else:
                        print(cust_results)
                        # when running in the modify customers page we want to export the results table 
                        # to be used in that function.  Also we want to make sure its only the record of a
                        # single customer and not more than 1
                        if modify == True:
                            # We need to check if the results have more than 1 customer.  It's an ugly solution
                            # but cust_results[1:][0] returns an error when there is only 1 result
                            try: 
                                cust_results[1:][0]
                                print("\033[31mERROR\033[0m Your selection returns more than one customer.  You can only proceed with one customer.")
                            except:
                                return_results = cust_results
                                break_from_function = 1
                                break
                else:
                    print("\033[31mERROR\033[0m You have made an invalid selection.  Remember to only enter the last 4 digits.")
                    print("")
        elif cust_choice == "3":
            while True:
                name_input = input("Please enter the customer's last name: ")
                name_results = cust_details_sql(l_name=name_input)
                
                if name_input == "exit":
                    print("Returning to previous page")
                    break
                elif name_results != 0:
                    print(name_results)
                    # when running in the modify customers page we want to export the results table 
                    # to be used in that function.  Also we want to make sure its only the record of a
                    # single customer and not more than 1
                    if modify == True:
                        # We need to check if the results have more than 1 customer.  It's an ugly solution
                        # but name_results[1:][0] returns an error when there is only 1 result
                        try: 
                            name_results[1:][0]
                            print("\033[31mERROR\033[0m Your selection returns more than one customer.  You can only proceed with one customer.")
                        except:
                            return_results = name_results
                            break_from_function = 1
                            break
                else:
                    print("\033[31mERROR\033[0m You have made an invalid selection or there are no such customers.")
                    print("")
        elif cust_choice == "4":
            while True:
                state_input = input("Please enter the State (2 letter abbreviation): ")

                if bool(re.match(r"^[A-Za-z]{2}$", state_input)):
                    state_results = cust_details_sql(cust_state = state_input)
                    if state_results == 0:
                        print("Sorry there are no customers in that state.")
                        continue
                    else:
                        print(state_results)
                        # when running in the modify customers page we want to export the results table 
                        # to be used in that function.  Also we want to make sure its only the record of a
                        # single customer and not more than 1
                        if modify == True:
                            # We need to check if the results have more than 1 customer.  It's an ugly solution
                            # but state_results[1:][0] returns an error when there is only 1 result
                            try: 
                                state_results[1:][0]
                                print("\033[31mERROR\033[0m Your selection returns more than one customer.  You can only proceed with one customer.")                            
                            except:
                                return_results = state_results
                                break_from_function = 1
                                break
                elif state_input == "exit":
                    print("Returning to previous page")
                    break
                else:
                    print("\033[31mERROR\033[0m You have made an invalid selection.  Remember to only enter two letters.")
                    print("")
        elif cust_choice == "5":
            while True:
                zip_input = input("Please enter the customer's zip code: ")
                # We need to put the exit break statement here because we are eliminating non digit chars in the next step
                if zip_input == "exit":
                    print("Returning to previous page")
                    break
                # below replaces any non digit characters (\D) with an empty string ""
                # essentially removing non digit chars
                zip_input = re.sub(r"\D", "", zip_input)
                
                #need to convert zip_input to a string because int doesnt have a length function
                if len(str(zip_input)) == 5:
                    #saving the sql query to a variable so we dont have to run it twice
                    zip_results = cust_details_sql(zip_code=zip_input)
                    if zip_results == 0:
                        print("There is no customer in that zip code.")
                        print("")
                    else:
                        print(zip_results)
                        # when running in the modify customers page we want to export the results table 
                        # to be used in that function.  Also we want to make sure its only the record of a
                        # single customer and not more than 1
                        if modify == True:
                            # We need to check if the results have more than 1 customer.  It's an ugly solution
                            # but zip_results[1:][0] returns an error when there is only 1 result
                            try: 
                                zip_results[1:][0]
                                print("\033[31mERROR\033[0m Your selection returns more than one customer.  You can only proceed with one customer.")
                            except:
                                return_results = zip_results
                                break_from_function = 1
                                break
                else:
                    print("\033[31mERROR\033[0m You have made an invalid selection.  Remember zip codes have 9 digits.")
                    print("")




            error_raised = 0
            full_results_shown = 1
            continue
        else:
            print("\033[31mERROR\033[0m You have made an invalid selection.  Please try again.")
        # if we are running this in the modify customers function we want to break from this while loop
        # and reset the break_from_function variable in case this function is run again.
        if break_from_function == 1:
            break_from_function = 0
            break        

def cust_update_sql(cust_ssn, col, new_val):
    try:
        # setting it this way is advised to prevent sql injection attacks. 
        params = (new_val, cust_ssn)
        cust_modify_sql =  f"UPDATE cdw_sapp_customer SET {col} = %s, LAST_UPDATED = CURRENT_TIMESTAMP WHERE SSN = %s" 
        
        cursor.execute(cust_modify_sql, params) #cursor was assigned in the connect_sql() function
        conn.commit()
        
        # fetching the results of the updated customer details.  we will be passing the 
        # PK cust_ssn.  but if cust_ssn was changed in the previous step then we will be passing
        # in the new ssn
        if col == 'SSN':
            show_changes_sql = f"SELECT * FROM cdw_sapp_customer WHERE SSN = {new_val}"
        else:
            show_changes_sql = f"SELECT * FROM cdw_sapp_customer WHERE SSN = {cust_ssn}"
        
        cursor.execute(show_changes_sql)
        result = cursor.fetchall()          #fetches the results
        
        cust_details_tb = PrettyTable(["SSN","First","Middle","Last","CC Num","Street Address",
                                    "City","State","Country","Zip Code","Phone Num","Email","Last Updated"])
        for i in result:
            # need to convert tuple to list in order to change individual elements
            i = list(i)
            # padding a leading 0 to the zip code(needs to be converted from int to string)
            i[9] = str(i[9]).rjust(5,"0")
            #had to slice the row to omit the 13th column from being added
            cust_details_tb.add_row(i)
        
        return cust_details_tb
    except msql.Error as error:
        return f"\033[31mERROR\033[0m Failed to update table record: {error}"
         
def run_modify_cust_details():
    # run the same cust details function but with slight tweaks catered to this function
    run_cust_details(modify=True)
    
    exit_check = exit_from_cust_details
    if exit_check == 1:
        return 
    # We need to isolate the SSN so we can use it to lookup customers when updating their
    # records.  To achieve this we use the json library to convert the prettytable
    # to a json string(its actually a list) and then we extract the dict in that list.  
    # The first item in that dict is the SSN value.
    # I needed to remove the Last Updated column because the timestamp data type couldn't
    # be serialized in json
    return_results.del_column('Last Updated')
    json_data = json.loads(return_results.get_json_string())
    cust_dict = json_data[1]
    cust_ssn = cust_dict['SSN']
    
    while True:
        # checks if we backed out of the cust details search, so we can break this loop as well
        # for some reason i can't put exit_from_cust_details directly in the if conditional. 
        
                       
        print("Which field would you like to modify?")
        print("")
        instructions()
        print("Possible selections are highlighted in yellow.")
        print("")

        print("\033[33m1\033[0m SSN")
        print("\033[33m2\033[0m First Name")
        print("\033[33m3\033[0m Middle Name")
        print("\033[33m4\033[0m Last Name")
        print("\033[33m5\033[0m Credit Card Number")
        print("\033[33m6\033[0m Street Address")
        print("\033[33m7\033[0m City")
        print("\033[33m8\033[0m State")
        print("\033[33m9\033[0m Country")
        print("\033[33m10\033[0m Zip Code")
        print("\033[33m11\033[0m Phone")
        print("\033[33m12\033[0m Email")
        print(" ")
        modify_choice = input("Your selection: ")
        
        if modify_choice == "exit":
            print("Returning to previous page")
            print("")
            break
        elif modify_choice == "1":
            while True:
                ssn_input = input("Change SSN to: ")
                
                if ssn_input == "exit":
                    print("Returning to previous page")
                    break
                # below replaces any non digit characters (\D) with an empty string ""
                # essentially removing non digit chars
                ssn_input = re.sub(r"\D", "", ssn_input)
                
                # need to convert ssn_input to a string because int doesnt have a length function
                if len(str(ssn_input)) == 9:
                    update_results = cust_update_sql(cust_ssn,'SSN', ssn_input)
                    # checks if the function output is a string, aka error message, then it will
                    # have this function start back at the top
                    if isinstance(update_results, str):
                        print(update_results)
                        print("")
                        continue
                    else:
                        print(update_results)
                        
                    # Need to update cust_ssn because the old value we were working with has
                    # been changed.  Need to point to the new value if user wants to update details
                    # for the same customer
                    cust_ssn = ssn_input
                    print("Successfully executed")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid SSN.  Remember SSNs have 9 digits.")
                    print("")
        elif modify_choice == "2":
            while True:
                f_name_input = input("Change First Name to: ")
                
                if f_name_input == "exit":
                    print("Returning to previous page")
                    break
                elif f_name_input != 'exit':
                    # .title() is needed to convert the given string to Title Case
                    update_results = cust_update_sql(cust_ssn,'FIRST_NAME', f_name_input.title())
                    # checks if the function output is a string, aka error message, then it will
                    # have this function start back at the top
                    if isinstance(update_results, str):
                        print(update_results)
                        print("")
                        continue
                    else:
                        print(update_results)
                        
                    print("Successfully executed")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid selection.  I honestly don't know how.")
                    print("")    
        elif modify_choice == "3":
            while True:
                m_name_input = input("Change Middle Name to: ")
                
                if m_name_input == "exit":
                    print("Returning to previous page")
                    break
                elif m_name_input != 'exit':
                    # .lower() is needed to convert the given string to lower Case
                    update_results = cust_update_sql(cust_ssn,'MIDDLE_NAME', m_name_input.lower())
                    # checks if the function output is a string, aka error message, then it will
                    # have this function start back at the top
                    if isinstance(update_results, str):
                        print(update_results)
                        print("")
                        continue
                    else:
                        print(update_results)
                        
                    print("Successfully executed")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid selection.  I honestly don't know how.")
                    print("") 
        elif modify_choice == "4":
            while True:
                l_name_input = input("Change Last Name to: ")
                
                if l_name_input == "exit":
                    print("Returning to previous page")
                    break
                elif l_name_input != 'exit':
                    # .title() is needed to convert the given string to Title Case
                    update_results = cust_update_sql(cust_ssn,'LAST_NAME', l_name_input.title())
                    # checks if the function output is a string, aka error message, then it will
                    # have this function start back at the top
                    if isinstance(update_results, str):
                        print(update_results)
                        print("")
                        continue
                    else:
                        print(update_results)
                        
                    print("Successfully executed")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid selection.  I honestly don't know how.")
                    print("")
        elif modify_choice == "5":
            while True:
                cc_input = input("Change Credit Card Number to: ")
                
                if cc_input == "exit":
                    print("Returning to previous page")
                    break
                # below replaces any non digit characters (\D) with an empty string ""
                # essentially removing non digit chars
                cc_input = re.sub(r"\D", "", cc_input)
                
                # need to convert cc_input to a string because int doesnt have a length function
                if len(str(cc_input)) == 16:
                    update_results = cust_update_sql(cust_ssn,'Credit_card_no', cc_input)
                    # checks if the function output is a string, aka error message, then it will
                    # have this function start back at the top
                    if isinstance(update_results, str):
                        print(update_results)
                        print("")
                        continue
                    else:
                        print(update_results)
                        
                    print("Successfully executed")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid CC Num.  Remember CC Nums have 16 digits.")
                    print("") 
        elif modify_choice == "6":
            while True:
                add_input = input("Change Street Address to: ")
                
                if add_input == "exit":
                    print("Returning to previous page")
                    break
                elif add_input != 'exit':
                    # .title() to make it title case
                    update_results = cust_update_sql(cust_ssn,'FULL_STREET_ADDRESS', add_input.title())
                    # checks if the function output is a string, aka error message, then it will
                    # have this function start back at the top
                    if isinstance(update_results, str):
                        print(update_results)
                        print("")
                        continue
                    else:
                        print(update_results)
                        
                    print("Successfully executed")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid selection.  I honestly don't know how.")
                    print("")
        elif modify_choice == "7":
            while True:
                city_input = input("Change City to: ")
                
                if city_input == "exit":
                    print("Returning to previous page")
                    break
                elif city_input != 'exit':
                    # .title() is needed to convert the given string to Title Case
                    update_results = cust_update_sql(cust_ssn,'CUST_CITY', city_input.title())
                    # checks if the function output is a string, aka error message, then it will
                    # have this function start back at the top
                    if isinstance(update_results, str):
                        print(update_results)
                        print("")
                        continue
                    else:
                        print(update_results)
                        
                    print("Successfully executed")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid selection.  I honestly don't know how.")
                    print("")
        elif modify_choice == "8":
            while True:
                state_input = input("Change State to: ")
                
                if state_input == "exit":
                    print("Returning to previous page")
                    break
                
                if len(state_input) == 2:
                    # .upper() to convert to capital letters
                    update_results = cust_update_sql(cust_ssn,'CUST_STATE', state_input.upper())
                    # checks if the function output is a string, aka error message, then it will
                    # have this function start back at the top
                    if isinstance(update_results, str):
                        print(update_results)
                        print("")
                        continue
                    else:
                        print(update_results)
                        
                    print("Successfully executed")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid State.  Remember States have 2 letters.")
                    print("")
        elif modify_choice == "9":
            while True:
                ctry_input = input("Change Country to: ")
                
                if ctry_input == "exit":
                    print("Returning to previous page")
                    break
                elif ctry_input != 'exit':
                    # .title() is needed to convert the given string to Title Case
                    update_results = cust_update_sql(cust_ssn,'CUST_COUNTRY', ctry_input.title())
                    # checks if the function output is a string, aka error message, then it will
                    # have this function start back at the top
                    if isinstance(update_results, str):
                        print(update_results)
                        print("")
                        continue
                    else:
                        print(update_results)
                        
                    print("Successfully executed")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid selection.  I honestly don't know how.")
                    print("") 
        elif modify_choice == "10":
            while True:
                zip_input = input("Change Zip Code to: ")
                
                if zip_input == "exit":
                    print("Returning to previous page")
                    break
                # below replaces any non digit characters (\D) with an empty string ""
                # essentially removing non digit chars
                zip_input = re.sub(r"\D", "", zip_input)
                
                # need to convert zip_input to a string because int doesnt have a length function
                if len(str(zip_input)) == 5:
                    update_results = cust_update_sql(cust_ssn,'CUST_ZIP', zip_input)
                    # checks if the function output is a string, aka error message, then it will
                    # have this function start back at the top
                    if isinstance(update_results, str):
                        print(update_results)
                        print("")
                        continue
                    else:
                        print(update_results)
                        
                    print("Successfully executed")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid zip code.  Remember zip codes have 5 digits.")
                    print("") 
        elif modify_choice == "11":
            while True:
                phone_input = input("Change Phone Number to: ")
                
                if phone_input == "exit":
                    print("Returning to previous page")
                    break
                # below replaces any non digit characters (\D) with an empty string ""
                # essentially removing non digit chars
                phone_input = re.sub(r"\D", "", phone_input)
                
                # need to convert phone_input to a string because int doesnt have a length function
                if len(str(phone_input)) == 10:
                    # change the number to match the format in the db
                    phone_input = f"({phone_input[:3]}){phone_input[3:6]}-{phone_input[6:]}"
                    update_results = cust_update_sql(cust_ssn,'CUST_PHONE', phone_input)
                    # checks if the function output is a string, aka error message, then it will
                    # have this function start back at the top
                    if isinstance(update_results, str):
                        print(update_results)
                        print("")
                        continue
                    else:
                        print(update_results)
                        
                    print("Successfully executed")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid phone num.  Remember phone nums have 10 digits.")
                    print("")
        elif modify_choice == "12":
            while True:
                email_input = input("Change Email Address to: ")
                
                if email_input == "exit":
                    print("Returning to previous page")
                    break
                #^\S+@\S+\.\S+$ checks to see if the string is a valid email address.  the "^\S+" checks
                #if there are one or more non-whitespace characters at the start of the string.  Can't have
                #blank spaces in an email address. The ^ is necessary because "ex ample@example.com" would be
                #a match on "ample@example.com".  We check for "@" with one or more non-whitespace character after it
                #followed by a "." (\. needs to be used because just a "." in regex matches to any single character).
                #Finished off by "\S+$" which matches one or more non-whitespace characters that end the string.  
                #The "$" is necessary for the same reason that the "^" is necessary.  The "~" is like a NOT so only
                #the non matches will be shown.
                elif bool(re.match(r'^\S+@\S+\.\S+$', email_input)):
                    update_results = cust_update_sql(cust_ssn,'CUST_EMAIL', email_input)
                    # checks if the function output is a string, aka error message, then it will
                    # have this function start back at the top
                    if isinstance(update_results, str):
                        print(update_results)
                        print("")
                        continue
                    else:
                        print(update_results)
                        
                    print("Successfully executed")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid email.  Please try again.")
                    print("")     
        else:
            print("\033[31mERROR\033[0m You have made an invalid selection.  Please try again.")  
            print("")              

def statement_header_format(cust_details_tuple):
    # padding a leading 0 to the zip code(needs to be converted from int to string)
    zip = str(cust_details_tuple[0][7]).rjust(5,"0")
    
    print("")
    print("\033[4mMonthly Statement\033[0m")
    print("")
    print("Customer Details:")
    print(f"First Name: {cust_details_tuple[0][0]}")
    print(f"Middle Name: {cust_details_tuple[0][1]}")
    print(f"Last Name: {cust_details_tuple[0][2]}")
    print(f"Credit Card Number: {cust_details_tuple[0][3]}")
    print(f"Street Address:")
    print(f"{cust_details_tuple[0][4]}")
    print(f"{cust_details_tuple[0][5]}, {cust_details_tuple[0][6]} {zip}")
    print(f"{cust_details_tuple[0][8]}")
    print(f"Phone Number: {cust_details_tuple[0][9]}")
    print(f"EMail Address: {cust_details_tuple[0][10]}")

def statement_header_sql(cc_num):
    try:
        # setting it this way is advised to prevent sql injection attacks. 
        params = [cc_num]
        
        statement_query = ("SELECT FIRST_NAME, MIDDLE_NAME, LAST_NAME, Credit_card_no, FULL_STREET_ADDRESS, " 
                        "CUST_CITY, CUST_STATE, CUST_ZIP, CUST_COUNTRY, CUST_PHONE, CUST_EMAIL "
                        "FROM cdw_sapp_customer "
                        "WHERE Credit_card_no = %s")
        
        cursor.execute(statement_query, params) #cursor was assigned in the connect_sql() function
        result = cursor.fetchall()            #fetches all the results
        
        statement_header = statement_header_format(result)
        
        return statement_header
    except msql.Error as error:
        return f"\033[31mERROR\033[0m Failed to retrieve customers records: {error}"

def statement_sql(cc_num, year, mon):
    try:
        # setting it this way is advised to prevent sql injection attacks. 
        params = [cc_num]
        
        statement_query = ("SELECT TRANSACTION_ID, TIMEID, TRANSACTION_TYPE, TRANSACTION_VALUE "
                        "FROM cdw_sapp_credit_card "  
                        f"WHERE CUST_CC_NO = %s AND TIMEID LIKE '{year}%' AND TIMEID LIKE '____{mon}%' "
                        "ORDER BY TIMEID DESC")
        
        cursor.execute(statement_query, params) #cursor was assigned in the connect_sql() function
        result = cursor.fetchall()            #fetches all the results
        
        statement_tb = PrettyTable(["Trans ID","Time (YYYYMMDD)","Type","Amount"])
        for i in result:
            #had to slice the row to omit the 13th column from being added
            statement_tb.add_row(i)
        
        cust_details = statement_header_sql(cc_num)
        
        return statement_tb, cust_details
    except msql.Error as error:
        return f"\033[31mERROR\033[0m Failed to retrieve records: {error}"

def cc_statement_input(cc_input):
    cc_cust_details = cust_details_sql(cc_num_full=cc_input)
    if cc_cust_details == 0:
        print("There is no customer with the given Credit Card number.")
        print("")
    else:
        while True:
            year_input = input("Please enter a year: ")
            
            if year_input == "exit":
                print("Returning to previous page")
                print("")
                break
            elif bool(re.match(r'^\d{4}$', year_input)):
                pass 
            else:
                print("\033[31mERROR\033[0m You have made an invalid selection. Only 2018 is valid.")
                print("")
                continue
            
            mon_input = input("Please enter a month (MM format): ")
            
            if mon_input == "exit":
                print("Returning to previous page")
                print("")
                break
            # Regex pattern: "^(0?[1-9]|1[0-2])$".  We need ^ to indicate that we are looking for 
            # the pattern at the start of a string, not in the middle of it.  Similar reason for the $ 
            # but for the end of the string.  0?[1-9] matches a single digit from 1-9 with an optional
            # leading zero.  | is an OR operator.  1[0-2] matches 10, 11, or 12.
            elif bool(re.match(r"^(0?[1-9]|1[0-2])$", mon_input)):
                mon_input = mon_input.rjust(2,"0")  #padding a leading zero if single digit
            else:
                print("\033[31mERROR\033[0m You have made an invalid selection. Remember, only one or two digits.")
                print("")
                continue
                    
            statement, cust_details = statement_sql(cc_input,year_input,mon_input)
            
            if isinstance(statement, str):
                print(cust_details)
                print(statement)
                print("")
            else:
                print(statement)
            break
                             
def run_gen_monthly_statement():
    while True:     
        print("")
        print("\033[4mGenerate Monthly Statement\033[0m")
        instructions()
        print("Possible selections are highlighted in yellow.")
        print("")
        print("\033[33m1\033[0m Enter CC num")
        print("\033[33m2\033[0m Search for Customer")
        print(" ")
        
        statement_choice = input("Your selection: ")
        
        if statement_choice == "exit":
            print("Returning to previous page")
            print("")
            break 
        elif statement_choice == "1":
            while True:
                cc_input = input("Please enter the credit card number: ")
                
                if cc_input == "exit":
                    print("Returning to previous page")
                    break
                # below replaces any non digit characters (\D) with an empty string ""
                # essentially removing non digit chars
                cc_input = re.sub(r"\D", "", cc_input)
                
                # need to convert cc_input to a string because int doesnt have a length function
                if len(str(cc_input)) == 16:
                    cc_statement_input(cc_input)
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid CC Num.  Remember CC Nums have 16 digits.")
                    print("") 
        elif statement_choice == "2":
            run_cust_details(modify=True)
            
            exit_check = exit_from_cust_details
            if exit_check == 1:
                continue   
    
            # We need to isolate the CC num so we can use it to lookup customers 
            # To achieve this we use the json library to convert the prettytable
            # to a json string(its actually a list) and then we extract the dict in that list.  
            # I needed to remove the Last Updated column because the timestamp data type couldn't
            # be serialized in json
            return_results.del_column('Last Updated')
            json_data = json.loads(return_results.get_json_string())
            cust_dict = json_data[1]
            cust_cc = cust_dict['CC Num']   
            print(f"Proceeding with Credit Card Number: {cust_cc}")
            print("")
            cc_statement_input(cust_cc) 
        else:
            print("\033[31mERROR\033[0m You have made an invalid selection.  Please try again.")  
            print("")

def time_preiod_sql(cc_num, start_time, end_time):
    try:
        # need to make sure the end_time is larger than the start_time or else the query won't return anything
        if end_time < start_time:
            old_start_time = start_time
            start_time = end_time
            end_time = old_start_time
            
        params = [cc_num, start_time, end_time]
        time_between_sql = ("SELECT TRANSACTION_ID, TIMEID, TRANSACTION_TYPE, TRANSACTION_VALUE " 
                            "FROM cdw_sapp_credit_card "  
                            "WHERE CUST_CC_NO = %s AND TIMEID BETWEEN %s AND %s "
                            "ORDER BY TIMEID DESC;")
        cursor.execute(time_between_sql,(params))    #cursor was assigned in the connect_sql() function
        result = cursor.fetchall()                   #fetches all the results
        
        time_period_results_tb = PrettyTable(["Trans ID","Time (YYYYMMDD)","Type","Amount"])
        for i in result:
            #had to slice the row to omit the 13th column from being added
            time_period_results_tb.add_row(i)
        
        return time_period_results_tb
    except msql.Error as error:
        return f"\033[31mERROR\033[0m Failed to retrieve records: {error}"
    
def run_trans_in_period():
    while True:
        print("")
        print("\033[4mCustomer Transactions Between Two Time Periods\033[0m")
        instructions()
        print("Possible selections are highlighted in yellow.")
        print("")
        print("\033[33m1\033[0m Enter CC num")
        print("\033[33m2\033[0m Enter SSN")
        print("\033[33m3\033[0m Search for Customer")
        print(" ")
        menu_selection = input("Your selection: ")
        
        if menu_selection == 'exit':
            print("Returning to previous page")
            print("")
            break 
        elif menu_selection == '1':
            while True:
                cc_input = input("Please enter the CC number: ")
                
                if cc_input == 'exit':
                    print("Returning to previous page")
                    print("")
                    break 
                
                # below replaces any non digit characters (\D) with an empty string ""
                # essentially removing non digit chars
                cc_input = re.sub(r"\D", "", cc_input)
                
                # need to convert cc_input to a string because int doesnt have a length function
                if len(str(cc_input)) == 16:
                    cc_cust_details = cust_details_sql(cc_num_full=cc_input)
                    if cc_cust_details == 0:
                        print("There is no customer with the given Credit Card number.")
                        print("")
                        continue
                    # setting this to the same cc variable that i used in the option 3 decision branch so i easily
                    # pass it into the function later
                    cust_cc = cc_input
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid CC Num.  Remember CC Nums have 16 digits.")
                    print("")
                    continue
                
            if cc_input == 'exit':
                continue    
        elif menu_selection == '2':
            while True:
                ssn_input = input("Please enter the customer's SSN: ")

                if ssn_input == 'exit':
                    print("Returning to previous page")
                    print("")
                    break
                
                # below replaces any non digit characters (\D) with an empty string ""
                # essentially removing non digit chars
                ssn_input = re.sub(r"\D", "", ssn_input)
                
                # need to convert ssn_input to a string because int doesnt have a length function
                if len(str(ssn_input)) == 9:
                    ssn_cust_details = cust_details_sql(ssn=ssn_input)
                    if ssn_cust_details == 0:
                        print("There is no customer with the given SSN.")
                        print("")
                        continue
                    
                    # We need to isolate the CC num so we can use it to lookup customers 
                    # To achieve this we use the json library to convert the prettytable
                    # to a json string(its actually a list) and then we extract the dict in that list.  
                    # I needed to remove the Last Updated column because the timestamp data type couldn't
                    # be serialized in json
                    ssn_cust_details.del_column('Last Updated')
                    json_data = json.loads(ssn_cust_details.get_json_string())
                    cust_dict = json_data[1]
                    cust_cc = cust_dict['CC Num']   
                    print(f"Proceeding with Credit Card Number: {cust_cc}")
                    print("")
                    break
                else:
                    print("\033[31mERROR\033[0m You have entered an invalid SSN.  Remember SSNs have 9 digits.")
                    print("")
                    continue
                
            if ssn_input == 'exit':
                continue
        elif menu_selection == "3":
            run_cust_details(modify=True)
            
            exit_check = exit_from_cust_details
            if exit_check == 1:
                continue   
    
            # We need to isolate the CC num so we can use it to lookup customers 
            # To achieve this we use the json library to convert the prettytable
            # to a json string(its actually a list) and then we extract the dict in that list.  
            # I needed to remove the Last Updated column because the timestamp data type couldn't
            # be serialized in json
            return_results.del_column('Last Updated')
            json_data = json.loads(return_results.get_json_string())
            cust_dict = json_data[1]
            cust_cc = cust_dict['CC Num']   
            print(f"Proceeding with Credit Card Number: {cust_cc}")
            print("")
        else:
            print("\033[31mERROR\033[0m You have made an invalid selection.  Please try again.")  
            print("")
            continue
        
        while True:
            time1 = input("Please enter start date (YYYYMMDD): ") 
            
            if time1 == 'exit':
                print("Returning to previous page")
                print("")
                break
            # need to convert to a string because int doesnt have a length function
            elif len(str(time1)) != 8:
                print("\033[31mERROR\033[0m You have entered an invalid date.  Remember to enter only 8 digits")
                print("")
            else:
                while True:   
                    time2 = input("Please enter end date (YYYYMMDD): ") 
            
                    if time2 == 'exit':
                        print("Returning to previous page")
                        print("")
                        break
                    # need to convert to a string because int doesnt have a length function
                    elif len(str(time2)) != 8:
                        print("\033[31mERROR\033[0m You have entered an invalid date.  Remember to enter only 8 digits")
                        print("")
                    else:
                        time_results = time_preiod_sql(cust_cc,time1,time2)
                        # checks if the function output is a string, aka error message, then it will
                        # have this function start back at the top
                        if isinstance(time_results, str):
                            print(time_results)
                            print("")
                        else:
                            print(time_preiod_sql(cust_cc,time1,time2))
                    
                    break
                break
                                     
def run_choice(choice):
    if choice == "1":
        run_zipcode_search()
    elif choice == "2":
        run_type_filter()
    elif choice == "3":
        run_branch_filter()
    elif choice == "4":
        run_cust_details()
    elif choice == "5":
        run_modify_cust_details()
    elif choice == "6":
        run_gen_monthly_statement()
    elif choice == "7":
        run_trans_in_period()
    else:
        print("\033[31mERROR\033[0m You have made an invalid selection.  Please try again.")
        print("")
    
def app():
    while True:
        instructions()
        main_menu()

        choice = input("Your selection: ")
        run_choice(choice)

        if choice == "exit":
            print("Closing program.  Come back next time.")
            break
               
startup_sequence()
welcome_title()
app()