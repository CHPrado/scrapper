import sqlite3

class ConexaoSQL:
  def getConexao(self):
    return sqlite3.connect('scrapper.db')

  def inserirImovel(self, descricao, area, precoVenda, precoAluguel, pais, 
              estado, cidade, regiao, bairro, logradouro, numero):
    conn = self.getConexao()
    c = conn.cursor()
    c.execute("INSERT INTO imovel (descricao, area, precoVenda, precoAluguel, pais, estado, cidade, regiao, bairro, logradouro, numero) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
              (descricao, area, precoVenda, precoAluguel, pais, estado, cidade, regiao, bairro, logradouro, numero))
    print("Imóvel adicionado...")
    conn.commit()

  def filtrarBairro(self, bairro):
    conn = self.getConexao()
    c = conn.cursor()
    sql = "SELECT * FROM imovel WHERE bairro = '" + bairro.upper() + "'"
    c.execute(sql)
    dados_imoveis = c.fetchall()

    for imovel in dados_imoveis:
      output = "Área: {}m². ".format(imovel[2])
      if imovel[3] == 'None':
        output = output + "Valor de Aluguel: R$ {0:2.2f}.".format(imovel[4])
      else:
        output = output + "Valor de Venda: R$ {0:2.2f}.".format(imovel[3])

      print(output)

  def filtrarMetragem(self, metragem):
    conn = self.getConexao()
    c = conn.cursor()
    sql = "SELECT * FROM imovel WHERE area = '" + metragem + "'"
    c.execute(sql)
    dados_imoveis = c.fetchall()

    for imovel in dados_imoveis:
      output = "Área: {}m². ".format(imovel[2])
      if imovel[3] == 'None':
        output = output + "Valor de Aluguel: R$ {0:2.2f}.".format(imovel[4])
      else:
        output = output + "Valor de Venda: R$ {0:2.2f}.".format(imovel[3])

      print(output)

  def filtrarPredio(self, logradouro, numero):
    conn = self.getConexao()
    c = conn.cursor()
    sql = "SELECT * FROM imovel WHERE logradouro = '" + logradouro + "' AND numero = '" + numero + "'"
    c.execute(sql)
    dados_imoveis = c.fetchall()

    for imovel in dados_imoveis:
      output = "Área: {}m². ".format(imovel[2])
      if imovel[3] == 'None':
        output = output + "Valor de Aluguel: R$ {0:2.2f}.".format(imovel[4])
      else:
        output = output + "Valor de Venda: R$ {0:2.2f}.".format(imovel[3])

      print(output)
