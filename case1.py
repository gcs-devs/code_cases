class ImageCounter:
    def __init__(self, image_map):
        self.image_map = image_map
        self.counter_dict = {i: 0 for i in range(16)}  # Inicializa contadores

    def count_elements(self, vector):
        # Zera as contagens
        self.counter_dict = {i: 0 for i in range(16)}
        
        # Percorre a matriz de pixels e atualiza os contadores
        for row in self.image_map:
            for element in row:
                if element in self.counter_dict:  # Verifica se o elemento está no intervalo de contagem
                    self.counter_dict[element] += 1

        # Gerando string de saída (formato de LOG)
        output_log = ""
        for i, count in self.counter_dict.items():
            output_log += f"Elemento {i}: {count} vezes\n"

        return output_log

# Exemplo de uso
image_map = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9, 10, 11],
    [12, 13, 14, 15]
]
inputs = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

image_counter = ImageCounter(image_map)
result = image_counter.count_elements(inputs)
print(result)

