import csv
import xml.etree.ElementTree as ET
import math

ELEMENTS_TYPE = ["PackageWidget", "ClassWidget", "InterfaceWidget", "DataTypeWidget", "EnumerationWidget", "GeneralizationSegment", 
                 "InterfaceRealizationSegment", "DependencySegment", "UsageSegment", "ImportSegment", "TemplateBindingSegment", 
                 "AssociationSegment", "InnerElementSegment"]

ELEMENTS = ["PackageWidget", "ClassWidget", "InterfaceWidget", "DataTypeWidget", "EnumerationWidget"]


# Função para ler um ficheiro
def read_xmi_file(filename):

    tree = ET.parse(filename + ".xmi")
    root = tree.getroot()

    return root


# Função para encontrar os elementos que não usam cores (Visual Expressiveness)
def find_elements_without_color(root):

    elements_without_color = set()

    # Percorrer todos os elementos do diagrama
    for elem in root.findall(".//ownedDiagramElements"):

        # Verificar se o tipo de elemento pertence ao conjunto de elementos
        if elem.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] in ["com.genmymodel.graphic.uml:" + elem_type for elem_type in ELEMENTS_TYPE]:
            # Verificar se o elemento não tem o atributo cor
            if 'color' not in elem.attrib and 'modelElement' in elem.attrib:
                id = elem.attrib['modelElement']
                elements_without_color.add(id)
                
    return [len(elements_without_color) > 0, len(elements_without_color)]


# Função para encontrar relações sem decrição (Dual Coding)
def find_relationships_without_description(root):

    relationships_without_description = 0

    # Verificar as relações do tipo Dependency
    for dependency in root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Dependency']"):
        if 'name' not in dependency.attrib or dependency.attrib["name"] == "":
            relationships_without_description += 1

    # Verificar as relações do tipo Usage
    for usage in root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Usage']"):
        if 'name' not in usage.attrib or usage.attrib["name"] == "":
            relationships_without_description += 1

    # Verificar as relações do tipo Association / Composition / Aggregation
    for association in root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Association']"):
        owned_ends = association.findall("./ownedEnd")

        for owned_end in owned_ends:
            if 'name' not in owned_end.attrib or owned_end.attrib["name"] == "":
                relationships_without_description += 1
                break

    # Verificar as relações do tipo Association Class
    for association_class in root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:AssociationClass']"):
        owned_ends = association_class.findall("./ownedEnd")

        for owned_end in owned_ends:
            if 'name' not in owned_end.attrib or owned_end.attrib["name"] == "":
                relationships_without_description += 1
                break 

    return [relationships_without_description > 0, relationships_without_description]


