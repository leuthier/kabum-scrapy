#### Utilizando Scrapy para extrair dados da KaBuM
#### Site: http://www.kabum.com.br/

#### Tutorial

$ rethinkdb
```
$ git clone https://github.com/leuthier/kabum-scrapy
$ pip install -r requirements.txt
$ cd kb
$ scrapy crawl kb -o computers.json
$ scrapy runspider login.py
``` 

#### Índice
  * [Objetivos](https://github.com/leuthier/kabum-scrapy/blob/master/README.md#objetivos)
  * Arquivos:
      * [/kabum/spiders/kb.py](https://github.com/leuthier/kabum-scrapy/blob/master/README.md)
      * [/kabum/pipelines.py](https://github.com/leuthier/kabum-scrapy/blob/master/README.md)
      * [/kabum/items.py](https://github.com/leuthier/kabum-scrapy/blob/master/README.md)
  * [Tempo gasto](https://github.com/leuthier/kabum-scrapy/blob/master/README.md#tempo-gasto)
  * [Programas utilizados](https://github.com/leuthier/kabum-scrapy/blob/master/README.md#programas-utilizados)
  * [Referências](https://github.com/leuthier/kabum-scrapy/blob/master/README.md#material)


#### Objetivos
- [x] Utilização de ```xpath``` nas buscas por links
- [x] Persistência das informações (RethinkDB)
- [x] Submissão de formulários
- [x] Utilização de logs para sinalizar ocorrências durante o scraping


#### Arquivo: [/kabum/spiders/kb.py](https://github.com/leuthier/kabum-scrapy/blob/master/kabum/spiders/kb.py)
``` code here 
```

#### Arquivo: [/kabum/pipelines.py](https://github.com/leuthier/kabum-scrapy/blob/master/kabum/pipelines.py)
``` code here 
```

#### Arquivo: [/kabum/settings.py](https://github.com/leuthier/kabum-scrapy/blob/master/kabum/settings.py)
``` code here 
```

#### Arquivo: [/kabum/items.py](https://github.com/leuthier/kabum-scrapy/blob/master/kabum/items.py)
``` code here 
```
 
 
#### Tempo gasto
  * Estudando:
  * Implementando:


#### Programas utilizados
  * [XPath Helper](https://chrome.google.com/webstore/detail/xpath-helper/hgimnogjllphhhkhlmebbmlgjoejdpjl)
  * [RethinkDB](https://www.rethinkdb.com/docs/install/)
  
  
#### Referências
  * [Guia de 10min com RethinkDB e Python [ENG]](https://www.rethinkdb.com/docs/guide/python/)
  * [Parte I - Configurando e rodando o Scrapy](http://www.gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-i/)
  * [Instalando, configurando e armazenando os dados no Rethinkdb](http://www.gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-ii/)
  * [XPath Tutorial [ENG]](https://www.w3schools.com/xml/xpath_intro.asp)