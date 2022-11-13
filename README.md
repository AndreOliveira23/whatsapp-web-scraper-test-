<h1 align="center">:file_cabinet: WhatsApp Web "Scraper" (teste) </h1>

## :memo: Descrição
Teste de web-scraping. A ideia inicial é coletar nome dos contatos e novas mensagens, e enviar via email.
(Um projeto com motivações pessoais, que poderá vir a servir para eu e alguns amigos, mas cuja intenção principal é iniciar na linguagem Python).

## :books: Isses
*POr enquanto, o script retorna 1 contato, de maneira estática, então, caso queira testar essa versão do código, é necessário logar com seu WhatsApp Web (eu por exemplo, estou usando uma conta secundária, especificamente para testes), inspecionar a página e buscar o seletor que guarda o nome do contato desjeado;
*Geralmente, o nome do contato está numa tag <span> gerada dinamicamente, então, ao encontrá-la, basta selecionar uma parte do nome da class, e inserir no na linha 35. O mesmo processo deve ser feito para retornar a última mensagem do mesmo contato, alterando o seletor na linha 36

## :wrench: Tecnologias utilizadas
* Python;
* Selenium;
* PHP (futuramente);
* MySQL;

## :rocket: Rodando o projeto
Para rodar o código é necessário apenas baixar o mesmo, se certificar que o servidor web local está devidamente iniciado e configurado e dar o seguinte comando para iniciar o projeto:
```
python3 script.py
```

## :soon: Implementações futuras
* Idealmente, o script deverá coletar os contatos de forma dinâmica;
* Várias outras ideias podem ser implementadas, mas vou buscar um passo de cada vez;

## :dart: Status do projeto
Em andamento...
