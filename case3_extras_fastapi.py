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
    hero_laps = {}
    for line in log:
        print(line)
        _, id_hero, _, laptime, mean_speed = line
        code = id_hero.split('–')[0]
        if code not in result:
            # separando não por '-', mas por '–'"
            hero_name = id_hero.split('–')[1].strip()
            result[code] = {'nome': hero_name, 'voltas': 0, 'tempo_total': 0, 'melhor_volta': float('inf'), 'velocidade_media': 0.0}
            hero_laps[code] = []
        laptime_secs = seconds_conversion(laptime)
        result[code]['voltas'] += 1
        result[code]['tempo_total'] += laptime_secs
        result[code]['velocidade_media'] += float(mean_speed.replace(',', '.'))
        hero_laps[code].append(laptime_secs)
        if laptime_secs < result[code]['melhor_volta']:
            result[code]['melhor_volta'] = laptime_secs
    return result, hero_laps

def seconds_conversion(timestamp):
    minute, second, = map(float, timestamp.split(':'))
    return minute * 60 + second

def finish_position_calculate(result):
    return sorted(result.items(), key=lambda x: x[1]['tempo_total'])

def hero_best_calculate(hero_lap):
    best_hero = {}
    for code, laps in hero_lap.items():
        best_hero[code] = min(laps)
    return best_hero

def lap_best_calculate(hero_lap):
    best_lap = [lap for laps in hero_lap.values() for lap in laps]
    return min(best_lap)

def log_report(positions, best_hero, best_lap):
    report = []
    for position, (code, info) in enumerate(positions, start=1):
        report.append({
            'Posição de Chegada': position,
            'Código do Super-herói': code,
            'Nome Super-herói': info['nome'],
            'Quantidade de Voltas Completadas': info['voltas'],
            'Tempo Total de Prova': timestamp_conversion(info['tempo_total']),
            'Melhor Volta': timestamp_conversion(best_hero[code]),
            'Velocidade Média (km/h)': info['velocidade_media']
        })
    report.append({
        'Melhor Volta da Corrida': timestamp_conversion(best_lap)
    })
    return report

def timestamp_conversion(secs):
    minute, second = divmod(secs, 60)
    return f"{int(minute):02d}:{int(second):02d}"


@app.get('/relatorio', response_model=List[Dict])
def relatorio_corrida():
    # Chame a função principal aqui e retorne o relatório como JSON
    log = read_filename('log_corrida.csv')
    result, hero_laps = log_processing(log)
    positions = finish_position_calculate(result)
    hero_best = hero_best_calculate(hero_laps)
    lap_best = lap_best_calculate(hero_laps)
    report = log_report(positions, hero_best, lap_best)
    return report

# Exemplo de uso
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=6969)
