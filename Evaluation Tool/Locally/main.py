import utils
import sys

# Main
def main():

    FOLDER = "../../Web Scraper/Google Colab/Dataset/"
    CSV_FILE = "results"
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
    files = utils.read_files_ids(INITIAL_FILE-1, FINAL_FILE)
    
    # Avaliar cada ficheiro
    for file in files:

        # Ler o ficheiro XMI
        FILE = file
        root = utils.read_xmi_file(FOLDER + FILE)

        # PoN - Visual Expressiveness
        elements_without_color = utils.find_elements_without_color(root)
        #print(elements_without_color)

        # PoN - Dual Coding
        relationships_without_description = utils.find_relationships_without_description(root)
        #print(relationships_without_description)

        # PoN - Graphic Economy
        element_types = utils.check_number_of_different_element_types(root)
        #print(element_types)

        # PoN - Perceptual Discriminability
        perceptual_discriminability = utils.check_for_perceptual_discriminability(root)
        #print(perceptual_discriminability)

        # Diagram Size
        diagram_size = utils.check_for_diagram_size(root)
        #print(diagram_size)

        # Diagram Flaw - Overlapping Elements
        overlapping_elements = utils.check_for_overlapping_elements(root)
        #print(overlapping_elements)

        # Diagram Flaw - Intersections
        intersections = utils.check_for_intersections(root)
        #print(intersections)

        # Diagram Flaw - Bends in Lines
        bends_in_lines = utils.check_for_bends_in_lines(root)
        #print(bends_in_lines)

        # Diagram Flaw - Close Lines
        close_merged_or_aligned_lines = utils.check_for_close_merged_or_aligned_lines(root)
        #print(close_merged_or_aligned_lines)

        # Guardar os resultados num ficheiro CSV
        utils.save_results_to_csv(CSV_FILE + ".csv", FILE, elements_without_color, relationships_without_description, element_types, perceptual_discriminability, diagram_size, overlapping_elements, intersections, bends_in_lines, close_merged_or_aligned_lines)

        # Mostrar o progresso
        progress += 1
        print("Progress: " + str(progress) + "/" + str(len(files)))


if __name__ == "__main__":
    main()