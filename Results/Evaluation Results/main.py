import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Função para contar o número total que cada princípio não é respeitado
def count_the_number_of_times_each_principle_is_not_respected(csv_file):

    principle_counts = {
        'elements_without_color': 0,
        'associations_without_description': 0,
        'element_types': 0,
        'perceptual_discriminability': 0,
        'diagram_size': 0,
        'overlapping_elements': 0,
        'intersections': 0,
        'bends_in_lines': 0,
        'close_merged_or_aligned_lines': 0
    }

    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            # Ler os campos do CSV
            elements_without_color = eval(row['elements_without_color'])[1]
            associations_without_description = eval(row['associations_without_description'])[1]
            perceptual_discriminability = eval(row['perceptual_discriminability'])[1]
            overlapping_elements = eval(row['overlapping_elements'])[1]
            intersections = eval(row['intersections'])[1]
            bends_in_lines = eval(row['bends_in_lines'])[1]
            close_merged_or_aligned_lines = eval(row['close_merged_or_aligned_lines'])[1]

            principle_counts['elements_without_color'] += elements_without_color
            principle_counts['associations_without_description'] += associations_without_description
            
            if eval(row['element_types'])[0]:
                principle_counts['element_types'] += 1
            
            principle_counts['perceptual_discriminability'] += perceptual_discriminability

            if not eval(row['diagram_size'])[0]:
                principle_counts['diagram_size'] += 1

            principle_counts['overlapping_elements'] += overlapping_elements
            principle_counts['intersections'] += intersections
            principle_counts['bends_in_lines'] += bends_in_lines
            principle_counts['close_merged_or_aligned_lines'] += close_merged_or_aligned_lines

    return principle_counts


# Função auxiliar para formatar o número de elementos UML
def format_count(value):
    if value >= 1e6:
        return '{:.1f}M'.format(value / 1e6)
    elif value >= 1e3:
        return '{:.0f}K'.format(value / 1e3)
    else:
        return str(value)


# Função que cria um gráfico da distribuição do número total que cada princípio não é respeitado
def create_graph_of_the_distribution_of_the_total_number_of_times_each_principle_is_not_respected(data):
    principles = ["Visual Expressiveness", "Dual Coding", "Graphic Economy", "Perceptual Discriminability", "Diagram Size", "Overlapping Elements", "Intersections", "Bends in Lines", "Close Lines"]
    counts = list(data.values())
    principles, counts = zip(*sorted(zip(principles, counts), key=lambda x: x[1], reverse=True))
    plt.figure(figsize=(10, 6))
    plt.bar(principles, counts, zorder=2)
    plt.grid(True, alpha=0.6, axis='y', zorder=1)
    plt.xlabel('Principles')
    plt.ylabel('Number of occurrences')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    for i, count in enumerate(counts):
        formatted_count = format_count(count)
        plt.text(i, count, formatted_count, ha='center', va='bottom')
    plt.savefig('total_count_of_each_principles_not_respected.png')
    plt.close()


# Função para contar o número de diagramas em que cada princípio não é respeitados pelo menos uma vez
def count_the_number_of_diagrams_in_which_each_principle_is_not_respected(csv_file):
    principle_counts = {
        'elements_without_color': 0,
        'associations_without_description': 0,
        'element_types': 0,
        'perceptual_discriminability': 0,
        'diagram_size': 0,
        'overlapping_elements': 0,
        'intersections': 0,
        'bends_in_lines': 0,
        'close_merged_or_aligned_lines': 0
    }

    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            if eval(row['elements_without_color'])[0]:
                principle_counts['elements_without_color'] += 1

            if eval(row['associations_without_description'])[0]:
                principle_counts['associations_without_description'] += 1
            
            if eval(row['element_types'])[0]:
                principle_counts['element_types'] += 1

            if not eval(row['perceptual_discriminability'])[0]:
                principle_counts['perceptual_discriminability'] += 1

            if not eval(row['diagram_size'])[0]:
                principle_counts['diagram_size'] += 1

            if eval(row['overlapping_elements'])[0]:
                principle_counts['overlapping_elements'] += 1

            if eval(row['intersections'])[0]:
                principle_counts['intersections'] += 1

            if eval(row['bends_in_lines'])[0]:
                principle_counts['bends_in_lines'] += 1

            if eval(row['close_merged_or_aligned_lines'])[0]:
                principle_counts['close_merged_or_aligned_lines'] += 1

    return principle_counts


