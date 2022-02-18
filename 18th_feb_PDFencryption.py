import os
import PyPDF2
import tkinter
from tkinter import filedialog
import time
from datetime import datetime
import smtplib
import csv
import pandas as pd
import logging
from mysql.connector import (connection)

# root=tkinter.Tk()
# root.withdraw()  # To withdraw a small box coming
# filepath=filedialog.askopenfilename()  # For choosing the file dianamically
# print(filepath)
class pdf_enc:
    """ this class is for pdf encrption"""
    def __init__(self,folder,dbname,recievermailid):
        self.folder=folder
        self.dbname=dbname
        self.recievermailid=recievermailid

    def pdf_encrption(self):
        """ this function is used to encrpt the pdf's precent in given directory"""


        """ The below code is used to create one log file to store all the errors """
        try:
            logging.basicConfig(filename="log_file1.txt",
                                filemode='a',
                                format='%(asctime)s %(levelname)s-%(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')

        except Exception as e:
            print("Error occured during creation of log file")
            print(e)

        try:
            direc = os.listdir(self.folder)
            list = []
            for file in direc:
                if file.endswith(".pdf"):
                    print(file)
                    pdf_file = open(self.folder + file, 'rb')
                    inputpdf = PyPDF2.PdfFileReader(pdf_file)
                    pages_no = inputpdf.numPages
                    output = PyPDF2.PdfFileWriter()

                    source = file
                    self.file_split = source.split(".pdf")[0]
                    # print(file_split)

                    self.c_t = datetime.now().strftime("%H-%M-%S")
                    print(self.c_t)
                    self.file_name = self.file_split + "-" + self.c_t + ".pdf"
                    print(self.file_name)

                    # source=file
                    # file_split=source.split(".")
                    # passwrd=repr(file_split[-2])
                    for i in range(pages_no):
                        inputpdf = PyPDF2.PdfFileReader(pdf_file)

                        output.addPage(inputpdf.getPage(i))
                        output.encrypt(self.file_split)

                        with open(self.file_name, "wb") as outputStream:
                            output.write(outputStream)

                    def getfileSize(filename):
                        return os.stat(filename).st_size

                    self.size = getfileSize(self.file_name)

                    print("fileSize=", self.size)
                    self.csv_file_creation()
                    self.db_connection()
        except Exception as e:
            print("Error occured while encrpting the file")
            logging.critical("Error while encrypting the pdf")
            print(e)


    def mail(self):
        """ this function is used to send mail to user once after pdf got encrpted"""
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)

            s.starttls()

            s.login("nirikshashetty3@gmail.com", "@niriksha123")

            message = "hi shetty your pdf's has got encrpted please do contact us if you have any queries,Thank You"

            self.sndermail = "nirikshashetty3@gmailcom"
            s.sendmail(self.sndermail, self.recievermailid, message)
            print(message)

            s.quit()
        except Exception as e:
            print("Error occured while sending mail")
            logging.critical("Error while sending the mail")
            print(e)

    def csv_file_creation(self):
        """ this function is used to add all the details of the encrpted file into csv file"""
        try:

            with open("details.csv", "a") as file_obj:
                csv_file_obj = csv.writer(file_obj)
                csv_file_name = "details.csv"
                csv_file_size = os.stat(csv_file_name).st_size == 0
                if csv_file_size:
                    csv_file_obj.writerow(["Fname", "Fsize", "Fcreation_time", "Fpassword", "usermail"])
                csv_file_obj.writerows([[self.file_name, self.size, self.c_t, self.file_split, self.recievermailid]])
        except Exception as e:
            print("Error occured while adding details to csv file")
            logging.critical("Error while adding details into csv file")
            print(e)


    def db_connection(self):
        """ this function is used to connect to required db and add all the details of encrpted file into separate table"""
        try:
            cnx = connection.MySQLConnection(user='dhoni', password='dhoni07', host='127.0.0.1', database=self.dbname)
            print("done")
            mycursor = cnx.cursor()
            mycursor.execute(
                "create table if not exists newtable (Fname varchar(500),Fsize int,Fcreation_time varchar(20),Fpassword varchar(500),usermail varchar(500))")
            print("Table created")

            querry1 = "insert into newtable(Fname,Fsize,Fcreation_time,Fpassword,usermail)values(%s,%s,%s,%s,%s)"
            val = [(self.file_name, self.size, self.c_t, self.file_split, self.recievermailid)]
            mycursor.executemany(querry1, val)
            print("values inserted")
            cnx.commit()
            print("saved")
            cnx.close()
        except Exception as e:
            print("Error occured while connecting to database")
            logging.critical("Error occured during the database connection or during passing details into table")
            print(e)



def main():
    try:
        sourceloc = r"C:/Users/Niriksha.Shetty/Documents/newfile/"
        dbname = input("enter the dbname you want to store data")
        recievermailid = input("Enter the mail id to whom you want to send mail")
        mypdf_enc = pdf_enc(sourceloc, dbname, recievermailid)
        mypdf_enc.pdf_encrption()
        mypdf_enc.mail()
        # mypdf_enc.csv_file_creation()
        # mypdf_enc.db_connection()
    except Exception as e:
        print("Error occured in main function")
        logging.critical("Error occured in main function")
        print(e)


if __name__=="__main__":
    main()














