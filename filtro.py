#Importando os pacotes necessários.

from fileinput import close
import urllib.request
from bs4 import BeautifulSoup
import csv

#Link estático

TRANSPA_RES = "http://www.governotransparente.com.br/acessoinfo/44669490/consultarcontratoaditivo?ano=13&credor=-1&page=1&datainfo=%22MTIwMjIwNDA0MTE1MVBQUA==%22&inicio=01/01/2022&fim=04/04/2022&unid=&valormax=&valormin="

#Listas de dados

B = []
I = []

#Algoritimo de web-scrapping

for i in range(1,57):
  
  b = 'page='+str(++i)
  new_TRANSPA_RES = TRANSPA_RES.replace('page=1',b)

  #Acessando a página
  page = urllib.request.urlopen(new_TRANSPA_RES)
  soup = BeautifulSoup(page, 'html5lib')

  #Procura a Tabela
  table = soup.find('table', class_='table')

  #Retira as informações da Tabela

  for row in table.findAll("tr"):
    cells = row.findAll('td')
    if len(cells) == 10:
      B.append(cells[1].find(text=True))
      I.append(cells[8].find(text=True))

#Escre os dados em um arquivo CSV

with open('filtro.csv', 'w') as f:
  writer = csv.writer(f)
  writer.writerows(zip(B,I))
