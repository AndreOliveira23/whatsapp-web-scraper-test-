import time
import itertools 
import mysql.connector
from time import sleep
from threading import Timer
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database ="meubanco"
)

mycursor = mydb.cursor()


global SCROLL_TO, SCROLL_SIZE

serv = Service("utils/chromedriver.exe")#Caminho para o chromedriver no sistema
op = webdriver.ChromeOptions()

options = Options()
options.add_argument('user-data-dir=./User_Data')  # Salvando os dados para não ter que escanear do QR Code novamente
op.add_argument('user-data-dir=./User_Data')
driver = webdriver.Chrome(service=serv, options=op)


def scrap():
    while True:
        print("Executando a função...")
        contatos = driver.find_elements(By.CLASS_NAME, "zoWT4") #Obtendo nome de todos os contatos presentes na tela
        mensagens = driver.find_elements(By.CLASS_NAME, "_1qB8f") #Obtendo as últimas mensagens de cada chat

        for(a,b) in zip(contatos,mensagens): #Combinando chat com suas respectivas últimas mensagens
            print("Contato: ", end = '')
            print(a.text)
            print("Última Mensagem: ", end = '')
            print(b.text)
            
            sql = "INSERT INTO whatsapp (Nome, Ultima_msg) VALUES (%s, %s)  ON DUPLICATE KEY UPDATE Ultima_msg=%s" #inserindo no banco de dados
            val = (a.text, b.text,b.text)
            mycursor.execute(sql, val)
            mydb.commit()
            if(mycursor.rowcount !=0 ): print ("Banco de dados atualizado com sucesso! ")
            print("")    
        time.sleep(10) #esperando 10 segundos antes de executar novamente
        print("fim da iteração")
    

def pane_scroll(dr):
    global SCROLL_TO, SCROLL_SIZE

    print('>>> scrolling side pane')
    side_pane = dr.find_element_by_id('pane-side')
    dr.execute_script('arguments[0].scrollTop = '+str(SCROLL_TO), side_pane)
    sleep(3)
    SCROLL_TO += SCROLL_SIZE


def main():
    # A função "scrap" inicia depois de 20 segundos. -> Como a tag onde está o nome do contato é gerada dinamicamente, o script não será capaz de selecionar caso a página
    # não esteja completamente carregada
    t = Timer(20, scrap)
    t.start() 

    global SCROLL_TO, SCROLL_SIZE
    SCROLL_SIZE = 600
    SCROLL_TO = 600
    
    driver.implicitly_wait(15)
    driver.get('https://web.whatsapp.com/')

    print("(Teste de web-scraping)")
    print('O código começará a executar assim que a página carregar totalmente!\n')

if __name__ == "__main__":
    main()