# Função que cria um gráfico da distribuição do número diagramas em que cada princípio não é respeitado pelo menos uma vez
def create_graph_of_the_distribution_of_the_number_of_diagrams_in_which_each_principle_is_not_respected_at_least_once(data):
    principles = ["Visual Expressiveness", "Dual Coding", "Graphic Economy", "Perceptual Discriminability", "Diagram Size", "Overlapping Elements", "Intersections", "Bends in Lines", "Close Lines"]
    counts = list(data.values())
    principles, counts = zip(*sorted(zip(principles, counts), key=lambda x: x[1], reverse=True))
    plt.figure(figsize=(10, 6))
    plt.bar(principles, counts, zorder=2)
    plt.grid(True, alpha=0.6, axis='y', zorder=1)
    plt.xlabel('Principles')
    plt.ylabel('Number of diagrams')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    for i, count in enumerate(counts):
        formatted_count = format_count(count)
        plt.text(i, count, formatted_count, ha='center', va='bottom')
    plt.savefig('principles_not_respected_at_least_once.png')
    plt.close()


# Função que conta o número de diagramas com n ocorrências do princípio X
def count_diagrams_with_n_occurrences(csv_file, principle_name):
    occurrences_count = {}

    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            occurrences = eval(row[principle_name])[1]
            occurrences_count[occurrences] = occurrences_count.get(occurrences, 0) + 1

    return occurrences_count


# Função que cria um histograma do número de diagramas com n ocorrências do princípio X
def create_histogram_of_the_number_of_diagrams_with_n_occurrences(occurrences_count, principle_name, x_min, x_max, y_min, y_max, x_step):
    occurrences = list(occurrences_count.keys())
    counts = list(occurrences_count.values())
    most_used_occurrences = occurrences[counts.index(max(counts))]
    plt.figure(figsize=(10, 6))
    plt.bar(most_used_occurrences, occurrences_count[most_used_occurrences], color='red', label=f'Most common number of occurrences', zorder=3)
    plt.bar(occurrences, counts, zorder=2)
    plt.grid(True, alpha=0.6, zorder=1)
    plt.xlabel('Number of occurrences')
    plt.ylabel('Number of diagrams')
    plt.axis([x_min, x_max, y_min, y_max])
    plt.xticks(range(x_min, x_max + 1, x_step))
    plt.legend()
    plt.savefig('histogram_number_of_diagrams_with_n_occurrences_of_' + principle_name + '.png')
    plt.close()


# Função que cria a linha KDE do número de diagramas com n ocorrências do princípio X
def create_kde_line_of_the_number_of_diagrams_with_n_occurrences(occurrences_count, principle_name):
    occurrences = []
    for key, value in occurrences_count.items():
        if key != 0:
            occurrences.extend([key] * value)

    median_occurrences = np.median(occurrences)
    mean_occurrences = np.mean(occurrences)

    plt.figure(figsize=(10, 6))
    plt.grid(True, alpha=0.6, zorder=1)
    plt.axvline(median_occurrences, color='orange', linestyle='--', label=f'Median number of occurrences: {median_occurrences:.2f}', zorder=2)
    plt.axvline(mean_occurrences, color='green', linestyle='--', label=f'Average number of occurrences: {mean_occurrences:.2f}', zorder=2)
    sns.kdeplot(occurrences, bw_method=0.5, fill=True, zorder=3)
    plt.xlabel('Number of occurrences')
    plt.ylabel('Density')
    plt.legend()
    plt.savefig('kde_number_of_diagrams_with_n_occurrences_of_' + principle_name + '.png')
    plt.close()