# Função para verficar se o número de elementos diferentes ultrapassa 6 (Graphic Economy)
def check_number_of_different_element_types(root):
    
    element_types = set()

    # Percorrer todos os elementos do diagrama
    for elem in root.findall(".//ownedDiagramElements"):
        # Verificar se o tipo de elemento pertence ao conjunto de elementos
        if elem.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] in ["com.genmymodel.graphic.uml:" + elem_type for elem_type in ELEMENTS_TYPE]:
            # Adicionar o tipo de elemento ao conjunto
            element_types.add(elem.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'])

    return [len(element_types) > 6, len(element_types)]


# Função para verificar se os elementos são distinguíveis (Perceptual Discriminability)
def check_for_perceptual_discriminability(root):

    ELEMENT_TYPES_IN_DIAGRAM = set()

    # Extrair todos os elementos do diagrama
    diagram_elements = root.findall(".//*[@{http://www.w3.org/2001/XMLSchema-instance}type]")

    # Criar um dicionário para armazenar as informações sobre cada tipo de elemento
    type_dict = {elem_type: {"ids": [], "names": [], "colors": [], "attributes": [], "operations": [], "enum_literals": []} for elem_type in ELEMENTS_TYPE}
    
    # Iterar sobre todos os elementos do diagrama
    for element in diagram_elements:
        elem_type = element.get("{http://www.w3.org/2001/XMLSchema-instance}type").split(':')[-1]
        
        # Verificar se o elemento existe no dicionário
        if elem_type in type_dict:
            # Guardar o tipo de elemento no conjunto
            ELEMENT_TYPES_IN_DIAGRAM.add(elem_type)

            # Extrair o ID, nome, cor, atributos, operações e literais do elemento (se existir)
            elem_id = element.attrib.get('modelElement')

            if elem_id is None:
                continue

            elem_name = ""
            elem_color = ""
            elem_attributes = []
            elem_operations = []
            elem_enum_literals = []

            if elem_type in ELEMENTS:
                elem_element = root.find(".//*[@{http://schema.omg.org/spec/XMI/2.1}id='" + elem_id + "']")

                if elem_element is not None:
                    elem_name = elem_element.attrib.get('name', '')

            if 'color' in element.attrib:
                elem_color = element.attrib['color']

            if elem_type in {"ClassWidget", "InterfaceWidget"}:
                elem_attributes = [attribute.attrib.get('name', '') for attribute in root.findall(".//*[@{http://schema.omg.org/spec/XMI/2.1}id='" + elem_id + "']/ownedAttribute")]
                elem_operations = [operation.attrib.get('name', '') for operation in root.findall(".//*[@{http://schema.omg.org/spec/XMI/2.1}id='" + elem_id + "']/ownedOperation")]

            if elem_type == "EnumerationWidget":
                elem_enum_literals = [enum_literal.attrib.get('name', '') for enum_literal in root.findall(".//*[@{http://schema.omg.org/spec/XMI/2.1}id='" + elem_id + "']/ownedLiteral")]

            # Adicionar o ID, nome e cor, atributos, operações e literais do elemento ao dicionário de tipos
            type_dict[elem_type]["ids"].append(elem_id)
            type_dict[elem_type]["names"].append(elem_name)
            type_dict[elem_type]["colors"].append(elem_color)
            type_dict[elem_type]["attributes"].append(elem_attributes)
            type_dict[elem_type]["operations"].append(elem_operations)
            type_dict[elem_type]["enum_literals"].append(elem_enum_literals)
    
    # Verificar se todos os elementos são de tipos diferentes
    if all(len(type_dict[elem_type]["ids"]) == 1 for elem_type in ELEMENTS_TYPE):
        return [True, 0]

    # Verificar se os elementos de cada tipo são perceptualmente discrimináveis
    else:
        occurrences = 0

        for elem_type in ELEMENT_TYPES_IN_DIAGRAM:

            ids = type_dict[elem_type]["ids"]                    
            colors = type_dict[elem_type]["colors"]
            names = type_dict[elem_type]["names"]
            attributes = type_dict[elem_type]["attributes"]
            operations = type_dict[elem_type]["operations"]
            enum_literals = type_dict[elem_type]["enum_literals"]
            
            # Verificar se os elementos são perceptualmente discrimináveis

            if elem_type in {"ClassWidget", "InterfaceWidget"}:
                for i in range(len(ids)):
                    for j in range(i + 1, len(ids)):
                        if colors[i] == colors[j] and names[i] == names[j] and attributes[i] == attributes[j] and operations[i] == operations[j]:
                            occurrences += 1

            elif elem_type in {"PackageWidget", "DataTypeWidget"}:
                for i in range(len(ids)):
                    for j in range(i + 1, len(ids)):
                        if colors[i] == colors[j] and names[i] == names[j]:
                            occurrences += 1

            elif elem_type == "EnumerationWidget":
                for i in range(len(ids)):
                    for j in range(i + 1, len(ids)):
                        if colors[i] == colors[j] and names[i] == names[j] and enum_literals[i] == enum_literals[j]:
                            occurrences += 1

            else:
                for i in range(len(ids)):
                    for j in range(i + 1, len(ids)):
                        if colors[i] == colors[j] and colors[i]:
                            occurrences += 1
                        
        if occurrences > 0:
            return [False, occurrences]
        else:
            return [True, 0]


# Função para obter o número de elementos num diagrama (Diagram Size)
def check_for_diagram_size(root):

    diagram_elements = 0

    # Percorrer todos os elementos do diagrama
    for elem in root.findall(".//ownedDiagramElements"):
        if 'modelElement' in elem.attrib and elem.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] in ["com.genmymodel.graphic.uml:" + elem_type for elem_type in ELEMENTS_TYPE]:
            diagram_elements += 1

    return [diagram_elements >= 20 and diagram_elements <= 60, diagram_elements]


