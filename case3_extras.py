import csv

def read_filename(filename):
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)  # Cabeçalho ignorado
        return list(reader)

def log_processing(log):
    result = {}
    hero_laps = {}
    for line in log:
        _, id_hero, _, laptime, mean_speed = line
        code = id_hero.split('-')[0]
        if code not in result:
            result[code] = {'nome': id_hero.split('-')[1], 'voltas': 0, 'tempo_total': 0, 'melhor_volta': float('inf')}
            hero_laps[code] = []
        laptime_secs = seconds_conversion(tempo_volta)
        result[code]['voltas'] += 1
        result[code]['tempo_total'] += laptime_secs
        hero_laps[code].append(laptime_secs)
        if laptime_secs < result[code]['melhor_volta']:
            resultado[code]['melhor_volta'] = laptime_secs
    return resultado, hero_laps

def seconds_conversion(timestamp):
    minute, second, milisecs = map(float, timestamp.split(':'))
    return minute * 60 + second + milisecs / 1000

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

def mean_speed_calculate(result, scale=10):
    mean_spds = {}
    for code, info in result.items():
        total_time_secs = info['tempo_total']
        total_distance_km = info['voltas'] * scale  # Assumindo que cada volta tem 10 km, definidos em `scale`
        mean_spds[code] = total_distance_km / (total_time_secs / 3600)  # Convertendo tempo de segundos para horas
    return mean_spds

def log_report(positions, best_hero, best_lap, mean_spds):
    report = []
    for position, (code, info) in enumerate(positions, start=1):
        report.append({
            'Posição de Chegada': position,
            'Código do Super-herói': code,
            'Nome Super-herói': info['nome'],
            'Quantidade de Voltas Completadas': info['voltas'],
            'Tempo Total de Prova': timestamp_conversion(info['tempo_total']),
            'Melhor Volta': timestamp_conversion(best_hero[code]),
            'Velocidade Média (km/h)': mean_spds[code]
        })
    report.append({
        'Melhor Volta da Corrida': timestamp_conversion(best_lap)
    })
    return report

def timestamp_conversion(secs):
    minute, second = divmod(secs, 60)
    return f"{int(minute):02d}:{int(second):02d}"

def main():
    log = read_filename('log_corrida.csv')
    resultado, voltas_herois = processar_log(log)
    posicoes = calcular_posicao_chegada(resultado)
    melhor_volta_super_heroi = calcular_melhor_volta_super_heroi(voltas_herois)
    melhor_volta_corrida = calcular_melhor_volta_corrida(voltas_herois)
    velocidades_medias = calcular_velocidade_media(resultado)
    relatorio = gerar_relatorio(posicoes, melhor_volta_super_heroi, melhor_volta_corrida, velocidades_medias)
    return relatorio

# Exemplo de uso
if __name__ == "__main__":
    relatorio = main()
    for linha in relatorio:
        print(linha)

