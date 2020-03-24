from csv import reader
from time import sleep  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tkinter
import nltk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from nltk.corpus import stopwords
from nltk.stem import   WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
import os
import io
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')


#################################################################

#pdf to text converter variables
resource_manager = PDFResourceManager()
fake_file_handle = io.StringIO()
converter = TextConverter(resource_manager, fake_file_handle)
page_interpreter = PDFPageInterpreter(resource_manager, converter)

#function which converts pdf to text
def pdf_to_text_converter(file)->str:
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                  caching=True,
                                  check_extractable=True):
            page_interpreter.process_page(page)
            text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()
    return text
#################################################################

#fucntion which scrapes paragraphes from websites and return a string
def scrape(Url_link)-> str:
    details_text=[]
    try:
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('start-maximized')
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(Url_link)
        sleep(8)
        elements=driver.find_elements_by_tag_name('p')
        text=''
        for i in elements:
            text+=i.text
    except Exception as e:
        print(e)
    return text     
#############################################################
#function that gives the occurence of words in the text and return a dictionary

def frequency_dict(article) -> dict:
   
    stop_words = set(stopwords.words())
    words = word_tokenize(article)
    wl = WordNetLemmatizer()
    
    frequency_dict = dict()
    for wd in words:
        rootword = wl.lemmatize(wd)
        if rootword in stop_words:
            continue
        if rootword in frequency_dict:
            frequency_dict[rootword] += 1
        else:
            frequency_dict[rootword] = 1

    return frequency_dict


############################################################
#function that give a weight to each sentences according to the words that are in the sentence. 
def sentences_frequency(sentences, frequency_dict) -> dict:   

    sentence_weight = dict()

    for sentence in sentences:
        sentence_wdcount = (len(word_tokenize(sentence)))
        sentence_wdcount_wot_stop_words = 0
        for wd_weight in frequency_dict:
            if wd_weight in sentence.lower():
                sentence_wdcount_wot_stop_words += 1
                if sentence in sentence_weight:
                    sentence_weight[sentence] += frequency_dict[wd_weight]
                else:
                    sentence_weight[sentence] = frequency_dict[wd_weight]

        sentence_weight[sentence] = sentence_weight[sentence] / sentence_wdcount_wot_stop_words
      
    return sentence_weight

###########################################################
#functions that gives the average weight of the set of sentences
def average_weight(sentence_weight) -> int:
   
    sum_ = 0
    for i in sentence_weight:
        sum_ += sentence_weight[i]

    average_weight = (sum_ / len(sentence_weight))

    return average_weight
###########################################################
#fucntions that create the summary
def summary(sentences, sentence_weight, threshold):
    sentence_counter = 0
    summary = ''

    for sentence in sentences:
        if sentence in sentence_weight and sentence_weight[sentence] >= (threshold):
            summary += " " + sentence
            sentence_counter += 1

    return summary

############################################################
#function that retrives the title of the document summarized. 
def title(string)-> str:
	doc_title =''
	i=len(string)-1
	while string[i] !='/':
		doc_title = string[i] + doc_title 
		i=i-1   
	return doc_title

############################################################
#fucntion which run the summary process

def run_article_summary(article):

    freq_dict = frequency_dict(article)
    
    sentences = sent_tokenize(article)
    

    sentence_scores = sentences_frequency(sentences, freq_dict)
    
    threshold = average_weight(sentence_scores)
    
    article_summary = summary(sentences, sentence_scores, 1.2*threshold)
    
    return article_summary
#######################################################################

input_name=['Website url']
type_file=['Url', 'Pdf']
Entries=[]
root_3= tkinter.Tk()
root_3.geometry ("1044x1568")
root_3.title('Please choose the type of document you want to summarize')
image= Image.open("fuji.jpg")
background_image= ImageTk.PhotoImage(image)
Background_label = tkinter.Label(root_3, image=background_image).pack()



######################################################################
#fucntion that get the text from the button in the Graphical User Interface

def getText(a):
  global char
  char=a 
  return str(a)

######################################################################
#Buttons in the Graphical User Interface

sbmitbtn_1 = tkinter.Button(root_3, text = 'URL' ,activebackground = "pink", activeforeground = "blue", command= lambda:[getText('URL'), root_3.destroy()])
sbmitbtn_1.config(height='2', width='8')
sbmitbtn_1.pack()
sbmitbtn_1.place(x=250, y=50)
sbmitbtn_2 = tkinter.Button(root_3, text = 'PDF' ,activebackground = "pink", activeforeground = "blue", command= lambda:[getText('PDF'), root_3.destroy()])
sbmitbtn_2.config(height='2', width='8')
sbmitbtn_2.pack()
sbmitbtn_2.place(x=400, y=50)

root_3.mainloop()

######################################################################
#if the file is a URL
if char =='URL':
######################################################################
# Graphical User Interface
  root_2=tkinter.Tk()
  root_2.geometry("720x406")
  root_2.title('Sum-ary')
  image = Image.open("broly.jpg")
  background_image=ImageTk.PhotoImage(image)
  background_label = tkinter.Label(root_2, image=background_image)
  background_label.pack()
  y_=70
  i=70

  for input_ in input_name:
      label =  tkinter.Label(root_2, text = input_).place(x = 20,y = y_)
      y_=y_+20
      entry=tkinter.Entry(root_2)
      entry.place(x=600,y=i)
      i=i+20
      Entries.append(entry)
 
######################################################################
#fucntion that get the text from the button in the Graphical User Interface

  def get1():
      global address
      address=[]
      for entry in Entries:
          address.append(entry.get())
      
######################################################################
# Graphical User Interface
  label1 =tkinter.Label(root_2, text = 'Website URL')
  label1.place(x =180,y =20)
  label1.config(font=('Calibri', 22))
  sbmitbtn = tkinter.Button(root_2, text = "Submit",activebackground = "pink", activeforeground = "blue", command=lambda: [get1(), root_2.destroy()])
  sbmitbtn.pack()
  sbmitbtn.place(x = 30, y = 220)
  root_2.mainloop()
######################################################################
# run summary function
  if __name__ == '__main__':
            summary_output = run_article_summary(scrape(address[0]))
            with open(title(address[0])+'_summary.txt', 'w') as article_summary:
            	article_summary.write(summary_output)
            	article_summary.close()

          

	

elif char=='PDF':
    #dialogbox so that the user can choose a file. 
    root_1=tkinter.Tk()
    root_1.withdraw()
    file = filedialog.askopenfile(parent=root_1,mode='rb',title='Choose a file')
    root_1.destroy()

    if file != None:
        data = file.read()
        file.close()
        print("I got %d bytes from this file." % len(data))
    ######################################################################
    # Run summary function
    if __name__ == '__main__':
        summary_output = run_article_summary(pdf_to_text_converter(file.name))
    with open(title(file.name)+'_summary.txt' , 'w') as summary_file:
    	summary_file.write(summary_output)
    	summary_file.close()

