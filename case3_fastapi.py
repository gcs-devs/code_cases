from fastapi import FastAPI, HTTPException
from typing import List, Dict
import csv

app = FastAPI()

def read_filename(filename):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Cabeçalho ignorado
        return list(reader)

def log_processing(log):
    result = {}
    for line in log:
        _, id_hero, _, laptime, _ = line
        code = id_hero.split('–')[0]
        if code not in result:
            # separando não por '-', mas por '–'"
            hero_name = id_hero.split('–')[1].strip()
            new_result = {'nome': hero_name, 'voltas': 0, 'tempo_total': 0}
            result[code] = new_result
        result[code]['voltas'] += 1
        result[code]['tempo_total'] += seconds_conversion(laptime)
        if result[code]['voltas'] == 4:	# prova finalizada após o vencedor completar as 4 voltas
            break
    return result

def seconds_conversion(timestamp):
    minute, second = map(float, timestamp.split(':'))
    return minute * 60 + second

def finish_position_calculate(result):
    return sorted(result.items(), key=lambda x: x[1]['tempo_total'])

def log_report(positions):
    report = []
    for position, (code, info) in enumerate(positions, start=1):
        report.append({
            'Posição de Chegada': position,
            'Código do Super-herói': code,
            'Nome Super-herói': info['nome'],
            'Quantidade de Voltas Completadas': info['voltas'],
            'Tempo Total de Prova': timestamp_conversion(info['tempo_total'])
        })
    return report

def timestamp_conversion(secs):
    minute, second = divmod(secs, 60)
    return f"{int(minute):02d}:{int(second):02d}"


@app.get('/relatorio', response_model=List[Dict])
def relatorio_corrida():
    try:
        # Chame a função principal aqui e retorne o relatório como JSON
        log = read_filename('log_corrida.csv')
        result = log_processing(log)
        position = finish_position_calculate(result)
        report = log_report(position)
        return report
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo de log não encontrado")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=6969)
