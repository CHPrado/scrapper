import sys
import requests
import re
from bs4 import BeautifulSoup as BS
from conexaoDB import ConexaoSQL

class ZapImoveis:
  def __init__(self):
    self.SCRAPPING = 100 #QUANTIDADE DE IMOVEIS A SEREM VARRIDOS POR EXECUÇÃO
    self.url = 'https://www.zapimoveis.com.br/tr/imoveis/sp'
    self.agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    self.conn = ConexaoSQL()

  def _get_descricao(self, bs_detalhe):
    return bs_detalhe.find('div', class_='descricao').text.replace('\n', '').replace('\r', '').replace('Ver descrição completa', '')

  def _get_area(self, bs_detalhe):
    return str(bs_detalhe.find('input', {'id' : 'areaUtil'}).get('value'))

  def _get_precoVenda(self, bs_detalhe):
    return str(bs_detalhe.find('input', {'id' : 'precoVenda'}).get('value'))
  
  def _get_precoAluguel(self, bs_detalhe):
    return str(bs_detalhe.find('input', {'id' : 'precoAluguel'}).get('value'))

  def _get_endereco(self, bs_detalhe):
    return re.split('[;]', str(bs_detalhe.find('input', {'id' : 'address'}).get('value')))

  def listarImoveis(self):
    main_page = requests.get(self.url, headers=self.agent)
    bs = BS(main_page.text, 'lxml')
    return bs.find_all('article', class_='minificha')

  def detalhesImovel(self, imovel):
    url_imovel = imovel.find('a').get('href')
    detalhe_imovel = requests.get(url_imovel, headers=self.agent)
    return BS(detalhe_imovel.text, 'lxml')

  def navegar(self):
    print("Varrendo imóveis de Zap Imoveis...")
    #NAVEGA NA PÁGINA PRINCIPAL E COLETA AS URL DOS IMÓVEIS LISTADOS
    lista_imoveis = self.listarImoveis()
    i = 0
    for imovel in lista_imoveis:
      bs_detalhe = self.detalhesImovel(imovel)

      #IMÓVEIS COM STATUS 'EM OBRA' TEM A PÁGINA DIFERENTE DOS DEMAIS, POR ISSO
      #AS PÁGINAS CONTEM TAGS DIFERENTES FAZENDO COM QUE RETORNE NONETYPE
      #OBS: A MAIORIA COM PREÇOS SOB CONSULTA.
      try: 
        descricao = self._get_descricao(bs_detalhe)
        area = self._get_area(bs_detalhe)
        endereco = self._get_endereco(bs_detalhe)
        precoVenda = self._get_precoVenda(bs_detalhe)
        precoAluguel = self._get_precoAluguel(bs_detalhe)

        pais = endereco[0].upper()
        estado = endereco[1].upper()
        cidade = endereco[2].upper()
        regiao = endereco[3].upper()
        bairro = endereco[4].upper()
        logradouro = endereco[5].upper()
        numero = endereco[6]
        # id = endereco[7]

        # print('Descrição: {}\n'.format(descricao))
        # print('Área : {}m², Preço Venda: {}, Preço Aluguel: {}'.format(area, precoVenda, precoAluguel))   
        # print('Logradouro: {}, nº: {}, Bairro: {}, Regiao: {}, Cidade: {}, Estado: {}\n\n'.format(logradouro, numero, bairro, regiao, cidade, estado))

        self.conn.inserirImovel(descricao, area, precoVenda, precoAluguel, pais, 
                                estado, cidade, regiao, bairro, logradouro, numero)
        i += 1

      except: #PARA PÁGINAS COM STATUS 'EM OBRA'. 
        pass
        # descricao = bs_detalhe.find('span', class_='descricao').text
        # areaMin = str(bs_detalhe.find('input', {'id' : 'hdnareaMin'}).get('value'))
        # areaMax = str(bs_detalhe.find('input', {'id' : 'hdnareaMax'}).get('value'))
        # preco = bs_detalhe.find('span', class_='dados-ficha').text
        # endereco = re.split('[;]', str(bs_detalhe.find('input', {'id' : 'hdnsaddress'}).get('value')))
        
        # pais = endereco[0]
        # estado = endereco[1]
        # cidade = endereco[2]
        # regiao = endereco[3]
        # bairro = endereco[4]
        # logradouro = endereco[5]
        # numero = endereco[6]
        # id = endereco[7]

        # print('Descrição: {}\n'.format(descricao))
        # print('Área mínima: {}m², Área máxima: {}, Preço: {}'.format(areaMin, areaMax, preco))   
        # print('Logradouro: {}, nº: {}, Bairro: {}, Regiao: {}, Cidade: {}, Estado: {}\n\n'.format(logradouro, numero, bairro, regiao, cidade, estado))

    print("Scrapper finalizado. {} imóveis adicionados no banco de dados.".format(i))
    #return "Scrapper finalizado. {} imóveis adicionados no banco de dados.".format(i)

  def filtrarBairro(self):
    bairro = input("Informe o bairro: ")
    self.conn.filtrarBairro(bairro)

  def filtrarMetragem(self):
    metragem = input("Informe a metragem (em m²): ")
    self.conn.filtrarMetragem(metragem)

  def filtrarPredio(self):
    logradouro = input("Informe o logradouro: ")
    numero = input("Informe o número do prédio: ")
    self.conn.filtrarPredio(logradouro, numero)

  def iniciar(self):
    while True:
      print("MENU\n"
        "1. Inicializar Scrapper.\n"
        "2. Filtrar por Metragem.\n"
        "3. Filtrar por Prédio.\n"
        "4. Filtrar por Bairro.\n"
        "0. Sair.\n")

      option = input("Opção: ")

      if option == '1':
        zap.navegar()
      elif option == '2':
        zap.filtrarMetragem()
      elif option == '3':
        zap.filtrarPredio()
      elif option == '4':
        zap.filtrarBairro()
      elif option == '0':
        break

if __name__ =="__main__":
  zap = ZapImoveis()
  zap.iniciar()


