import re
import sys

texto = sys.argv[1]
estilo = sys.argv[2] if len(sys.argv) > 2 else ''
print("estilo:", estilo)
with open(texto, 'r') as texto:
    texto = texto.read()
    print(texto, '\n\n')

def compilar(texto):
    texto = negitalico(texto)
    texto = negrito(texto)
    texto = italico(texto)
    texto = paragrafo(texto)
    texto = subseccao(texto)
    texto = seccao(texto)
    texto = capitulo(texto)
    texto = titulo(texto)
    texto = ul(texto)
    texto = ol(texto)
    return texto

def negitalico(texto):
    texto = re.sub(r'\*{3}(.*)\*{3}', '<strong><em>\\1</em></strong>', texto)
    texto = re.sub(r'_{3}(.*)_{3}', '<strong><em>\\1</em></strong>', texto)
    return texto

def negrito(texto):
    texto = re.sub(r'\*{2}(.*)\*{2}', '<strong>\\1</strong>', texto)
    texto = re.sub(r'_{2}(.*)_{2}', '<strong>\\1</strong>', texto)
    return texto
    
def italico(texto):
    texto = re.sub(r'\*(.*)\*', '<em>\\1</em>', texto)
    texto = re.sub(r'_(.*)_', '<em>\\1</em>', texto)
    return texto

def paragrafo(texto):
    texto = re.sub(r'(\r\n|\r|\n|^)+([^\r\n#!\-\d]+)', '\n<p>\\2</p>', texto)
    return texto

def subseccao(texto):
    texto = re.sub(r'#{3}\s?(.*)', '<h3>\\1</h3>', texto)
    return texto

def seccao(texto):
    texto = re.sub(r'#{2}\s?(.*)', '<h2>\\1</h2>', texto)
    return texto

def capitulo(texto):
    texto = re.sub(r'#\s?(.*)', '<h1>\\1</h1>', texto)
    return texto

def titulo(texto):
    texto = re.sub(r'!(.*)!', '<title>\\1</title>', texto)
    return texto

def ul(texto):
    texto = re.sub(r'(-)(.*)', '<ul>\\1\\2', texto, 1)
    texto = re.sub(r'-(.*)', '<li>\\1</li>', texto)
    return texto

def ol(texto):
    texto = re.sub(r'([0-9]+\.)(.*)', '<ol>\\1\\2', texto, 1)
    texto = re.sub(r'[0-9]+\.(.*)', '<li>\\1</li>', texto)
    return texto

resultado = sys.argv[1].split('.', 1)[0] + '.html'
print(resultado)
#print(compilar(texto))
with open(resultado, 'w') as wf:
    wf.write(compilar(texto))

lista_palavras = []
with open(resultado, 'r') as final:
    texto = final.readlines()
    
    for linha in texto:
        lista_palavras += linha.split('\n')

novo_titulo = ''
lista_palavras = [x for x in lista_palavras if x]
lista_palavras += ['']
print(lista_palavras)
pos_compilado = ''
for i in range(len(lista_palavras)):
    #print(lista_palavras[i])
    if lista_palavras[i][-5:] == '</li>' and lista_palavras[i+1][:4] != '<li>':
        lista_palavras[i] += '</ul></ol>'

    if '<title>' in lista_palavras[i]:
        novo_titulo = lista_palavras[i]
        lista_palavras[i] = ''
        
    pos_compilado += lista_palavras[i] + '\n'


header = '''<html>
<head>
''' + novo_titulo + '''
<link rel="stylesheet" href="''' + estilo + '''">
</head>
<body>
'''
footer = '''</body>
</html>'''

pos_compilado = header + pos_compilado + footer

print(pos_compilado)
with open(resultado, 'w') as wf:
    wf.write(pos_compilado)