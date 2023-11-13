

from model.chatbot import chatBots
from PyPDF2 import PdfReader
import textract
import xlrd
from werkzeug.utils import secure_filename
import os 
import pandas as pd

def checkValidity(id):
        isBot = chatBots.objects[:1](id=id).first()
        if not isBot:
            return False
        else:
              if (('text' in isBot and len(isBot.text)>0) or ('websiteData' in isBot and len(isBot.websiteData)>0) or ('faqData' in isBot and len(isBot.faqData)>0) or ('docData' in isBot and len(isBot.docData)>0)):
                    return True
              else:
                    return False

def pdfReader(file):
      pdf = PdfReader(file)
      text = ''
      for page in pdf.pages:
            text += page.extract_text()
      return text
def docuentReader(path):
       print("in")
       text =  textract.process("./"+path)
       mytext = text.decode('utf-8')
       print(mytext)
       return mytext
def xlReader(file):
      xls_workbook = xlrd.open_workbook(file_contents=file.read())
      print(xls_workbook)
      text = ''
      for sheet in xls_workbook.sheets():
        for row in range(sheet.nrows):
            row_values = [str(cell) for cell in sheet.row_values(row)]  # Convert each cell to a string
            text += ' '.join(row_values) + '\n'
      return text
def xlsxReader(file):
      df = pd.read_excel(file)
      # Iterate through the DataFrame and extract text
      text = ''
      for column in df.columns:
            for row in df[column]:
                  if not pd.isna(row):  # Check if the cell is not empty
                        text += str(row) + '\n'
      return text
