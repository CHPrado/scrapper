import sys
import requests
import re
from bs4 import BeautifulSoup as BS
from conexaoDB import ConexaoSQL

class ZapImoveis:
  def __init__(self):
    self.QTD_IMOVEIS = 30 #QUANTIDADE MÍNIMA DE IMÓVEIS A SEREM SCANNEADOS DO SITE
    self.pagina = 1 #PAGINA ATUAL
    #URL INICIAL
    self.url = 'https://www.zapimoveis.com.br/tr/imoveis/sp+sao-paulo/?gclid=CjwKCAjw1ZbaBRBUEiwA4VQCIUwVQNUVCZnEDpCYPLQ4dKPqhIQ4IkOsxiudPNjn7XmXEeoKQhi5HxoCbZUQAvD_BwE#{"precomaximo":"2147483647","parametrosautosuggest":[{"Bairro":"","Zona":"","Cidade":"SAO%20PAULO","Agrupamento":"","Estado":"SP"}],"pagina":"1","ordem":"Relevancia","paginaOrigem":"ResultadoBusca","semente":"1413743582","formato":"Lista"}'
    self.agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    self.conn = ConexaoSQL()

  def _get_descricao(self, bs_detalhe):
    try:
      descricao = bs_detalhe.find('div', class_='descricao').text.replace('\n', '').replace('\r', '').replace('Ver descrição completa', '')
    except:
      descricao = bs_detalhe.find('span', class_='descricao').text
    return descricao

  def _get_area(self, bs_detalhe):
    try:
      area = str(bs_detalhe.find('input', {'id' : 'areaUtil'}).get('value'))
    except:
      area = str(bs_detalhe.find('input', {'id' : 'hdnareaMin'}).get('value'))
    return area

  def _get_precoVenda(self, bs_detalhe):
    try:
      preco = str(bs_detalhe.find('input', {'id' : 'precoVenda'}).get('value'))
    except:
      preco = bs_detalhe.find('span', class_='dados-ficha').text
    return preco
  
  def _get_precoAluguel(self, bs_detalhe):
    return str(bs_detalhe.find('input', {'id' : 'precoAluguel'}).get('value'))

  def _get_endereco(self, bs_detalhe):
    try:
      endereco = re.split('[;]', str(bs_detalhe.find('input', {'id' : 'address'}).get('value')))
    except:
      endereco = re.split('[;]', str(bs_detalhe.find('input', {'id' : 'hdnsaddress'}).get('value')))
    return endereco

  def listarImoveis(self):
    self.url = 'https://www.zapimoveis.com.br/tr/imoveis/sp+sao-paulo/?gclid=CjwKCAjw1ZbaBRBUEiwA4VQCIUwVQNUVCZnEDpCYPLQ4dKPqhIQ4IkOsxiudPNjn7XmXEeoKQhi5HxoCbZUQAvD_BwE#{"precomaximo":"2147483647","parametrosautosuggest":[{"Bairro":"","Zona":"","Cidade":"SAO%20PAULO","Agrupamento":"","Estado":"SP"}],"pagina":"'+str(self.pagina)+'","ordem":"Relevancia","paginaOrigem":"ResultadoBusca","semente":"1413743582","formato":"Lista"}'
    main_page = requests.get(self.url, headers=self.agent)
    bs = BS(main_page.text, 'lxml')
    return bs.find_all('article', class_='minificha')

  def detalhesImovel(self, imovel):
    url_imovel = imovel.find('a').get('href')
    detalhe_imovel = requests.get(url_imovel, headers=self.agent)
    return BS(detalhe_imovel.text, 'lxml')

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
  
  def listarTodos(self):
    self.conn.listarTodos()

  def navegar(self):
    print("Varrendo imóveis de Zap Imoveis...")
    qtd_imoveis = 0
    #NAVEGA NA PÁGINA PRINCIPAL E COLETA AS URL DOS IMÓVEIS LISTADOS
    while True:
      print("Página {}...".format(self.pagina))
      lista_imoveis = self.listarImoveis()
      
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
          id = int(endereco[7])

          self.conn.inserirImovel(id, descricao, area, precoVenda, precoAluguel, pais, 
                                  estado, cidade, regiao, bairro, logradouro, numero)
          qtd_imoveis += 1

        except: # Exception as e:  
          # print(e)
          pass

      #MANTEM O LOOP ENQUANTO NAO ATINGIR A QUANTIDADE MÍNIMA DE IMÓVEIS 
      if qtd_imoveis >= self.QTD_IMOVEIS:
        break
      else:
        #PASSA PARA PRÓXIMA PÁGINA
        self.pagina += 1
        
    print("Scrapper finalizado. {} imóveis adicionados no banco de dados.".format(qtd_imoveis))

  def iniciar(self):
    while True:
      print("\n===ZAP IMOVEIS SCRAPPER===\n"
        "1. Inicializar Scrapper.\n"
        "2. Filtrar por Metragem.\n"
        "3. Filtrar por Prédio.\n"
        "4. Filtrar por Bairro.\n"
        "5. Gerar planilha com todos os imóveis.\n"
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
      elif option =='5':
        zap.listarTodos()
      elif option == '0':
        break

if __name__ =="__main__":
  zap = ZapImoveis()
  zap.iniciar()