# Função auxiliar para obter o ID, posição e dimensões do elementos do diagrama
def get_elements_info(root):
    elements = {}

    # Percorrer todos os elementos do diagrama
    for elem in root.findall(".//ownedDiagramElements"):
        elem_type = elem.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']

        # Verificar se o tipo de elemento pertence ao conjunto de elementos
        if elem_type in ["com.genmymodel.graphic.uml:" + elem_type for elem_type in ELEMENTS]:
            
            # Obter o ID, posição e dimensões do elementos
            elem_id = elem.attrib.get('modelElement')
            
            if elem_id is None:
                continue

            # Verificar se o x e o y existem
            if 'x' in elem.attrib:
                x = float(elem.attrib['x'])
            else:
                x = 0.0

            if 'y' in elem.attrib:
                y = float(elem.attrib['y'])
            else:
                y = 0.0

            if 'width' in elem.attrib:
                width = float(elem.attrib['width'])
            else:
                width = 0.0
            
            if 'height' in elem.attrib:
                height = float(elem.attrib['height'])
            else:
                height = 0.0

            # Adicionar o elemento ao dicionário
            elements[elem_id] = (x, y, width, height)

    return elements


# Função para verificar se os elementos se sobrepõem (Overlapping Elements)
def check_for_overlapping_elements(root):

    elements = get_elements_info(root)
    overlapping_elements = 0

    for i, (id_1, pos1) in enumerate(elements.items()):
        for id_2, pos2 in list(elements.items())[i+1:]:
            x1, y1, w1, h1 = pos1
            x2, y2, w2, h2 = pos2

            # Verificar se os elementos se sobrepõem no eixo dos x
            if x1 < x2 + w2 and x1 + w1 > x2:
                # Verificar se os elementos se sobrepõem no eixo dos y
                if y1 < y2 + h2 and y1 + h1 > y2:
                    overlapping_elements += 1

    return [overlapping_elements > 0, overlapping_elements]


def get_relationships_elements_coordinates(root):

    relationships = {}

    WaypointWidget = root.findall(".//ownedDiagramElements[@{http://www.w3.org/2001/XMLSchema-instance}type='com.genmymodel.ecoreonline.graphic:WaypointWidget']")
    AnchorWidget = root.findall(".//ownedDiagramElements[@{http://www.w3.org/2001/XMLSchema-instance}type='com.genmymodel.ecoreonline.graphic:AnchorWidget']")

    for anchor_widget in AnchorWidget:

        # Veficar se o elemento é um ponto inicial
        if anchor_widget.get('targetSegments'):
            initial_point = anchor_widget
            initial_point_target = initial_point.attrib.get('targetSegments')
        else:
            continue

        # Verificar se existe o primeiro ponto intermédio
        intermediate_point_1 = None
        intermediate_point_1_target = None
        for waypoint_widget in WaypointWidget:
            if waypoint_widget.attrib.get('sourceSegments') == initial_point_target:
                intermediate_point_1 = waypoint_widget
                intermediate_point_1_target = intermediate_point_1.attrib.get('targetSegments')
                break
        else:
            continue

        # Verificar se existe o segundo ponto intermédio
        intermediate_point_2 = None
        intermediate_point_2_target = None
        for waypoint_widget in WaypointWidget:
            if waypoint_widget.attrib.get('sourceSegments') == intermediate_point_1_target:
                intermediate_point_2 = waypoint_widget
                intermediate_point_2_target = intermediate_point_2.attrib.get('targetSegments')
                break
        else:
            continue

        # Verificar se existe o ponto final
        final_point = None
        for anchor_widget_final in AnchorWidget:
            if anchor_widget_final.attrib.get('sourceSegments') == intermediate_point_2_target:
                final_point = anchor_widget_final
                break
        else:
            continue

        # Obter as coordenadas dos elementos
        id = intermediate_point_1.attrib.get('modelElement')
        initial_point_coordinates = (float(initial_point.attrib.get('x', 0.0)), float(initial_point.attrib.get('y', 0.0)))
        intermediate_point_1_coordinates = (float(intermediate_point_1.attrib.get('x', 0.0)), float(intermediate_point_1.attrib.get('y', 0.0)))
        intermediate_point_2_coordinates = (float(intermediate_point_2.attrib.get('x', 0.0)), float(intermediate_point_2.attrib.get('y', 0.0)))
        final_point_coordinates = (float(final_point.attrib.get('x', 0.0)), float(final_point.attrib.get('y', 0.0)))

        relationships[id] = [initial_point_coordinates, intermediate_point_1_coordinates, intermediate_point_2_coordinates, final_point_coordinates]

    # Caso especial para: Dependency, Usage, Import, Template Binding e Inner relation
    for anchor_widget in AnchorWidget:

        # Veficar se o elemento é um ponto inicial
        initial_point = None
        if anchor_widget.get('targetSegments'):
            initial_point = anchor_widget
            initial_point_target = initial_point.attrib.get('targetSegments')
        
            # Verificar se existe o ponto final
            final_point = None
            for anchor_widget_final in AnchorWidget:
                if anchor_widget_final.attrib.get('sourceSegments') == initial_point_target:
                    final_point = anchor_widget_final
                    break
        
        if initial_point and final_point:
            # Calcular as coordenadas intermédias
            intermediate_point_x = (float(initial_point.attrib.get('x', 0.0)) + float(final_point.attrib.get('x', 0.0))) / 2.0
            intermediate_point_y = (float(initial_point.attrib.get('y', 0.0)) + float(final_point.attrib.get('y', 0.0))) / 2.0

            # Obter as coordenadas dos elementos
            id = initial_point.attrib.get('modelElement')

            # Caso especial para o Inner relation
            if id is None:
                id = initial_point.attrib.get('targetSegments')

            initial_point_coordinates = (float(initial_point.attrib.get('x', 0.0)), float(initial_point.attrib.get('y', 0.0)))
            intermediate_point_1_coordinates = (intermediate_point_x, intermediate_point_y)
            intermediate_point_2_coordinates = (intermediate_point_x, intermediate_point_y)
            final_point_coordinates = (float(final_point.attrib.get('x', 0.0)), float(final_point.attrib.get('y', 0.0)))

            relationships[id] = [initial_point_coordinates, intermediate_point_1_coordinates, intermediate_point_2_coordinates, final_point_coordinates]

    return relationships


