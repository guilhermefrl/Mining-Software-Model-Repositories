import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

entities = ['Package', 'Class', 'Interface', 'DataType', 'Enumeration']
relationships = ['Generalization', 'Realization', 'Dependency', 'Usage', 'Import', 'Template_Binding',
                 'Association', 'Composition', 'Aggregation', 'Inner_relation', 'Association_Class']
elements = ['Package', 'Class', 'Interface', 'DataType', 'Attribute', 'Operation', 'Enumeration',
            'Enumeration_Literal', 'Generalization', 'Realization', 'Dependency', 'Usage', 'Import',
            'Template_Binding', 'Association', 'Composition', 'Aggregation', 'Inner_relation', 'Association_Class']

# Função para guardar o número de autores distintos e não identificados
def count_authors(file_path):
    authors = set()
    non_identified_authors = 0

    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            author = row['author']
            if author == '':
                non_identified_authors += 1
            else:
                authors.add(author)

    with open('author_count.txt', 'w') as output_file:
        output_file.write(f"Distinct authors: {len(authors)}\n")
        output_file.write(f"Non-identified authors: {non_identified_authors}\n")


# Função para contar o número de diagramas com n entidades
def count_diagrams_with_n_entities(csv_file):
    diagrams_with_n_entities = {}

    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            entity_count = sum(int(row[entity]) for entity in entities)
            if entity_count in diagrams_with_n_entities:
                diagrams_with_n_entities[entity_count] += 1
            else:
                diagrams_with_n_entities[entity_count] = 1

    return diagrams_with_n_entities


# Função que cria um histograma do número de diagramas com n entidades
def create_histogram_number_of_diagrams_with_n_entities(data):
    counts = list(data.values())
    bins = list(data.keys())

    most_used_entities = bins[counts.index(max(counts))]
    
    plt.bar(most_used_entities, data[most_used_entities], color='red', label=f'Number of most used entities', zorder=3)
    plt.bar(bins, counts, zorder=2)
    plt.grid(True, alpha=0.6, zorder=1)
    plt.xlabel('Number of entities')
    plt.ylabel('Number of diagrams')
    plt.legend()
    plt.axis([0, 90, 0, 16000])
    plt.savefig('histogram_number_of_diagrams_with_n_entities.png')
    plt.close()


# Função para o KDE do número de diagramas com n entidades
def create_kde_number_of_diagrams_with_n_entities(data):
    entities = []
    for key, value in data.items():
        entities.extend([key] * value)

    median_entities = np.median(entities)
    mean_entities = np.mean(entities)

    plt.figure(figsize=(12, 6))
    plt.grid(True, alpha=0.6, zorder=1)
    plt.axvline(median_entities, color='orange', linestyle='--', label=f'Median number of entities: {median_entities:.2f}', zorder=2)
    plt.axvline(mean_entities, color='green', linestyle='--', label=f'Average number of entities: {mean_entities:.2f}', zorder=2)
    sns.kdeplot(entities, bw_method=0.5, fill=True, zorder=3)
    plt.xlabel("Number of entities")
    plt.ylabel("Density")
    plt.legend()
    plt.savefig('kde_number_of_diagrams_with_n_entities.png')
    plt.close()


# Função para contar o número de diagramas com n relações
def count_diagrams_with_n_relationships(csv_file):
    diagrams_with_n_relationships = {}

    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            relationship_count = sum(int(row[relationship]) for relationship in relationships)
            if relationship_count in diagrams_with_n_relationships:
                diagrams_with_n_relationships[relationship_count] += 1
            else:
                diagrams_with_n_relationships[relationship_count] = 1

    return diagrams_with_n_relationships


# Função que cria um histograma do número de diagramas com n relações
def create_histogram_number_of_diagrams_with_n_relationships(data):
    counts = list(data.values())
    bins = list(data.keys())
    most_used_entities = bins[counts.index(max(counts))]
    
    plt.bar(most_used_entities, data[most_used_entities], color='red', label=f'Number of most used relationships', zorder=3)
    plt.bar(bins, counts, zorder=2)
    plt.grid(True, alpha=0.6, zorder=1)
    plt.xlabel('Number of relationships')
    plt.ylabel('Number of diagrams')
    plt.axis([0, 90, 0, 12000])
    plt.legend()
    plt.savefig('histogram_number_of_diagrams_with_n_relationships.png')
    plt.close()


# Função para o KDE do número de diagramas com n relações
def create_kde_number_of_diagrams_with_n_relationships(data):
    relationships = []
    for key, value in data.items():
        relationships.extend([key] * value)

    median_relationships = np.median(relationships)
    mean_relationships = np.mean(relationships)

    plt.figure(figsize=(12, 6))
    plt.grid(True, alpha=0.6, zorder=1)
    plt.axvline(median_relationships, color='orange', linestyle='--', label=f'Median number of relationships: {median_relationships:.2f}', zorder=2)
    plt.axvline(mean_relationships, color='green', linestyle='--', label=f'Average number of relationships: {mean_relationships:.2f}', zorder=2)
    sns.kdeplot(relationships, bw_method=0.5, fill=True, zorder=3)
    plt.xlabel("Number of relationships")
    plt.ylabel("Density")
    plt.legend()
    plt.savefig('kde_number_of_diagrams_with_n_relationships.png')
    plt.close()


