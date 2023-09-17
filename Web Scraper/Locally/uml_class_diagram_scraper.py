import utils
import sys

# Main
def main():

    # Assegurar o uso correto
    if len(sys.argv) != 3:
        sys.exit("Usage: python uml_class_diagram_scraper.py INITIAL_PAGE FINAL_PAGE")

    INITIAL_PAGE = int(sys.argv[1])
    FINAL_PAGE = int(sys.argv[2])

    # Verificar se a página final é menor que a página inicial
    if FINAL_PAGE < INITIAL_PAGE:
        sys.exit("The final page must be greater or equal than the initial page!")

    # Range de páginas
    pages = range(INITIAL_PAGE, FINAL_PAGE + 1)

    project_ids = []
    progress = 0
    
    # Para cada página do repositório público, obter os projetos
    for page in pages:
        print("A obter os projetos da página " + str(page) + "...")
        projects = utils.get_projects_of_page(page)
        
        # Obter o ID de cada projeto
        print("A obter os IDs dos projetos da página " + str(page) + "...\n")
        for project in projects:
            project_id = utils.project_id(project)

            # Verificar se o ID do projeto é válido
            if project_id is not None:
                project_ids.append(project_id)

    # Descarregar o XMI de cada projeto
    print("A descarregar os XMI dos projetos...\n")
    for project_id in project_ids:

        is_uml_class_diagram, content = utils.is_UML_class_diagram(project_id)

        # Verificar se o ficheiro XMI é um diagrama de classes UML
        if is_uml_class_diagram:
            
            # Verificar se o projeto já foi descarregado
            if not utils.is_project_downloaded(project_id):
                # Descarregar o XMI do projeto
                utils.download_xmi(content, project_id)

                # Guardar o ID do projeto descarregado
                utils.save_downloaded_project_id(project_id)

        # Mostrar o progresso
        progress += 1
        print("Download: " + str(progress) + "/" + str(len(project_ids)))


if __name__ == "__main__":
    main()