# Função auxiliar para verificar se dois segmentos de reta se intersectam
def has_intersection(p1, p2, p3, p4):

    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])

        if val == 0:
            return 0
        
        return -1 if val > 0 else 1

    o1 = orientation(p1, p2, p3)
    o2 = orientation(p1, p2, p4)
    o3 = orientation(p3, p4, p1)
    o4 = orientation(p3, p4, p2)

    if o1 != o2 and o3 != o4:
        if (min(p1[0], p2[0]) < p3[0] < max(p1[0], p2[0]) and min(p3[0], p4[0]) < p1[0] < max(p3[0], p4[0])):
            return True
        if (min(p1[1], p2[1]) < p3[1] < max(p1[1], p2[1]) and min(p3[1], p4[1]) < p1[1] < max(p3[1], p4[1])):
            return True
        if (min(p1[0], p2[0]) < p4[0] < max(p1[0], p2[0]) and min(p3[1], p4[1]) < p2[1] < max(p3[1], p4[1])):
            return True
        if (min(p1[1], p2[1]) < p4[1] < max(p1[1], p2[1]) and min(p3[0], p4[0]) < p2[0] < max(p3[0], p4[0])):
            return True
        return False
    else:
        return False


# Função para verficar se existem interseções entre as relações ou relações e elementos (Intersections)
def check_for_intersections(root):
    
    # Obter as coordenadas dos elementos de cada relação
    relationships = get_relationships_elements_coordinates(root)

    line_segments = []
    intersections = 0

    # Obter os segmentos de reta de cada relação
    for id, points in relationships.items():
        # Verificar se os pontos intermédios são diferentes por mais de 2 unidades
        if abs(points[1][0] - points[2][0]) > 2 or abs(points[1][1] - points[2][1]) > 2:
            line_segments.append([points[0], points[1]])
            line_segments.append([points[1], points[2]])
            line_segments.append([points[2], points[3]])
        # Caso contrário, considerar apenas os pontos inicial e final, ou seja, a relação é uma linha reta
        else:
            line_segments.append([points[0], points[3]])

    # Verificar se existem interseções entre os segmentos de reta
    for i in range(len(line_segments)):
        for j in range(i + 1, len(line_segments)):
            if has_intersection(line_segments[i][0], line_segments[i][1], line_segments[j][0], line_segments[j][1]):
                intersections += 1

    # Verificar se existem interseções entre as relações e outros elementos
    elements = get_elements_info(root)

    for i in range(len(line_segments)):
        for elem_id, elem_info in elements.items():
            x = elem_info[0]
            y = elem_info[1]
            width = elem_info[2]
            height = elem_info[3]

            # Verificar se o segmento de reta intersecta o elemento
            if has_intersection(line_segments[i][0], line_segments[i][1], (x, y), (x + width, y)) or \
               has_intersection(line_segments[i][0], line_segments[i][1], (x, y), (x, y + height)) or \
               has_intersection(line_segments[i][0], line_segments[i][1], (x + width, y), (x + width, y + height)) or \
               has_intersection(line_segments[i][0], line_segments[i][1], (x, y + height), (x + width, y + height)):
                intersections += 1
            
    return [intersections > 0, intersections]


