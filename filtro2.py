from cgitb import text
from fileinput import close
import urllib.request
from bs4 import BeautifulSoup
import csv

#DECLARADO VARIÁVEIS GLOBAIS

I_DATA = str(input('Digite a data de ínicio:\n'))
F_DATA = str(input('Digite a data de fim:\n'))
URL_TRANSP = str("http://www.governotransparente.com.br/acessoinfo/44669490/consultarcontratoaditivo?ano=13&credor=-1&page=1&datainfo=%22MTIwMjIwNDA0MTE1MVBQUA==%22&inicio=" + I_DATA + "&fim=" + F_DATA + "&unid=&valormax=&valormin=")
NUM_CONTRATO = []
NUM_ANEXOS = []


#Acessando a Página
page = urllib.request.urlopen(URL_TRANSP)
soup = BeautifulSoup(page,'html5lib')
#print(soup.prettify)


#Procurando quantidade de páginas
TOTAL = []
tabela = soup.find_all('p')
for p in tabela:
    TOTAL.append(p)
total = str(TOTAL[0]).split()
quant_TOTAL_i = int(total[6]) #quantidade total de contratos
quant_TOTAL_pag = (quant_TOTAL_i // 10) + 2 #quantidade total de páginas a serem executadas


#Algortimo de Web-scrapping
index_s = 0
for i in range(1 , quant_TOTAL_pag):
    b = 'page='+str(++i)
    new_URL_TRANSP = URL_TRANSP.replace('page=1', b )

    #Acessando a página
    page = urllib.request.urlopen(new_URL_TRANSP)
    soup = BeautifulSoup(page, 'html5lib')

    #Procura a tabela
    table = soup.find('table', class_ = 'table')

    #Retira as informações da tabela

    for row in table.findAll('tr'):
        cells = row.findAll('td')
        if len(cells) == 10:
            NUM_CONTRATO.append(cells[1].find(text=True))
            NUM_ANEXOS.append(int(cells[8].find(text=True)))
    index_s += 1
    print(f'Estou colhendo os dados, restam {quant_TOTAL_pag - index_s} páginas para seren análisadas.')

#Filtrando por apenas contratos sem anexos

CONTRATOS_SEM_ANEXO = []

index_f = 0
for i in NUM_ANEXOS:  
    if i == 0:
        index_f += 1
        CONTRATOS_SEM_ANEXO.append(NUM_CONTRATO[index_f - 1])
    else: 
        index_f += 1
        continue
    print(f'Estou filtrando os contratos que faltam anexos! Atualmente temos {len(CONTRATOS_SEM_ANEXO)} nesta condição.')
   
print(f'Pronto, agora só irei escrever um arquivo com o nome dos contratos!')

#Escreve os dados em um arquivo CSV

with open('filtro.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(CONTRATOS_SEM_ANEXO))