# Função para contar o número de cada elemento UML
def count_elements(csv_file):
    element_counts = {element: 0 for element in elements}

    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for element in elements:
                element_counts[element] += int(row[element])

    return element_counts


# Função para guardar o número de cada elemento UML e a percentagem correspondente num ficheiro de texto
def save_element_counts(element_counts):
    total_elements = sum(element_counts.values())

    sorted_counts = sorted(element_counts.items(), key=lambda x: x[1], reverse=True)

    with open('element_counts.txt', 'w') as file:
        for element, count in sorted_counts:
            percentage = (count / total_elements) * 100
            formatted_line = f"{element}: {count} ({percentage:.2f}%)"
            file.write(formatted_line + '\n')


# Função auxiliar para formatar o número de elementos UML
def format_count(value):
    if value >= 1e6:
        return '{:.1f}M'.format(value / 1e6)
    elif value >= 1e3:
        return '{:.0f}K'.format(value / 1e3)
    else:
        return str(value)


# Função que cria um gráfico da distribuição dos elementos UML
def create_element_distribution_plot(data):
    counts = list(data.values())
    elements = ['Package', 'Class', 'Interface', 'DataType', 'Attribute', 'Operation', 'Enumeration',
                'Enumeration Literal', 'Generalization', 'Realization', 'Dependency', 'Usage', 'Import',
                'Template Binding', 'Association', 'Composition', 'Aggregation', 'Inner relation', 'Association Class']
    counts, elements = zip(*sorted(zip(counts, elements), reverse=True))
    plt.figure(figsize=(10, 6))
    plt.bar(elements, counts, zorder=2)
    plt.grid(True, alpha=0.6, axis='y', zorder=1)
    plt.xlabel('UML elements')
    plt.ylabel('Number of elements')
    plt.axis([-1, 19, 0, 2500000])
    plt.xticks(rotation=60, ha='right')
    plt.subplots_adjust(bottom=0.3)
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    for i, count in enumerate(counts):
        formatted_count = format_count(count)
        plt.text(i, count, formatted_count, ha='center', va='bottom')
    plt.savefig('element_distribution.png')
    plt.close()


# Função analisar o número de diagranas híbridos
def analyze_hybrid_diagrams(csv_file):
    diagram_counts = {}
    total_files = 0

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_files += 1
            diagram_types = []

            for diagram_type, has_diagram in row.items():
                if has_diagram.lower() == 'true':
                    diagram_types.append(diagram_type)

            diagram_combination = ', '.join(sorted(diagram_types))
            if diagram_combination in diagram_counts:
                diagram_counts[diagram_combination] += 1
            else:
                diagram_counts[diagram_combination] = 1

    sorted_counts = sorted(diagram_counts.items(), key=lambda x: x[1], reverse=True)

    results = []
    for diagram_combination, count in sorted_counts:
        percentage = (count / total_files) * 100
        results.append(f"{diagram_combination}: {count} {percentage:.2f}%")

    return results


# Função para guardar a análise dos diagramas híbridos num ficheiro de texto
def save_hybrid_diagrams_analysis(results):
    with open('hybrid_diagrams_analysis.txt', 'w') as output_file:
        for result in results:
            output_file.write(result + '\n')


# Main
def main():
    csv_file_path = 'results.csv'
    csv_file_path2 = 'results2.csv'

    # Contar o número de autores distintos e não identificados
    count_authors(csv_file_path)
    print("Progress: 1/11")

    # Contar o número de diagramas com n entidades
    diagrams_with_n_entities = count_diagrams_with_n_entities(csv_file_path)
    print("Progress: 2/11")

    # Criar um histograma do número de diagramas com n entidades
    create_histogram_number_of_diagrams_with_n_entities(diagrams_with_n_entities)
    print("Progress: 3/11")

    # Criar um KDE do número de diagramas com n entidades
    create_kde_number_of_diagrams_with_n_entities(diagrams_with_n_entities)
    print("Progress: 4/11")

    # Contar o número de diagramas com n relações
    diagrams_with_n_relationships = count_diagrams_with_n_relationships(csv_file_path)
    print("Progress: 5/11")

    # Criar um histograma do número de diagramas com n relações
    create_histogram_number_of_diagrams_with_n_relationships(diagrams_with_n_relationships)
    print("Progress: 6/11")

    # Criar um KDE do número de diagramas com n relações
    create_kde_number_of_diagrams_with_n_relationships(diagrams_with_n_relationships)
    print("Progress: 7/11")

    # Contar o número de cada elemento UML
    element_counts = count_elements(csv_file_path)
    print("Progress: 8/11")

    # Guardar num ficheiro de texto o número de cada elemento UML e a percentagem correspondente
    save_element_counts(element_counts)
    print("Progress: 9/11")

    # Fazer um gráfico da distribuição dos elementos UML
    create_element_distribution_plot(element_counts)
    print("Progress: 10/11")

    # Análise de diagramas híbridos
    analysis = analyze_hybrid_diagrams(csv_file_path2)
    save_hybrid_diagrams_analysis(analysis)
    print("Progress: 11/11")


if __name__ == '__main__':
    main()