# Função auxiliar para verificar se numa relação existem dois segmentos de reta
def has_two_lines(initial_point, intermediate_point_1, intermediate_point_2, final_point):

    X_axis = []
    Y_axis = []

    # Adicionar as coordenadas dos pontos
    X_axis.append(initial_point[0])
    X_axis.append(intermediate_point_1[0])
    X_axis.append(intermediate_point_2[0])
    X_axis.append(final_point[0])

    Y_axis.append(initial_point[1])
    Y_axis.append(intermediate_point_1[1])
    Y_axis.append(intermediate_point_2[1])
    Y_axis.append(final_point[1])

    # Verificar existem 3 pontos com a mesma coordenada no eixo dos x
    if X_axis.count(X_axis[0]) == 3 or X_axis.count(X_axis[1]) == 3 or X_axis.count(X_axis[2]) == 3 or X_axis.count(X_axis[3]) == 3:
        return True
    
    # Verificar existem 3 pontos com a mesma coordenada no eixo dos y
    if Y_axis.count(Y_axis[0]) == 3 or Y_axis.count(Y_axis[1]) == 3 or Y_axis.count(Y_axis[2]) == 3 or Y_axis.count(Y_axis[3]) == 3:
        return True
    
    return False


# Função para verificar se existem curvas nas relações (Bends in Lines)
def check_for_bends_in_lines(root):

    bend_in_lines = 0
    
    relationships = get_relationships_elements_coordinates(root)

    for id, points in relationships.items():
        # Verificar se os pontos intermédios são diferentes por mais de 2 unidades
        if abs(points[1][0] - points[2][0]) > 2 or abs(points[1][1] - points[2][1]) > 2:
            if has_two_lines(points[0], points[1], points[2], points[3]):
                bend_in_lines += 1
            else:
                bend_in_lines += 2

    return [bend_in_lines > 0, bend_in_lines]


# Função auxiliar para verificar se dois segmentos de reta estão muito próximos um do outro
def is_close(segment1, segment2):

    limit_x = 10
    limit_y = 25

    x1_1, y1_1 = segment1[0]
    x1_2, y1_2 = segment1[1]
    x2_1, y2_1 = segment2[0]
    x2_2, y2_2 = segment2[1]

    # Calculate distances between two line segments
    denominator = math.sqrt((y2_2 - y2_1) ** 2 + (x2_2 - x2_1) ** 2)
    if denominator == 0:
        distance1 = float('inf')
    else:
        distance1 = abs((y2_2 - y2_1) * x1_1 - (x2_2 - x2_1) * y1_1 + x2_2 * y2_1 - y2_2 * x2_1) / denominator

    denominator = math.sqrt((y2_2 - y2_1) ** 2 + (x2_2 - x2_1) ** 2)
    if denominator == 0:
        distance2 = float('inf')
    else:
        distance2 = abs((y2_2 - y2_1) * x1_2 - (x2_2 - x2_1) * y1_2 + x2_2 * y2_1 - y2_2 * x2_1) / denominator

    denominator = math.sqrt((y1_2 - y1_1) ** 2 + (x1_2 - x1_1) ** 2)
    if denominator == 0:
        distance3 = float('inf')
    else:
        distance3 = abs((y1_2 - y1_1) * x2_1 - (x1_2 - x1_1) * y2_1 + x1_2 * y1_1 - y1_2 * x1_1) / denominator

    denominator = math.sqrt((y1_2 - y1_1) ** 2 + (x1_2 - x1_1) ** 2)
    if denominator == 0:
        distance4 = float('inf')
    else:
        distance4 = abs((y1_2 - y1_1) * x2_2 - (x1_2 - x1_1) * y2_2 + x1_2 * y1_1 - y1_2 * x1_1) / denominator

    if (distance1 < limit_x and distance2 < limit_x) or (distance3 < limit_y and distance4 < limit_y):
        return True

    return False


