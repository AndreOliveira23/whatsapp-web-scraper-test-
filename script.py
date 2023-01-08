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
        contatos = driver.find_elements(By.CLASS_NAME, "_3OvU8")#Recuperando toda a informação na div de cada contato

        #iterando sobre contatos        
        for value in contatos:
            
            #Cada DIV no WhatsApp Web tem no mínimo 3 e no máximo 4 informações:
            #Nome do contato, dia ou hora da última mensagem, a mensagem em si (essas três, sempre) e 
            #o número de novas mensagens (somente para mensagens novas)
            
            #->A variável contatos guarda essas 3 ou 4 informações; Se o último caractere for um número, quer dizer que se trata
            #de uma nova mensagem recebida (pois o número é o número de novas mensagens no chat); 
            #Senão, quer dizer que a última mensagem foi enviada por você. (Por isso não tem número)

            #Dessa forma, o script reconhece novas mensagens e consegue filtrar pra enviar por email
            last = value.text[-1]

            if(last.isnumeric()):
                res = value.text.split() #Separando cada palavra para acessar os índices
                contato = res[0]+" "+res[1]+" "+res[2]
                ultimoIndex = res[len(res)-1] 
                mensagem = res[4]
                for x in range(5,len(res)-1,1):
                   mensagem = mensagem+" "+res[x]

                print(res)
                print("Size res: ",end="")
                print(len(res))
                print("contato: "+contato)
                print("Mensagem> "+mensagem)
                
                sql = "INSERT INTO whatsapp (Nome, Ultima_msg) VALUES (%s, %s)  ON DUPLICATE KEY UPDATE Ultima_msg=%s" #inserindo no banco de dados
                val = (contato, mensagem, mensagem)
                mycursor.execute(sql, val)
                mydb.commit()
                if(mycursor.rowcount !=0 ): print ("Banco de dados atualizado com sucesso! ")
                print("")    
                print("---------------------------------------------")


        time.sleep(10) #esperando 10 segundos antes de executar novamente
        print("fim da iteração")
        print("-------------------------------------------------------------------------------------")
    

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
