# Nombre del archivo de texto
input_file = "datos.txt"

# Nombre del archivo .tsp a generar
output_file = "ciudades.tsp"

# Abrir el archivo de texto de entrada y leer los datos
with open(input_file, "r") as file:
    lines = file.readlines()

# Número de ciudades
num_cities = len(lines)

# Escribir los datos en el formato .tsp
with open(output_file, "w") as file:
    file.write(f"NAME: CustomTSP\n")
    file.write(f"TYPE: TSP\n")
    file.write(f"COMMENT: Custom TSP with {num_cities} cities\n")
    file.write(f"DIMENSION: {num_cities}\n")
    file.write(f"EDGE_WEIGHT_TYPE: EUC_2D\n")
    file.write(f"NODE_COORD_SECTION\n")

    for line in lines:
        city_data = line.split()
        city_name = city_data[0]
        x_coord = city_data[1]
        y_coord = city_data[2]
        file.write(f"{city_name} {x_coord} {y_coord}\n")

    file.write("EOF\n")

print(f"Archivo {output_file} creado exitosamente.")
