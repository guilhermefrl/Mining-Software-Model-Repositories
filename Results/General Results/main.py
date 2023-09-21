# -*- coding: utf-8 -*-

import sys
import csv
import xml.etree.ElementTree as ET

# Função para ler o range de IDs do ficheiro txt
def read_files_ids(initial_file, final_file):

    FOLDER = "../Scraper/Google Colab/"
    FILE = "downloaded_files.txt"

    # Abrir o ficheiro e ler as linhas
    with open(FOLDER + FILE, 'r') as file:
        lines = file.read().splitlines()        

    return lines[initial_file:final_file]


# Função para ler um ficheiro
def read_xmi_file(filename):

    tree = ET.parse(filename + ".xmi")
    root = tree.getroot()

    return root


# Função para obter o número de cada tipo de elemento no diagrama
def check_number_of_different_element_types(root):
    count = {
        "Package": 0,
        "Class": 0,
        "Interface": 0,
        "DataType": 0,
        "Attribute": 0,
        "Operation": 0,
        "Enumeration": 0,
        "Enumeration_Literal": 0,
        "Generalization": 0,
        "Realization": 0,
        "Dependency": 0,
        "Usage": 0,
        "Import": 0,
        "Template_Binding": 0,
        "Association": 0,
        "Composition": 0,
        "Aggregation": 0,
        "Inner_relation": 0,
        "Association_Class": 0
    }

    # -> Entities:

    # Package
    Packages = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Package']")

    if len(Packages) > 0:
        count["Package"] = len(Packages)

    # Class
    Classes = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Class']")

    if len(Classes) > 0:
        count["Class"] = len(Classes)

    # Interface
    Interfaces = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Interface']")

    if len(Interfaces) > 0:
        count["Interface"] = len(Interfaces)
    
    # DataType
    DataTypes = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:DataType']")

    if len(DataTypes) > 0:
        count["DataType"] = len(DataTypes)

    # Attribute
    Attributes = root.findall(".//ownedAttribute")

    if len(Attributes) > 0:
        count["Attribute"] = len(Attributes)

    # Operation
    Operations = root.findall(".//ownedOperation")

    if len(Operations) > 0:
        count["Operation"] = len(Operations)

    # Enumeration
    Enumeratios = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Enumeration']")

    if len(Enumeratios) > 0:
        count["Enumeration"] = len(Enumeratios)

    # Enumeration_Literal
    Enumeration_Literals = root.findall(".//ownedLiteral")

    if len(Enumeration_Literals) > 0:
        count["Enumeration_Literal"] = len(Enumeration_Literals)

    # -----------------------------
    # -> Relationships:

    # Generalization
    Generalizations = root.findall(".//generalization")

    if len(Generalizations) > 0:
        count["Generalization"] = len(Generalizations)

    # Realization
    Realizations = root.findall(".//interfaceRealization")

    if len(Realizations) > 0:
        count["Realization"] = len(Realizations)

    # Dependency
    Dependencies = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Dependency']")

    if len(Dependencies) > 0:
        count["Dependency"] = len(Dependencies)

    # Usage
    Usages = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Usage']")

    if len(Usages) > 0:
        count["Usage"] = len(Usages)

    # Import
    Imports = root.findall(".//elementImport")

    if len(Imports) > 0:
        count["Import"] = len(Imports)

    # Template Binding
    Template_Bindings = root.findall(".//templateBinding")

    if len(Template_Bindings) > 0:
        count["Template_Binding"] = len(Template_Bindings)

    # Association
    Associations = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Association']")

    if len(Associations) > 0:
        count["Association"] = len(Associations)

    # Composition
    Compositions = root.findall(".//ownedEnd[@aggregation='composite']")

    if len(Compositions) > 0:
        count["Composition"] = len(Compositions)
        count["Association"] = count["Association"] - count["Composition"]

    # Aggregation
    Aggregations = root.findall(".//ownedEnd[@aggregation='shared']")

    if len(Aggregations) > 0:
        count["Aggregation"] = len(Aggregations)
        count["Association"] = count["Association"] - count["Aggregation"]

    # Inner relation
    Inner_relations = root.findall(".//nestedClassifier")

    if len(Inner_relations) > 0:
        count["Inner_relation"] = len(Inner_relations)

    # Association Class
    Association_Classes = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:AssociationClass']")

    if len(Association_Classes) > 0:
        count["Association_Class"] = len(Association_Classes)

    return count


