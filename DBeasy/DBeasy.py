import psycopg2
from getpass import getpass
from prettytable import PrettyTable
import os

def connecttopostgres():
    user = str(input("User: "))
    password = getpass("Password: ")

    try:
        con = psycopg2.connect(
            user = user,
            password = password,
            host = "localhost"
        )

        con.autocommit = True

        print("Connected Successfully")
        
        cur = con.cursor()

        cur.execute("select version();") 
        
        sql_version = cur.fetchone()

        print(sql_version)

        databasedetails(user, password, cur, con)
    
    except:
        print("error")

def databasedetails(user, password, cur, con):
    print("WELCOME TO DBeasy for postgresql")
    print("SELECT YOUR OPTION --")
    print("""
    PRESS 1 -- SHOW ALL DATABASES(NAMES ONLY)
    PRESS 2 -- SHOW ALL DATABASES(FULL DETAILS)
    PRESS 3 -- CREATE NEW DATABASE
    PRESS 4 -- CONNECT TO A DATABASE
    PRESS 5 -- DROP A DATABASE
    """)

    opt = int(input())

    if opt == 1:
        print("AVAILABLE DATABASES")
        cur.execute("SELECT * FROM pg_database")
        
        table = PrettyTable()

        table.field_names = ["Name"]
        for row in cur.fetchall():
            if row[5] == False:
                table.add_row([row[0]])
        
        print(table)

    elif opt == 2:
        print("AVAILABLE DATABASES")
        cur.execute("SELECT * FROM pg_database")

        table = PrettyTable()

        table.field_names = ["Name", "Language", ]
        for row in cur.fetchall():
            if row[5] == False:
                table.add_row([row[0], row[3]])
        
        print(table)

    elif opt == 3:
        print("CREATE YOUR NEW DATABASE -- ")

        newdbname = str(input("Enter your new database name: "))

        try:
            cur.execute("CREATE DATABASE " + newdbname)
            print("Database created successfully..")
        except:
            print("Database not created")

    elif opt == 4:
        print("CONNECT TO A EXISTING DATABASE")

        contodb = str(input("Enter database name: "))

        try:        
            con.close()
            newcon = psycopg2.connect(
                user = user,
                password = password,
                host = "localhost",
                database = contodb
            )
            newcon.autocommit = True

            print("Successfully connected to database {}".format(contodb))

            dbcur = newcon.cursor()
            dbqueries(user, password, dbcur, newcon)
        except:
            print("Not able to establish connection..")

    elif opt == 5:
        print("DROP/DELETE DATABASE -- ")

        newdbname = str(input("Enter the database name: "))

        try:
            cur.execute("DROP DATABASE " + newdbname)
            print("Database deleted successfully..")
        except:
            print("Database not deleted")


def dbqueries(user, password, dbcur, newcon):
    print("SELECT YOUR OPTION --")
    print("""
    SELECT YOUR OPTION --
    PRESS 1 - TO VIEW ALL THE TABLES IN THE DATABASE
    PRESS 2 - TO CREATE TABLE
    PRESS 3 - TO DROP TABLE
    PRESS 4 - TO VIEW ALL THE COLUMNS IN A TABLE
    PRESS 5 - TO ADD NEW COLUMN INTO TABLE
    PRESS 6 - TO INSERT DATA
    PRESS 7 - TO EDIT DATA
    """)

    qryopt = int(input())

    if qryopt == 1:
        sqltext = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"
        dbcur.execute(sqltext)

        dbatables = PrettyTable()
        dbatables.field_names = ["Table Name"]

        for row in dbcur.fetchall():
            dbatables.add_row(row)
        print(dbatables)

        cmdcommandfunc(user, password, dbcur, newcon)

    elif qryopt == 2:

        colnames = []
        coltypes = []

        newdbtable = str(input("Enter table name: "))
        totalcols = int(input("Total no. of col.s for the table: "))
        for i in range(totalcols):
            print(i+1, " col name: ")
            colnames.append(str(input()))
            print(i+1, "col datatype and size(eg. VARCHAR(100)): ")
            coltypes.append(str(input()))

        sqltext = "CREATE TABLE " + newdbtable + "("

        index = 0

        for colname, coltype in zip(colnames, coltypes):
            if index!=0:
                sqltext += "," + colname + " " + coltype
            else:
                sqltext += colname + " " + coltype
            index += 1            

        sqltext += ");"

        try:
            dbcur.execute(sqltext)
            print("Table created..")

            cmdcommandfunc(user, password, dbcur, newcon)
        except:
            print("error...table not created.")

    elif qryopt == 3:
        droptable = str(input("Drop table: "))

        sqltext = "DROP TABLE " + droptable + ";"

        try:
            dbcur.execute(sqltext)
            print("Table deleted..")

            cmdcommandfunc(user, password, dbcur, newcon)

        except:
            print("error...while deleting table")

    elif qryopt == 4:
        viewtable = str(input("Table name: "))

        sqltext = "SELECT * FROM " + viewtable + ";"

        try:
            dbcur.execute(sqltext)
            table = PrettyTable()
            
            table.field_names = [desc[0] for desc in dbcur.description]
            
            for row in dbcur.fetchall():
                tuplelist = []
                for i in range(len(row)):
                    tuplelist.append(row[i])
                table.add_row(tuplelist)
            
            print(table)
            cmdcommandfunc(user, password, dbcur, newcon)
        except:
            print("error")

    elif qryopt == 6:
        print("""
        PRESS 1 - TO ENTER MULTIPLE SIMILAR ROW DATA TO A TABLE
        PRESS 2 - TO ENTER MULTIPLE DIFFERENT ROW DATA TO A TABLE
        PRESS 3 - TO ADD DATA INTO MANY TABLES
        """)

        add_data_opt = int(input())

        if add_data_opt == 1:
            table = str(input("Table Name: "))
            sqltext = "INSERT INTO " + table

            closeloop = 0
            print("Enter column names separating with a ',' :")
            column_names_str = str(input())

            sqltext += "(" + column_names_str + ")"

            print("Enter column data separating with a ',' :")
            column_data_str = str(input())

            sqltext += " VALUES(" + column_data_str + ");"

            print(sqltext)
             

        
            

def cmdcommandfunc(user, password, dbcur, newcon):

    cmdcommand = str(input())
    if cmdcommand== "exit":
        os.system("cls")
        dbqueries(user, password, dbcur, newcon)
    elif cmdcommand == "main":
        os.system("cls")
        databasedetails(user, password, dbcur, newcon)


connecttopostgres()
