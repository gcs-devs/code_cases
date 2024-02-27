from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

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


# Classe padronizada para leitura de JSON pelo FastAPI
class VectorInput(BaseModel):
    vector: List[int]

# Executar POST, header Content-Type = application/json e o JSON no body!
@app.post("/counter")
async def counter_api(vector_input: VectorInput):
    inputs = vector_input.vector
    
    # Exemplo de matriz de pixels
    image = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15]
    ]

    # Instancia a classe ImageCounter para contar os elementos
    image_counter = ImageCounter(image)
    counter_dict = image_counter.count_elements(inputs)

    return counter_dict


# Definindo porta alternativa para o app
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=6969)
