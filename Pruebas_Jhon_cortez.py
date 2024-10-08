import requests
from bs4 import BeautifulSoup
import webbrowser #proporciona una interfaz de alto nivel que permite mostrar documentos basados en web a los usuarios.

# Lista de URLs de los sitios web que deseas raspar
urls = [
    "https://www.fondoemprender.com/SitePages/Home.aspx"
]

# Función para extraer convocatorias de un sitio web
def extraer_convocatorias(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Aquí debes ajustar el selector según la estructura del HTML de cada sitio
        convocatorias = soup.find_all('div', class_='col-md-4')  # Cambia esto según el HTML

        resultados = []  # Lista para almacenar los resultados

        for convocatoria in convocatorias:
            # Ajusta el siguiente selector para extraer la información necesaria
            titulo = convocatoria.find('h5').text.strip()  # Cambia según el HTML
            fecha = convocatoria.find('span', class_='fecha').text.strip()  # Cambia según el HTML
            resultados.append({'titulo': titulo, 'fecha': fecha})
        
        return resultados
    else:
        print(f'Error al acceder a {url}: {response.status_code}')
        return []

# Generar el contenido HTML
html_content = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Convocatorias</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .convocatoria {
            margin-bottom: 20px;
        }
        .titulo {
            font-weight: bold;
        }
        .fecha {
            color: gray;
        }
    </style>
</head>
<body>
    <h1>Convocatorias Extraídas</h1>
'''

# Recorre cada URL y extrae las convocatorias
for url in urls:
    convocatorias = extraer_convocatorias(url)
    if convocatorias:
        html_content += f'<h2>Convocatorias de {url}:</h2>'
        for convocatoria in convocatorias:
            html_content += f'''
            <div class="convocatoria">
                <p class="titulo">{convocatoria['titulo']}</p>
                <p class="fecha">Fecha: {convocatoria['fecha']}</p>
            </div>
            '''
    else:
        html_content += f'<p>Error al acceder a {url}.</p>'

# Cerrar el contenido HTML
html_content += '''
</body>
</html>
'''

# Guardar el HTML en un archivo
with open('convocatorias.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

# Abrir el archivo en el navegador (opcional)
webbrowser.open('convocatorias.html')