# Função para criar um box plot do número de diagramas com n ocorrências do princípio X
def create_box_plot_of_the_number_of_diagrams_with_n_occurrences(occurrences_count, principle_name):
    occurrences = []
    for key, value in occurrences_count.items():
        if key != 0:
            occurrences.extend([key] * value)
    plt.figure(figsize=(10, 6))
    plt.grid(True, alpha=0.6, zorder=1)
    plt.boxplot(occurrences, zorder=2)
    plt.ylabel('Number of occurrences')
    plt.xticks([x for x in plt.xticks()[0] if x != 1])

    min_val = np.min(occurrences)
    q1_val = np.percentile(occurrences, 25)
    median_val = np.median(occurrences)
    q3_val = np.percentile(occurrences, 75)
    iqr = q3_val - q1_val
    upper_whisker = q3_val + 1.5 * iqr
    legend_text = f"Minimum: {min_val}\nQ1: {q1_val}\nMedian: {median_val}\nQ3: {q3_val}\nMaximum: {upper_whisker}"
    plt.legend([legend_text], loc='upper right', handlelength=0, handletextpad=0)

    plt.savefig('boxplot_number_of_diagrams_with_n_occurrences_of_' + principle_name + '.png')
    plt.close()


# Função para criar um box plot do número de diagramas com n ocorrências do princípio X, sem outliers
def create_box_plot_of_the_number_of_diagrams_with_n_occurrences_without_outliers(occurrences_count, principle_name):
    occurrences = []
    for key, value in occurrences_count.items():
        if key != 0:
            occurrences.extend([key] * value)
    plt.figure(figsize=(10, 6))
    plt.grid(True, alpha=0.6, zorder=1)
    plt.boxplot(occurrences, showfliers=False, zorder=2)
    plt.ylabel('Number of occurrences')
    plt.xticks([x for x in plt.xticks()[0] if x != 1])

    min_val = np.min(occurrences)
    q1_val = np.percentile(occurrences, 25)
    median_val = np.median(occurrences)
    q3_val = np.percentile(occurrences, 75)
    iqr = q3_val - q1_val
    upper_whisker = q3_val + 1.5 * iqr
    legend_text = f"Minimum: {min_val}\nQ1: {q1_val}\nMedian: {median_val}\nQ3: {q3_val}\nMaximum: {upper_whisker}"
    plt.legend([legend_text], loc='upper right', handlelength=0, handletextpad=0)

    plt.savefig('boxplot_number_of_diagrams_with_n_occurrences_of_' + principle_name + '_without_outliers.png')
    plt.close()


# Função que cria um pie chart com a percentagem de diagramas que respeitam e não respeitam o princípio X
def create_pie_chart_percentage_of_diagrams_that_respect_and_do_not_respect_the_x_principle(data, total_of_diagrams, principle_name):
    respect_count = total_of_diagrams - data
    not_respect_count = data
    labels = ['Respect', 'Do not respect']
    sizes = [respect_count, not_respect_count]
    colors = ['#47B39C', '#EC6B56']

    plt.figure(figsize=(8, 8))
    wedges, _, autotexts = plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)

    for i, count in enumerate(sizes):
        percentage = count / total_of_diagrams * 100
        autotexts[i].set_text(f"{percentage:.1f}% ({format_count(count)})")

    plt.savefig('pie_chart_percentage_of_diagrams_that_respect_and_do_not_respect_the_' + principle_name + '.png')
    plt.close()


# Função para calcular a média de ocorrências de cada princípio
def calculate_the_average_number_of_occurrences_of_each_principle(csv_file):
    def round_to_one_decimal(number):
        return round(number, 1)
    
    principle_counts = count_the_number_of_times_each_principle_is_not_respected(csv_file)

    with open(csv_file, newline='', encoding='utf-8') as file:
        total_samples = sum(1 for line in file) - 1

    average_occurrences = {principle: round_to_one_decimal(count / total_samples) for principle, count in principle_counts.items()}

    return average_occurrences


# Função para criar um gráfico com a média de ocorrências de cada princípio
def create_graph_with_the_average_number_of_occurrences_of_each_principle(data):
    principles = ["Visual Expressiveness", "Dual Coding", "Graphic Economy", "Perceptual Discriminability", "Diagram Size", "Overlapping Elements", "Intersections", "Bends in Lines", "Close Lines"]
    counts = list(data.values())
    principles, counts = zip(*sorted(zip(principles, counts), key=lambda x: x[1], reverse=True))
    plt.figure(figsize=(10, 6))
    plt.bar(principles, counts, zorder=2)
    plt.grid(True, alpha=0.6, axis='y', zorder=1)
    plt.xlabel('Principles')
    plt.ylabel('Average number of occurrences')
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.3)
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    for i, count in enumerate(counts):
        formatted_count = format_count(count)
        plt.text(i, count, formatted_count, ha='center', va='bottom')
    plt.savefig('average_number_of_occurrences_of_each_principles_not_respected.png')
    plt.close()