# Função para obter o autor do diagrama
def get_author(root):

    author = root.findall(".//details[@key='author']")

    # Caso exista um autor
    if len(author) > 0:
        return author[0].attrib['value']
    else:
        return None


# Função para guardar os resultados no ficheiro CSV
def save_results_to_csv(filename, file_id, count, author):
    
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([file_id] + list(count.values()) + [author])


# Função verificar diagramas híbridos
def hybrid_diagram(root):

    types_of_diagrams = {
        "Component_Diagram": False,
        "Deployment_Diagram": False,
        "Object_Diagram": False,
        "Use_Case_Diagram": False
    }

    # Verificar se é um Component Diagram
    Component = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Component']")

    if len(Component) > 0:
        types_of_diagrams["Component_Diagram"] = True

    # Verificar se é um Deployment Diagram
    Node = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Node']")

    Device = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Device']")

    Execution_Environment = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:ExecutionEnvironment']")

    Artifact = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Artifact']")

    if len(Node) > 0 or len(Device) > 0 or len(Execution_Environment) > 0 or len(Artifact) > 0:
        types_of_diagrams["Deployment_Diagram"] = True

    # Verificar se é um Object Diagram
    Instance = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:InstanceSpecification']")

    if len(Instance) > 0:
        types_of_diagrams["Object_Diagram"] = True

    # Verificar se é um Use Case Diagram
    Actor = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Actor']")

    Use_Case = root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:UseCase']")

    if len(Actor) > 0 or len(Use_Case) > 0:
        types_of_diagrams["Use_Case_Diagram"] = True

    return types_of_diagrams


# Função para guardar os resultados no ficheiro CSV 2
def save_results_to_csv2(filename, file_id, types_of_diagrams):

    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([file_id] + list(types_of_diagrams.values()))


# Main
def main():

    FOLDER = "../Scraper/Google Colab/Dataset/"
    progress = 0

    # Assegurar o uso correto
    if len(sys.argv) != 3:
        sys.exit("Usage: python main.py INITIAL_FILE FINAL_FILE")

    INITIAL_FILE = int(sys.argv[1])
    FINAL_FILE = int(sys.argv[2])

    # Verificar limites
    if INITIAL_FILE < 1:
        sys.exit("The initial file must be greater than 0!")

    # Verificar se a posição do ficheiro final é menor que a posição do ficheiro inicial
    if FINAL_FILE < INITIAL_FILE:
        sys.exit("The final file must be greater or equal than the initial file!")

    # Range de ficheiros
    files = read_files_ids(INITIAL_FILE-1, FINAL_FILE)

    # Avaliar cada ficheiro
    for file in files:

        # Ler o ficheiro XMI
        FILE = file
        root = read_xmi_file(FOLDER + FILE)

        # Obter o número de cada tipo de elemento no diagrama
        count = check_number_of_different_element_types(root)

        # Obter o autor do ficheiro
        author = get_author(root)

        # Guardar os resultados no ficheiro CSV
        save_results_to_csv("results.csv", FILE, count, author)

        # Verificar se é um diagrama híbrido
        types_of_diagrams = hybrid_diagram(root)

        # Guardar os resultados no ficheiro CSV 2
        save_results_to_csv2("results2.csv", FILE, types_of_diagrams)

        # Mostrar o progresso
        progress += 1
        print("Progress: " + str(progress) + "/" + str(len(files)))


if __name__ == "__main__":
    main()