# Função auxiliar para verificar duas relações partilham um endpoint
def share_one_endpoint(root, id1, id2):
    id1_endpoints = []
    id2_endpoints = []

    # Caso sejam Assocation / Assication Class
    for elem in root.findall(".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:Association']" or 
                             ".//packagedElement[@{http://www.w3.org/2001/XMLSchema-instance}type='uml:AssociationClass']"):

        # Obter os endpoints da associação 1
        if elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == id1:
            for endpoint in elem.attrib['memberEnd'].split():
                for ownedEnd in elem.findall("./ownedEnd"):
                    if 'type' in ownedEnd.attrib and ownedEnd.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == endpoint:
                        id1_endpoints.append(ownedEnd.attrib['type'])

        # Obter os endpoints da associação 2
        if elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == id2:
            for endpoint in elem.attrib['memberEnd'].split():
                for ownedEnd in elem.findall("./ownedEnd"):
                    if 'type' in ownedEnd.attrib and ownedEnd.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == endpoint:
                        id2_endpoints.append(ownedEnd.attrib['type'])

    # Caso seja Generalization
    for elem in root.findall(".//generalization"):
        # Obter os endpoints da generalização 1
        if 'general' in elem.attrib and 'specific' in elem.attrib and elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == id1:
            id1_endpoints.append(elem.attrib['general'])
            id1_endpoints.append(elem.attrib['specific'])
        
        # Obter os endpoints da generalização 2
        if 'general' in elem.attrib and 'specific' in elem.attrib and elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == id2:
            id2_endpoints.append(elem.attrib['general'])
            id2_endpoints.append(elem.attrib['specific'])

    # Caso seja Realization / Dependency / Usage
    for elem in root.findall(".//packagedElement[@{http://schema.omg.org/spec/XMI/2.1}type='uml:Dependency']" or 
                             ".//interfaceRealization" or
                             ".//packagedElement[@{http://schema.omg.org/spec/XMI/2.1}type='uml:Usage']"):
        # Obter os endpoints da relação 1
        if 'client' in elem.attrib and 'supplier' in elem.attrib and elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == id1:
            id1_endpoints.append(elem.attrib['client'])
            id1_endpoints.append(elem.attrib['supplier'])
        
        # Obter os endpoints da relação 2
        if 'client' in elem.attrib and 'supplier' in elem.attrib and elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == id2:
            id2_endpoints.append(elem.attrib['client'])
            id2_endpoints.append(elem.attrib['supplier'])

    # Caso seja Import
    for elem in root.findall(".//elementImport"):
        # Obter os endpoints da relação 1
        if 'importedElement' in elem.attrib and 'importingNamespace' in elem.attrib and elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == id1:
            id1_endpoints.append(elem.attrib['importedElement'])
            id1_endpoints.append(elem.attrib['importingNamespace'])
        
        # Obter os endpoints da relação 2
        if 'importedElement' in elem.attrib and 'importingNamespace' in elem.attrib and elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == id2:
            id2_endpoints.append(elem.attrib['importedElement'])
            id2_endpoints.append(elem.attrib['importingNamespace'])

    # Caso seja Template Binding
    for elem in root.findall(".//templateBinding"):
        # Obter os endpoints da relação 1
        if 'boundElement' in elem.attrib and 'signature' in elem.attrib and elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == id1:
            id1_endpoints.append(elem.attrib['boundElement'])
            id1_endpoints.append(elem.attrib['signature'])
        
        # Obter os endpoints da relação 2
        if 'boundElement' in elem.attrib and 'signature' in elem.attrib and elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == id2:
            id2_endpoints.append(elem.attrib['boundElement'])
            id2_endpoints.append(elem.attrib['signature'])

    # Caso seja Inner relation
    for element in root.findall(".//ownedDiagramElements"):
        element_type = element.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']
        if element_type == 'com.genmymodel.ecoreonline.graphic:AnchorWidget':

            # Obter os endpoints da Inner relation 1
            if ('sourceSegments' in element.attrib and element.attrib['sourceSegments'] == id1) or ('targetSegments' in element.attrib and element.attrib['targetSegments'] == id1):
                elem_id = element.attrib['attachedElement']

                for elem in root.findall(".//ownedDiagramElements"):
                    if elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == elem_id:
                        id2_endpoints.append(elem.attrib['modelElement'])

            # Obter os endpoints da Inner relation 2
            if ('sourceSegments' in element.attrib and element.attrib['sourceSegments'] == id2) or ('targetSegments' in element.attrib and element.attrib['targetSegments'] == id2):
                elem_id = element.attrib['attachedElement']

                for elem in root.findall(".//ownedDiagramElements"):
                    if elem.attrib['{http://schema.omg.org/spec/XMI/2.1}id'] == elem_id:
                        id2_endpoints.append(elem.attrib['modelElement'])

    # Verificar se as associações partilham um endpoint
    for i in range(len(id1_endpoints)):
        for j in range(len(id2_endpoints)):
            if id1_endpoints[i] == id2_endpoints[j]:
                return True
    
    return False


