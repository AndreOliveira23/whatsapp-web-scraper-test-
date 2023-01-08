import time
import smtplib
import unicodedata
import mysql.connector
from threading import Timer
from inspect import getmembers



def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

def to_bytes(s):
    if type(s) is bytes:
         return s
    elif type(s) is str or (sys.version_info[0] < 3 and type(s) is unicode):
         return codecs.encode(s, 'utf-8')
    else:
        raise TypeError("Expected bytes or string, but got %s." % type(s))



#função email
def mail():
    while True:
        #Conectando com o banco de dados
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database ="meubanco"
        )

        mycursor = mydb.cursor()
        
        mycursor.execute('SELECT * FROM whatsapp')

        myresult = mycursor.fetchall()
        size = len(myresult)
        i=0
    

        for i in range(0,size,1):
            contato = to_bytes(myresult[i][0].encode('utf-8'))
            ultimaMSG = myresult[i][1]
            ultimaMsgPHP = myresult[i][2]

            #COmparando campos para ver se existem novas mensagems:
            if(ultimaMsgPHP == ultimaMSG):
                print("Não existem novas mensagens")
                print("contato: ",end='')
                print(to_bytes(contato).decode('utf-8'))
                print("msg>:"+ultimaMSG)
                print("ult php:> "+ultimaMsgPHP)
            else:
                print("Nova mensagem detectada!!")
                print("contato: ",end='')
                print(to_bytes(contato).decode('utf-8'))
                print("Mensagem: "+ultimaMSG)
                print("Enviando email....")

            
                #Enviando email
                gmail_user = 'emailRemetente@email.com' #Colocar o email que irá enviar as mensagens
                gmail_password = 'senha' #senha do email
                sent_from = gmail_user
               
                to = ['seuEmailPessoal@email.com'] #Destinatário - Email onde você quer receber as mensagens

                remetente = strip_accents(to_bytes(contato).decode('utf-8'))

                subject = "Mensagem de: "+remetente+" no Zip zoperson!"
                
                body = "Mensagem: "+ultimaMSG.encode('utf-8').decode('utf-8')
                
                message = 'Subject: {}\n\n{}'.format(subject, body)

                message = message.encode('utf-8')


                try:

                    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

                    smtp_server.ehlo()

                    smtp_server.login(gmail_user, gmail_password)

                    smtp_server.sendmail(sent_from, to, message)

                    smtp_server.close()

                    print ("Email enviado com sucesso!")

                    sql = "UPDATE whatsapp SET Ultima_msg_php = %s WHERE Nome = %s" #Atualizando campo no banco para comparar na próxima iteração
                    val = (ultimaMSG,contato)

                    mycursor.execute(sql,val)

                    mydb.commit()

                    if(mycursor.rowcount != 0): print("Última mensagem p atualizada com sucesso!")
                    print("")   
                    
                except Exception as ex:

                    print ("Something went wrong….",ex)

            print("fim da iteração")
            print("-------------------------------------------------------------------------------------")
            time.sleep(3) #esperando 10 segundos antes de executar novamente

def main():
    #mail inicia depois de 10 segundos
    t = Timer(10,mail)
    t.start()


if __name__ == "__main__":
    main()
