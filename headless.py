import os
import time
import datetime
import csv
import json
from urllib.request import urlretrieve
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.common.exceptions import NoSuchElementException
import psycopg2

from dotenv import load_dotenv
load_dotenv()

# Get the connection string from the environment variable

# connection_string = os.environ('DB_URL_ENV')

# Connect to the Postgres database

# conn = psycopg2.connect(connection_string)

# conn.autocommit = True

def func_log(serial,word):
    log_time = datetime.datetime.now()
    log_single_line=str(log_time) + ' |------ Word No: '+ str(serial) + ' ----- | Name: ' + str(word)
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(log_single_line + '\n')
        f.close()


def func_insert(input_word,word1,explanation1,english1,translate1,keywords1):

    word=word1.replace("'", "''")
    explanation=explanation1.replace("'", "''")
    english=english1.replace("'", "''")
    translate=translate1.replace("'", "''")
    keywords=keywords1.replace("'", "''")

    # Create a cursor object
    # cur = conn.cursor()

    #Create Sql query
    sql_query='''INSERT INTO words_tables (word, explanation, english, translate, keywords, as_soundex)
                    VALUES (' '''+ input_word + ''' ', ' '''+ explanation + ''' ', ' ''' + english + ''' ', ' '''+word+ ''' ', ' ''' +keywords +''' ', 'NA');'''
    # print(sql_query)
    
    # try:
    #     cur.execute(sql_query)
    # except psycopg2.IntegrityError:
    #     conn.rollback()
    #     print('data already exist')
    # else:
    #     with open('output.sql', 'a', encoding='utf-8') as f:
    #         f.write(sql_query)
    #         f.close()
        # conn.commit()

    with open('output.sql', 'a', encoding='utf-8') as f:
            f.write(sql_query)
            f.close()


    # Close the cursor and connection
    # cur.close()

# declaration block 
url = os.environ['URL_ENV']
# declaration block 

def func_download_db():
  url="https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"
  urlretrieve(url, "words_dictionary.json")

def func_scrap_data(input_word):
    try:
            word_data = driver.find_element(By.ID, "word")
            explaination_data = driver.find_element(By.ID, "explaination")
            english_data = driver.find_element(By.ID, "english")
            translate_data = driver.find_element(By.ID, "translate")
            keyword_data = driver.find_element(By.ID, "keyword")

            # Get text of div element using <element>.text
            print(word_data.text)
            if(len(word_data.text) != 0):
                func_insert(input_word,word_data.text ,explaination_data.text ,english_data.text ,translate_data.text,keyword_data.text)
                # div_text = word_data.text + explaination_data.text + english_data.text + translate_data.text + keyword_data.text
                # print(div_text)
                # with open('demofile2.sql', 'a', encoding='utf-8') as f:
                #     f.write(div_text)
                #     f.close()
            else:
                print("No")   
        
    except NoSuchElementException:
            print("The div element does not exist.")
func_download_db()

f = open('words_dictionary.json')
data_dictionary = json.load(f)
all_word_list=list(data_dictionary)

start=int(os.environ['START_ENV'])
end=int(os.environ['END_ENV'])

if start==0 & end==0:
    converted_list=all_word_list
else:
    converted_list=all_word_list[start-1:end+1]
options = webdriver.ChromeOptions()

# ******************** Uncomment The Middle Line for turn on Headless Mode ********************

options.add_argument("--headless=new")  #Headless
# options.add_argument('--no-sandbox')   
# ******************** Uncomment The Middle Line for turn on Headless Mode ********************
i=1
for x in converted_list:
    func_log(i,x)
    i=i+1
    with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options) as driver: #modified 
        driver.get(url)
        # print("Page URL:", driver.current_url)        
        word_input = driver.find_element(By.ID, 'word0')
        submit_button = driver.find_element(By.ID, 'search')
        # filling out the form elements
        word_input.send_keys(x)
        # word_input.send_keys('Assamese')
        # submit the form and log in
        submit_button.click()

        time.sleep(.5)
        func_scrap_data(x)

# conn.close()