# Função auxiliar para verificar se as relações são do mesmo tipo
def same_relationship_type(root, id1, id2):

    elem_type1 = ""
    elem_type2 = ""

    # Verificar o tipo da relação 1
    for elem in root.findall(".//ownedDiagramElements"):
        if 'modelElement' in elem.attrib and elem.attrib['modelElement'] == id1 and elem.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] in ["com.genmymodel.graphic.uml:" + elem_type for elem_type in ELEMENTS_TYPE]:
            elem_type1 = elem.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']
            break

    # Verificar o tipo da relação 2
    for elem in root.findall(".//ownedDiagramElements"):
        if 'modelElement' in elem.attrib and elem.attrib['modelElement'] == id2 and elem.attrib['{http://www.w3.org/2001/XMLSchema-instance}type'] in ["com.genmymodel.graphic.uml:" + elem_type for elem_type in ELEMENTS_TYPE]:
            elem_type2 = elem.attrib['{http://www.w3.org/2001/XMLSchema-instance}type']
            break

    # Verificar se os tipos são iguais
    if elem_type1 == elem_type2:
        return True

    return False


# Função para verificar se existem relações que estão juntas ou muito próximas, a menos que sejam do mesmo tipo e partilhem exatamente um endpoint (Close Lines)
def check_for_close_merged_or_aligned_lines(root):
    
    close_lines = 0
    line_segments = []

    relationships = get_relationships_elements_coordinates(root)

    # Obter os segmentos de reta de cada relação
    for id, points in relationships.items():

        # Verificar se os pontos intermédios são diferentes por mais de 2 unidades
        if abs(points[1][0] - points[2][0]) > 2 or abs(points[1][1] - points[2][1]) > 2:
            line_segments.append([id, [points[0], points[1]]])
            line_segments.append([id, [points[1], points[2]]])
            line_segments.append([id, [points[2], points[3]]])

        # Caso contrário, considerar apenas os pontos inicial e final, ou seja, a relação é uma linha reta
        else:
            line_segments.append([id, [points[0], points[3]]])
    
    # Verificar se existem segmentos de reta muito próximos
    for i in range(len(line_segments)):
        for j in range(i + 1, len(line_segments)):
            if line_segments[i][0] != line_segments[j][0]:
                if is_close(line_segments[i][1], line_segments[j][1]) and not share_one_endpoint(root, line_segments[i][0], line_segments[j][0]) and not same_relationship_type(root, line_segments[i][0], line_segments[j][0]):
                    close_lines += 1

    return [close_lines > 0, close_lines]


# Função para ler o range de IDs do ficheiro txt
def read_files_ids(initial_file, final_file):

    FOLDER = "../../Web Scraper/Google Colab/"
    FILE = "downloaded_files.txt"

    # Abrir o ficheiro e ler as linhas
    with open(FOLDER + FILE, 'r') as file:
        lines = file.read().splitlines()        

    return lines[initial_file:final_file]


# Função para guardar os resultados num ficheiro CSV
def save_results_to_csv(filename, file_id, elements_without_color, relationships_without_description, element_types, perceptual_discriminability, diagram_size, overlapping_elements, intersections, bends_in_lines, close_merged_or_aligned_lines):

    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([file_id, elements_without_color, relationships_without_description, element_types, perceptual_discriminability, diagram_size, overlapping_elements, intersections, bends_in_lines, close_merged_or_aligned_lines])