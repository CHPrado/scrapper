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
    
    conn.commit()