# Main
def main():
    csv_file_path = 'results.csv'
    total_of_diagrams = 103103
    
    # Contar o número total que cada princípio não é respeitado
    total_count_of_each_principles_not_respected = count_the_number_of_times_each_principle_is_not_respected(csv_file_path)
    print("Progress: 1/50")

    # Criar um histograma do número total que cada princípio não é respeitado
    create_graph_of_the_distribution_of_the_total_number_of_times_each_principle_is_not_respected(total_count_of_each_principles_not_respected)
    print("Progress: 2/50")


    # Contar o número de diagramas em que cada princípio não é respeitado pelo menos uma vez
    principles_not_respected_at_least_once = count_the_number_of_diagrams_in_which_each_principle_is_not_respected(csv_file_path)
    print("Progress: 3/50")

    # Fazer um gráfico da distribuição em que cada princípio não é respeitado pelo menos uma vez
    create_graph_of_the_distribution_of_the_number_of_diagrams_in_which_each_principle_is_not_respected_at_least_once(principles_not_respected_at_least_once)
    print("Progress: 4/50")

    
    # Contar o número de diagramas com n ocorrências do princípio Visual Expressiveness
    number_of_diagrams_with_n_occurrences_of_the_Visual_Expressiveness_principle = count_diagrams_with_n_occurrences(csv_file_path, 'elements_without_color')
    print("Progress: 5/50")

    # Criar um histograma do número de diagramas com n ocorrências do princípio Visual Expressiveness
    create_histogram_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Visual_Expressiveness_principle, 'Visual Expressiveness', 1, 130, 0, 6000, 5)
    print("Progress: 6/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Visual Expressiveness
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Visual_Expressiveness_principle, 'Visual Expressiveness')
    print("Progress: 7/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Visual Expressiveness, sem outliers
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences_without_outliers(number_of_diagrams_with_n_occurrences_of_the_Visual_Expressiveness_principle, 'Visual Expressiveness')
    print("Progress: 8/50")

    # Contar o número de diagramas com n ocorrências do princípio Dual Coding
    number_of_diagrams_with_n_occurrences_of_the_Dual_Coding_principle = count_diagrams_with_n_occurrences(csv_file_path, 'associations_without_description')
    print("Progress: 9/50")

    # Criar um histograma do número de diagramas com n ocorrências do princípio Dual Coding
    create_histogram_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Dual_Coding_principle, 'Dual Coding', 1, 35, 0, 12000, 1)
    print("Progress: 10/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Dual Coding
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Dual_Coding_principle, 'Dual Coding')
    print("Progress: 11/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Dual Coding, sem outliers
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences_without_outliers(number_of_diagrams_with_n_occurrences_of_the_Dual_Coding_principle, 'Dual Coding')
    print("Progress: 12/50")

    # Contar o número de diagramas com n ocorrências do princípio Perceptual Discriminability
    number_of_diagrams_with_n_occurrences_of_the_Perceptual_Discriminability_principle = count_diagrams_with_n_occurrences(csv_file_path, 'perceptual_discriminability')
    print("Progress: 13/50")

    # Criar um histograma do número de diagramas com n ocorrências do princípio Perceptual Discriminability
    create_histogram_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Perceptual_Discriminability_principle, 'Perceptual Discriminability', 1, 75, 0, 2000, 3)
    print("Progress: 14/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Perceptual Discriminability
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Perceptual_Discriminability_principle, 'Perceptual Discriminability')
    print("Progress: 15/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Perceptual Discriminability, sem outliers
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences_without_outliers(number_of_diagrams_with_n_occurrences_of_the_Perceptual_Discriminability_principle, 'Perceptual Discriminability')
    print("Progress: 16/50")

    # Contar o número de diagramas com n ocorrências do princípio Overlapping Elements
    number_of_diagrams_with_n_occurrences_of_the_Overlapping_Elements_principle = count_diagrams_with_n_occurrences(csv_file_path, 'overlapping_elements')
    print("Progress: 17/50")

    # Criar um histograma do número de diagramas com n ocorrências do princípio Overlapping Elements
    create_histogram_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Overlapping_Elements_principle, 'Overlapping Elements', 1, 115, 0, 6000, 5)
    print("Progress: 18/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Overlapping Elements
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Overlapping_Elements_principle, 'Overlapping Elements')
    print("Progress: 19/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Overlapping Elements, sem outliers
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences_without_outliers(number_of_diagrams_with_n_occurrences_of_the_Overlapping_Elements_principle, 'Overlapping Elements')
    print("Progress: 20/50")

    # Contar o número de diagramas com n ocorrências do princípio Intersections
    number_of_diagrams_with_n_occurrences_of_the_Intersections_principle = count_diagrams_with_n_occurrences(csv_file_path, 'intersections')
    print("Progress: 21/50")

    # Criar um histograma do número de diagramas com n ocorrências do princípio Intersections
    create_histogram_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Intersections_principle, 'Intersections', 1, 230, 0, 5000, 10)
    print("Progress: 22/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Intersections
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Intersections_principle, 'Intersections')
    print("Progress: 23/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Intersections, sem outliers
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences_without_outliers(number_of_diagrams_with_n_occurrences_of_the_Intersections_principle, 'Intersections')
    print("Progress: 24/50")


    # Contar o número de diagramas com n ocorrências do princípio Bends in Lines
    number_of_diagrams_with_n_occurrences_of_the_Bends_in_Lines_principle = count_diagrams_with_n_occurrences(csv_file_path, 'bends_in_lines')
    print("Progress: 25/50")

    # Criar um histograma do número de diagramas com n ocorrências do princípio Bends in Lines
    create_histogram_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Bends_in_Lines_principle, 'Bends in Lines', 1, 50, 0, 14000, 2)
    print("Progress: 26/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Bends in Lines
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Bends_in_Lines_principle, 'Bends in Lines')
    print("Progress: 27/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Bends in Lines, sem outliers
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences_without_outliers(number_of_diagrams_with_n_occurrences_of_the_Bends_in_Lines_principle, 'Bends in Lines')
    print("Progress: 28/50")

    # Contar o número de diagramas com n ocorrências do princípio Close Lines
    number_of_diagrams_with_n_occurrences_of_the_Close_Lines_principle = count_diagrams_with_n_occurrences(csv_file_path, 'close_merged_or_aligned_lines')
    print("Progress: 29/50")

    # Criar um histograma do número de diagramas com n ocorrências do princípio Close Lines
    create_histogram_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Close_Lines_principle, 'Close Lines', 1, 350, 0, 6000, 15)
    print("Progress: 30/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Close Lines
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Close_Lines_principle, 'Close Lines')
    print("Progress: 31/50")

    # Criar um box plot do número de diagramas com n ocorrências do princípio Close Lines, sem outliers
    create_box_plot_of_the_number_of_diagrams_with_n_occurrences_without_outliers(number_of_diagrams_with_n_occurrences_of_the_Close_Lines_principle, 'Close Lines')
    print("Progress: 32/50")


    # Criar a linha KDE do número de diagramas com n ocorrências do princípio Visual Expressiveness
    create_kde_line_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Visual_Expressiveness_principle, 'Visual Expressiveness')
    print("Progress: 33/50")

    # Criar a linha KDE do número de diagramas com n ocorrências do princípio Dual Coding
    create_kde_line_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Dual_Coding_principle, 'Dual Coding')
    print("Progress: 34/50")

    # Criar a linha KDE do número de diagramas com n ocorrências do princípio Perceptual Discriminability
    create_kde_line_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Perceptual_Discriminability_principle, 'Perceptual Discriminability')
    print("Progress: 35/50")

    # Criar a linha KDE do número de diagramas com n ocorrências do princípio Overlapping Elements
    create_kde_line_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Overlapping_Elements_principle, 'Overlapping Elements')
    print("Progress: 36/50")

    # Criar a linha KDE do número de diagramas com n ocorrências do princípio Intersections
    create_kde_line_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Intersections_principle, 'Intersections')
    print("Progress: 37/50")

    # Criar a linha KDE do número de diagramas com n ocorrências do princípio Bends in Lines
    create_kde_line_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Bends_in_Lines_principle, 'Bends in Lines')
    print("Progress: 38/50")

    # Criar a linha KDE do número de diagramas com n ocorrências do princípio Close Lines
    create_kde_line_of_the_number_of_diagrams_with_n_occurrences(number_of_diagrams_with_n_occurrences_of_the_Close_Lines_principle, 'Close Lines')
    print("Progress: 39/50")


    # Criar um pie chart com a percentagem de diagramas que respeitam e não respeitam o princípio Visual Expressiveness
    create_pie_chart_percentage_of_diagrams_that_respect_and_do_not_respect_the_x_principle(int(principles_not_respected_at_least_once['elements_without_color']), total_of_diagrams, 'Visual Expressiveness')
    print("Progress: 40/50")

    # Criar um pie chart com a percentagem de diagramas que respeitam e não respeitam o princípio Dual Coding
    create_pie_chart_percentage_of_diagrams_that_respect_and_do_not_respect_the_x_principle(int(principles_not_respected_at_least_once['associations_without_description']), total_of_diagrams, 'Dual Coding')
    print("Progress: 41/50")

    # Criar um pie chart com a percentagem de diagramas que respeitam e não respeitam o princípio Graphic Economy
    create_pie_chart_percentage_of_diagrams_that_respect_and_do_not_respect_the_x_principle(int(principles_not_respected_at_least_once['element_types']), total_of_diagrams, 'Graphic Economy')
    print("Progress: 42/50")

    # Criar um pie chart com a percentagem de diagramas que respeitam e não respeitam o princípio Perceptual Discriminability
    create_pie_chart_percentage_of_diagrams_that_respect_and_do_not_respect_the_x_principle(int(principles_not_respected_at_least_once['perceptual_discriminability']), total_of_diagrams, 'Perceptual Discriminability')
    print("Progress: 43/50")

    # Criar um pie chart com a percentagem de diagramas que respeitam e não respeitam o princípio Diagram Size
    create_pie_chart_percentage_of_diagrams_that_respect_and_do_not_respect_the_x_principle(int(principles_not_respected_at_least_once['diagram_size']), total_of_diagrams, 'Diagram Size')
    print("Progress: 44/50")

    # Criar um pie chart com a percentagem de diagramas que respeitam e não respeitam o princípio Overlapping Elements
    create_pie_chart_percentage_of_diagrams_that_respect_and_do_not_respect_the_x_principle(int(principles_not_respected_at_least_once['overlapping_elements']), total_of_diagrams, 'Overlapping Elements')
    print("Progress: 45/50")

    # Criar um pie chart com a percentagem de diagramas que respeitam e não respeitam o princípio Intersections
    create_pie_chart_percentage_of_diagrams_that_respect_and_do_not_respect_the_x_principle(int(principles_not_respected_at_least_once['intersections']), total_of_diagrams, 'Intersections')
    print("Progress: 46/50")

    # Criar um pie chart com a percentagem de diagramas que respeitam e não respeitam o princípio Bends in Lines
    create_pie_chart_percentage_of_diagrams_that_respect_and_do_not_respect_the_x_principle(int(principles_not_respected_at_least_once['bends_in_lines']), total_of_diagrams, 'Bends in Lines')
    print("Progress: 47/50")

    # Criar um pie chart com a percentagem de diagramas que respeitam e não respeitam o princípio Close Lines
    create_pie_chart_percentage_of_diagrams_that_respect_and_do_not_respect_the_x_principle(int(principles_not_respected_at_least_once['close_merged_or_aligned_lines']), total_of_diagrams, 'Close Lines')
    print("Progress: 48/50")
    

    # Contar o número médio de ocorrências de cada princípio
    average_occurrences = calculate_the_average_number_of_occurrences_of_each_principle(csv_file_path)
    print("Progress: 49/50")

    # Criar um um gráfico com a média de ocorrências de cada princípio
    create_graph_with_the_average_number_of_occurrences_of_each_principle(average_occurrences)
    print("Progress: 50/50")


if __name__ == '__main__':
    main()