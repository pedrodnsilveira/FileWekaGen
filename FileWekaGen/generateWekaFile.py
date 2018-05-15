#!/usr/bin/python
import MySQLdb
import sys

if len(sys.argv) != 3:
    print "ERROR. Usage: generateWekaFile.py [(string)file_name.arff] [(string)SQL_query]\n"
    exit()

if ".arff" not in sys.argv[1]:
    print "ERROR. File name must be an \".arff\" file.\n"
    exit()

#recebe um inteiro (posicao), pega a coluna do resultSet referente a essa posicao e retorna
#todos os valores distintos dessa coluna jah no formato do arquivo .arff em forma de texto
def getDistinctAtributeValues( pos ):
    fielDistinctValues = [row[pos] for row in dataSet]
    fielDistinctValues = set(fielDistinctValues)
    fielDistinctValues = list(fielDistinctValues)
    txt = "{"
    for x in fielDistinctValues:
        txt = txt + "'" + x + "'" + ","
    txt = txt + "}"
    txt = txt.replace("'',","")
    txt = txt.replace(",}","}")
    return txt;

fileName = str(sys.argv[1])
query = str(sys.argv[2])

# Gera a string de conexao ex.: seu host, seu usuario, sua senha e seu db
db = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="testLA")
# Posiciona o cursor
cursor = db.cursor()
# Executa a consulta
cursor.execute(query)
# Conta o numero de linhas na tabela
numrows = int(cursor.rowcount)

#pega as informacoes sobre os campos da tabela
fieldInfo = cursor.description

#pega os dados da consulta
dataSet = cursor.fetchall()

#preenche o header do arquivo
head = "@relation "+fileName.replace(".arff","")+"\n\n"
col = 0
for x in fieldInfo:
    #verifica se o tipo do atributo eh string, text ou varchar
    if (x[1] == 15) or (x[1] == 253) or (x[1] == 254):
        t = getDistinctAtributeValues(col)
    else:
        t = "numeric"
    head = head + "@attribute " + x[0] + " " + t + "\n"
    col = col + 1
head = head + "\n@data\n"

#preenche o corpo do arquivo
body=""
for row in dataSet:
    for v in row:
        body = body + "'" + str(v) + "'" + ","
    body = body[:-1] + "\n"
body = body.replace("'',","?,")

texto = head + body[:-1]

#gera o arquivo .arff
f1=open(fileName, 'w+')
print >>f1, texto