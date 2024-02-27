from flask import Flask, request, jsonify

app = Flask(__name__)

class ImageCounter:
    def __init__(self, image_map):
        self.image = image_map
        self.counter_dict = {i: 0 for i in range(16)}  # Inicializa contadores

    def count_elements(self, vector):
        # Zera as contagens
        self.counter_dict = {i: 0 for i in range(16)}
        
        # Percorre a matriz de pixels e atualiza os contadores
        for row in self.image:
            for element in row:
                self.counter_dict[element] += 1

        return self.counter_dict

@app.route('/counter', methods=['POST'])
def counter_api():
    data = request.get_json()
    inputs = data.get('vector')
    
    # Exemplo de matriz de pixels
    image = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15]
    ]

    # Instancia a classe ImageCounter para contar os elementos
    image_counter = ImageCounter(image)
    count_dict = image_counter.count_elements(inputs)

    return jsonify(count_dict)

if __name__ == '__main__':
    app.run(debug=True)
