import re
import requests
from bs4 import BeautifulSoup

# URL do GenMyModel
URL = "https://app.genmymodel.com"

# URL do repositório público
PUBLIC_REPOSITORY_URL = URL + "/api/repository/public/"
# Query
PUBLIC_REPOSITORY_URL_QUERY = "?q=&type=UML"

# URL da API
API_URL = URL + "/api/projects/"
# Query
API_URL_QUERY = "xmi?withDiagrams=true"

# Pasta onde os ficheiros XMI são guardados
XMI_PATH = "Dataset/"

# Ficheiro onde os IDs dos projetos descarregados são guardados
DOWNLOADED_FILES = "downloaded_files.txt"

# Elementos essenciais dos diagramas de classes UML
UML_CLASS_DIAGRAM_ELEMENTS = ["uml:Class", "uml:Interface", "uml:DataType", "uml:Enumeration"]


# Função para alterar a página do url
def change_page(page):
    # Separar o URL em partes
    url = PUBLIC_REPOSITORY_URL.split("/")

    # Alterar a última parte do URL
    url[-1] = str(page)

    # Juntar o URL
    url = "/".join(url)

    # Adicionar a query
    url += PUBLIC_REPOSITORY_URL_QUERY

    return url


# Função para obter os projetos de uma página
def get_projects_of_page(page):
    # Construir o URL da página
    url = change_page(page)

    # Fazer o pedido à página
    response = requests.get(url)
    
    # Verificar se a página existe
    if response.status_code != 200:
        return None
    
    # Obter o conteúdo da página
    content = response.content

    # Fazer parse do conteúdo da página
    soup = BeautifulSoup(content, 'html.parser')

    # Encontrar todas as tags "a" com a classe "ui card public-project blue"
    links = soup.find_all('a', class_='ui card public-project blue')

    # Extrair as URLs dos projetos
    project_urls = [URL + link['href'] for link in links]

    return project_urls


# Função para obter o ID de um projeto
def project_id(project_url):
    # Fazer o pedido à página
    response = requests.get(project_url)

    # Verificar se a página existe
    if response.status_code != 200:
        return None
    
    # Obter o conteúdo da página
    content = response.content

    # Fazer parse do conteúdo da página
    soup = BeautifulSoup(content, 'html.parser')

    # Obter a tag meta og:image
    og_image_tag = soup.find('meta', {'property': 'og:image'})

    # Extrair o ID do projeto usando expressões regulares
    try:
        project_id = re.search(r'/projects/([^/]+)/', og_image_tag['content'])
    except:
        return None

    return project_id.group(1)


# Função para obter o XMI de um projeto
def project_xmi(project_id):
    url = API_URL + project_id + "/" + API_URL_QUERY
    return url


# Função para verificar se é um diagrama de classes UML
def is_UML_class_diagram(project_id):
    # Obter o URL do XMI
    url = project_xmi(project_id)

    # Fazer o pedido à página
    response = requests.get(url)

    # Verificar se a página existe
    if response.status_code != 200:
        return False, None
    
    # Obter o conteúdo do ficheiro XMI
    content = response.content

    # Fazer parse do conteúdo da página
    soup = BeautifulSoup(content, 'xml')
    
    # Verificar se o ficheiro XMI contém os elementos essenciais de um diagrama de classes UML
    elements = soup.find_all('packagedElement', {'xsi:type': UML_CLASS_DIAGRAM_ELEMENTS})

    if elements:
        return True, content
    else:
        return False, None


# Função para guardar o ID de um projeto descarregado, adicionando-o a um ficheiro
def save_downloaded_project_id(project_id):
    # Escrever os ID dos projetos no ficheiro
    with open(DOWNLOADED_FILES, "a") as file:
            file.write(project_id + "\n")


# Função para fazer download do XMI de um projeto
def download_xmi(content, project_id):
    # Definir Path do Google Drive
    PATH = ""

    # Guardar o ficheiro XMI
    filename = PATH + f"/Web Scraper/Google Colab/Dataset/{project_id}.xmi"
    with open(filename, "wb") as file:
        file.write(content)
    
    return filename


# Função para verificar se um projeto já foi descarregado
def is_project_downloaded(project_id):
    # Ler o ficheiro com os IDs dos projetos descarregados
    with open(DOWNLOADED_FILES, "r") as file:
        if project_id in file.read():
            return True
        else:
            return False