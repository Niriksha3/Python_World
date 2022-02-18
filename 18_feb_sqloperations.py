
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
import smtplib
import logging
import csv

class SqlOperations:

    """ This class is created to perform various mysql operations in python """
    def __init__(self,dbname):
        self.dbname=dbname
        self.my_connection = None


        """ The below code is used to create one log file to store all the errors """
        try:
            logging.basicConfig(filename="log_file1.txt",
                                filemode='a',
                                format='%(asctime)s %(levelname)s-%(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')

        except Exception as e:
            print("Error occured during creation of log file")
            print(e)

        """ The below code is used to connect to required database """

        try:

            self.my_connection = connection.MySQLConnection(user='dhoni', password='dhoni07', host='127.0.0.1',
                                               database=self.dbname)
            self.mycursor = self.my_connection.cursor()

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
                print(err)
            else:
                print(err)

    def create_table(self):
        """ This function is used to create table """

        try:

            t_name = input("Enter the table name to be created")
            no_column = int(input("Please enter the number of columns : "))
            query1= """CREATE TABLE  {}(""".format(t_name)
            for i in range(no_column):
                column_i = input("Enter the details of column no {} : Enter columnname datatype constraints separated by space: ".format(i + 1))
                query1 = query1 + column_i + ","
            query1 = query1[:-1]
            query = query1 + ")"
            self.mycursor.execute(query)
            print("Table Created")
            msg="Hi niriksha your table got created"
            self.mail(msg,'create')

        except Exception as e:
            print("Error occured during table creation")
            logging.critical("Error occured during creation of table")
            print(e)

    def insert_data(self):
        """ This function is used to insert data into table """
        try:

            t_name = input("Enter the table name in which you want to insert the data")
            no_column = int(input("Please enter the number of columns you want to insert : "))
            query1 = """insert into  {}(""".format(t_name)
            for i in range(no_column):
                column_i = input("Enter the column {} to which you want to insert: ".format(i+1))
                query1 = query1 + column_i + ","
            query1 = query1[:-1]
            query2= query1 + ")"
            query2=query2 + "values("
            for i in range(no_column):
                value_i=input("Enter the value {} you want to insert: ".format(i+1))
                query2 = query2 + value_i +","
            query2=query2[:-1]
            query=query2 + ")"

            self.mycursor.execute(query)
            print("inserted")
            msg="Hi niriksha your data got inserted"
            self.mail(msg,'insert')

        except Exception as e:
            print("Error occured during inserting data into table")
            logging.critical("Error occured during inserting data into table")
            print(e)

    def show_data(self):
        """ This function is used to show all the data present in the table """
        try:


            tablename = input("enter the table name you want to see data in it")
            query = f'SELECT * FROM {tablename}'
            self.mycursor.execute(query)
            data = self.mycursor.fetchall()
            for x in data:
                print(x)
            msg = "Hi niriksha your data is showed"
            self.mail(msg,'showdata')

        except Exception as e:
            print("Error while entering the table name ")
            logging.warning("Error while entering the table name to see the records")
            print(e)




    def delete_data(self):
        """ This function is used to delete the data from the table """
        try:

            tablename = input("enter the table name from which you want to delete the data")
            column_name=input("enter the column name that you want to take as reference")
            value=input("enter the value which you want to delete that particular row")

            query=f'DELETE FROM {tablename} WHERE {column_name}={value}'
            self.mycursor.execute(query)
            print("data got deleted ")
            msg="Hi niriksha your data got deleted"
            self.mail(msg,'delete')



        except Exception as e:
            print("Error occured while deleting the record")
            logging.warning("Error occured while deleting the record")
            print(e)

    def drop_table(self):
        """ This function is used to drop the table """
        try:

            tablename = input("enter the table name you want to drop")
            query=f'drop table {tablename}'
            self.mycursor.execute(query)
            print("Table droped")
            msg="Hi niriksha your table has got deleted"
            self.mail(msg,'drop')

        except Exception as e:
            print("Error occured while droping the table")
            logging.warning("Error occured while droping the table")
            print(e)


    def update_data(self):
        """ This function is used to update the data from the table """
        try:

            tablename = input("enter the table name you want to update")
            column_name=input("enter the column name in which you want to change")
            value=input("enter the value you want to change")
            ref_column=input("enter the column name which you want to take as reference")
            ref_value=input("enter the value for the reference column")

            query=f'UPDATE {tablename} SET {column_name}={value} WHERE {ref_column}={ref_value}'
            self.mycursor.execute(query)
            print("Updated")
            msg="Hi niriksha your data got updated"
            self.mail(msg,'update')

        except Exception as e:
            print("Error occured while updating the record")
            logging.warning("Error occured while updating the record")
            print(e)

    def mail(self,msg,key):
        """ This function is used to send mail to the users once sql operation is performed successfully """
        """ The below code will take the mailId from the csv file which contains the mailId for particular sql operation """
        try:
            csv_file = csv.reader(open("mail_document.csv", 'r'))
            for row in csv_file:
                if key == row[0]:
                    #print(row[1])
                    mailid=row[1]

            recievermailid=mailid

            s = smtplib.SMTP('smtp.gmail.com', 587)

            s.starttls()

            s.login("nirikshashetty3@gmail.com", "@niriksha123")

            self.message = msg

            self.sndermail = "nirikshashetty3@gmailcom"
            s.sendmail(self.sndermail, recievermailid, self.message)
            print("mail sent")

            s.quit()
        except Exception as e:
            logging.critical("Error occured while sending mail")
            print(e)





    def commit_close(self):
        """ This function is used to commit and close the connections """
        if self.my_connection != None:
            self.my_connection.commit()
            self.my_connection.close()

def main():
    try:
        dbname = input("Enter the database name\n")
        my_sql = SqlOperations(dbname)
        if my_sql.my_connection != None:
            while True:
                operation = int(input(
                    "choose the db operations to be performed:\n 1.Create table\n 2.Insert data\n 3.delete data\n 4.update data\n 5.Drop table\n 6.Show_data\n"))
                if operation == 1:
                    my_sql.create_table()
                elif operation == 2:
                    my_sql.insert_data()
                elif operation == 3:
                    my_sql.delete_data()
                elif operation == 4:
                    my_sql.update_data()
                elif operation ==5:
                    my_sql.drop_table()
                elif operation ==6:
                    my_sql.show_data()
                else:
                    print("invalid selection")
                choise = input("Do you want to continue y/n \n")
                if choise.upper() == "Y":
                    continue
                else:
                    break

    except Exception as e:

        print(e)

    finally:
        my_sql.commit_close()

if __name__ == "__main__":
        main()

