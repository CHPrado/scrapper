import sqlite3
from xlwt import Workbook

class ConexaoSQL:
  def getConexao(self):
    return sqlite3.connect('scrapper.db')

  def inserirImovel(self, id, descricao, area, precoVenda, precoAluguel, pais, 
              estado, cidade, regiao, bairro, logradouro, numero):
    conn = self.getConexao()
    c = conn.cursor()
    c.execute("INSERT INTO imovel (id, descricao, area, precoVenda, precoAluguel, pais, estado, cidade, regiao, bairro, logradouro, numero) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (id, descricao, area, precoVenda, precoAluguel, pais, estado, cidade, regiao, bairro, logradouro, numero))
    conn.commit()

  def filtrarBairro(self, bairro):
    conn = self.getConexao()
    c = conn.cursor()
    sql = "SELECT * FROM imovel WHERE bairro LIKE '%" + bairro.upper() + "%' ORDER BY precoVenda"
    c.execute(sql)
    dados_imoveis = c.fetchall()

    if len(dados_imoveis) > 0:
      nome_arquivo = 'Bairro {}'.format(bairro.upper())
      self.gerarExcel(nome_arquivo, dados_imoveis)
    else:
      print("Nenhum registro encontrado.")

  def filtrarMetragem(self, metragem):
    conn = self.getConexao()
    c = conn.cursor()
    sql = "SELECT * FROM imovel WHERE area = '" + metragem + "' ORDER BY precoVenda"
    c.execute(sql)
    dados_imoveis = c.fetchall()

    if len(dados_imoveis) > 0:
      nome_arquivo = 'Metragem {}'.format(metragem.upper())
      self.gerarExcel(nome_arquivo, dados_imoveis)
    else:
      print("Nenhum registro encontrado.")

  def filtrarPredio(self, logradouro, numero):
    conn = self.getConexao()
    c = conn.cursor()
    sql = "SELECT * FROM imovel WHERE logradouro LIKE '%" + logradouro + "%' AND numero = '" + numero + "' ORDER BY precoVenda"
    c.execute(sql)
    dados_imoveis = c.fetchall()

    if len(dados_imoveis) > 0:
      nome_arquivo = 'Predio logradouro - {}'.format(logradouro.upper())
      self.gerarExcel(nome_arquivo, dados_imoveis)
    else:
      print("Nenhum registro encontrado.")
  
  def listarTodos(self):
    conn = self.getConexao()
    c = conn.cursor()
    sql = "SELECT * FROM imovel ORDER BY precoVenda"
    c.execute(sql)
    dados_imoveis = c.fetchall()

    if len(dados_imoveis) > 0:
      nome_arquivo = 'LISTA COMPLETA SCRAPPER'
      self.gerarExcel(nome_arquivo, dados_imoveis)
    else:
      print("Nenhum registro encontrado.")

  def gerarExcel(self, nome_arquivo, dados_imoveis):
    wb = Workbook()
    sheet1 = wb.add_sheet('Página 1', cell_overwrite_ok=True)
    sheet1.col(0).width = 15000
    sheet1.col(1).width = 5000
    sheet1.col(2).width = 5000
    sheet1.col(3).width = 5000
    sheet1.col(4).width = 10000
    sheet1.col(5).width = 5000
    sheet1.col(6).width = 5000

    sheet1.write(0, 0, 'Descrição')
    sheet1.write(0, 1, 'Área (m²)')
    sheet1.write(0, 2, 'Valor de Venda R$')
    sheet1.write(0, 3, 'Valor de Aluguel R$')
    sheet1.write(0, 4, 'Logradouro')
    sheet1.write(0, 5, 'Número')
    sheet1.write(0, 6, 'Bairro')

    i = 1
    for imovel in dados_imoveis:
      sheet1.write(i, 0, imovel[1])
      sheet1.write(i, 1, imovel[2])
      sheet1.write(i, 2, imovel[3])
      sheet1.write(i, 3, imovel[4])
      sheet1.write(i, 4, imovel[10])
      sheet1.write(i, 5, imovel[11])
      sheet1.write(i, 6, imovel[9])

      i += 1
    try:
      wb.save('{}.xls'.format(nome_arquivo))
      print('Planilha Excel "{}" gerada'.format(nome_arquivo))
    except:
      print('Erro ao gerar planilha Excel. Talvez um arquivo com mesmo nome esteja aberto. Feche o arquivo e tente novamente.')