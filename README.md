<h1 align="center">:file_cabinet: WhatsApp Web "Scraper" (teste) </h1>

## :memo: Descrição
Teste de web-scraping. A ideia inicial é coletar nome dos contatos e novas mensagens, e enviar via email.
(Um projeto com motivações pessoais, que poderá vir a servir para eu e alguns amigos, mas cuja intenção principal é iniciar na linguagem Python).

## :books: Issues
O WhatsApp Web gera as classes de maneria dinâmica. Caso queira testar essa versão do código, é necessário logar com seu WhatsApp Web (eu por exemplo, estou usando uma conta secundária, especificamente para testes), inspecionar a página e buscar o seletor que guarda o nome dos contatos;

*Geralmente, o nome do contato está numa tag <span> gerada dinamicamente, então, ao encontrá-la, basta selecionar uma parte do nome da class, e inserir no na variável 'contatos'. O mesmo processo deve ser feito para retornar a última mensagem do mesmo contato, alterando o seletor na variável 'mensagens'

## :wrench: Tecnologias utilizadas
* Python;
* Selenium;
* MySQL;

## :rocket: Rodando o projeto
Para rodar o código é necessário apenas baixar o mesmo, se certificar que o servidor web local está devidamente iniciado e configurado e dar o seguinte comando para iniciar o projeto:
```
python3 script.py
```

## :soon: Implementações futuras
* Enviar as mensagens armazenadas no banco por email;
* Várias outras ideias podem ser implementadas, mas vou buscar um passo de cada vez;

## :dart: Status do projeto
Em andamento...
