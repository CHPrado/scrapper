import requests
import re
from bs4 import BeautifulSoup as BS

url = 'https://www.zapimoveis.com.br/tr/imoveis/sp'
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
main_page = requests.get(url, headers=agent)

soup = BS(main_page.text, 'lxml')

lista_imoveis = soup.find_all('article', class_='minificha')

for imovel in lista_imoveis:
  url_imovel = imovel.find('a').get('href')
  #print(url_imovel)

  detalhe_imovel = requests.get(url_imovel, headers=agent)
  bs_page = BS(detalhe_imovel.text, 'lxml')

  #IMÓVEIS COM STATUS 'EM OBRA' TEM A PÁGINA DIFERENTE DOS DEMAIS, POR ISSO
  #AS PÁGINAS CONTEM TAGS DIFERENTES FAZENDO COM QUE RETORNE NONETYPE
  try: 
    descricao = bs_page.find('div', class_='descricao').text
    preco = (re.sub(' +', ' ', bs_page.find('div', class_='value-ficha').text)).replace('\n', '').replace('\r', '')
    
    print('Descrição: {}\n'.format(descricao))
    print('{}\n'.format(preco))   
  except: #PARA PÁGINAS COM STATUS 'EM OBRA'
    # descricao = bs_page.find('span', class_='descricao').text
    # preco = bs_page.find('span', class_='dados-ficha').text

    # print('Descrição: {}\n'.format(descricao))
    # print('{}\n'.format(preco)) 
    pass



