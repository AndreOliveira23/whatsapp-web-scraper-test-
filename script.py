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
  database ="tucuma_pdo"
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
    print("Executando a função...")
    contato = driver. find_element(By.XPATH,"//span[contains(@class,'ggj6brxn')]").text #Contato: André Oliveira
    ultima_msg = driver. find_element(By.XPATH,"//span[contains(@class,'Hy9nV')]").text #última mensagem no chat
    print("Nome do contato:"+contato)
    print("Última mensagem: "+ultima_msg)
    now = datetime.now()

    #inserindo contato e msg no banco de dados
    # Banco = criar banco simples com campos que você quer extrair
    # Esses campos extras estão nesse código por conta de outro banco que estou usando no momento da criação desse código
    sql = "INSERT INTO usuarios (nome, ultima_msg, email,created) VALUES (%s, %s, %s, %s)"
    val = (contato, ultima_msg, "teste@teste", now)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "registro inserido com sucesso!.")
   

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
    input('Press enter to exit\n')



if __name__ == "__main__":
    main()
