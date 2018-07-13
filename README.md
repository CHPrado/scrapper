# Zap Imoveis Scrapper

Para executar pelo terminal entre no diretório /venc/scripts e ative o ambiente virtual digitando activate.
Depois retorne à raiz e execute o aplicativo scrapper digitando python scrapper.py

O programa salva no banco os dados dos imóveis listados na página principal do site. Caso a quantidade de imóveis listada na página principal seja inferior à quantidade mínima de imóveis informada no código, o programa irá mudar para as próximas páginas até que essa quantidade seja atingida.
Está disponível as opções de gerar planinlhas Excel contendo todos os imóveis salvos no banco de dados, ou filtrados por bairro, metragem, e por prédio (informando logradouro e número).

Para o desenvolvimento do projeto foi utilizada a ferramenta BeautifulSoup para coletar as informações dos imóveis do site. SQLite3 para criar o banco de dados e XLWT para gerar as planilhas Excel.
