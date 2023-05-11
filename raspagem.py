import pandas as pd
import pdfquery
from bs4 import BeautifulSoup

## Passo 1: Converter o pdf em um arquivo xml com pdfquery
# Ler o .pdf
pdf = pdfquery.PDFQuery('file1.pdf')
pdf.load()

# Converter o pdf em .xml
pdf.tree.write('file1.xml', pretty_print=True)

## Passo 2: fazer mudanças manuais no xml, extraindo apenas a tabela de interesse
# Arquivo modificado salvo como file3.xml

## Passo 3: ler o conteúdo do xml e acessá-lo estruturadamente com o BeatifulSoup
# Importando o arquivo xml
file = open('file3.xml', 'r')  # r for read mode
contents = file.read()

# Raspar (scrap) os dados com o BeautifulSoup
sopinha = BeautifulSoup(contents, 'xml')

linha_a_linha = sopinha.find_all('LTTextLineHorizontal')

data = []

# Organizar as linhas uma a uma no objeto data
for i in range(0, len(linha_a_linha)):
    rows = [linha_a_linha[i].get_text()]
    data.append(rows)

# Converter o objeto data em um DataFrame do pandas
final_data = pd.DataFrame(data, columns=['Valores'])

# Exportar como csv...
# Arquivo é muito pequeno para pensar em como organizar isso programaticamente
df.to_csv(encoding='utf-8')

final_data.to_csv(
    r'/home/igor/Área de Trabalho/Solteiras/teste.csv', index=False
)
