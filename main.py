import sys
import numpy as np
import matplotlib.pyplot as plt

def load_file(file, extension='.txt'):
    """Lê os dados de um arquivo separados por quebra de linha."""
    try:
        with open(f'{file}{extension}', 'r') as f:
            data = [int(linha.strip()) for linha in f if linha.strip().isdigit()]
    except:
        print(f'Arquivo "{file}{extension}" não encontrado.')
        return None
    return np.array(data)

def summary(data, p=90) -> (int, int, int, any):
    """Calcula percentil, média e variância dos dados."""
    percentile = np.percentile(data, p)

    data_ = data[data <= percentile]

    mean = np.mean(data_)
    variance = np.var(data_)
    return (percentile, mean, variance, data_)

def plot(name="dados", p=100, y_limit_min=0, y_limit_max=None, clip=False):
    """Plota um gráfico mostrando a variação dos dados."""


    data = load_file(name)
    if data is None :
        return


    percentile, mean, variance, data_ = summary(data, p)
    if clip:
        data = data_
        mean = np.mean(data_)
        variance = np.var(data_)
        filename = f"plots/grafico_{name}_{p}_clipped.png"
    else:
        filename = f"plots/grafico_{name}_{p}_noclip.png"

    print(f"P{p}: {percentile} ns | Média: {mean:.2f} ns | Variância: {variance:.2f} ns") 


    plt.figure(figsize=(10, 5))



    if(p != 100) and not clip:
        plt.axhline(y=percentile, color='r', linestyle='-', label=f'P{p}')
    plt.axhline(y=mean, color='black', linestyle='-', label=f'Média')

    plt.xlabel('Amostra')
    plt.ylabel('Tempo (ns)')

    #plt.plot(data_, marker=None, linestyle='-', label='Desempenho')
    plt.scatter(range(len(data)), data, s=1, color='blue', alpha=0.3)
    # plt.fill_between(range(len(data_)), y1=percentile, y2=int(y_limit_max), color='red', alpha=0.3)


    plt.ylim(bottom=int(y_limit_min))
    if y_limit_max:
        plt.ylim(top=int(y_limit_max))

    if clip:
        plt.title(f'Variação do Desempenho {name} P{p}')
    else:
        plt.title(f'Variação do Desempenho {name}')
    plt.legend()
    estatisticas_texto = f"Média: {mean:.2f} ns\nVariância: {variance:.2f} ns\nP{p}: {percentile} ns"
    plt.legend(title=estatisticas_texto)
    plt.grid()


    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f'Salvo como: "{filename}"')


def main():
    config = {
        "nome":None,
        "p":100,
        "clip":False,
        "ymax":None,
    }

    if len (sys.argv) < 2 :
        print (f'Esperados os campos {config}')
        return
    

    for param in sys.argv[1:]:
        param = param.split("=")
        if len (param) == 2 :            
            config[param[0]] = param[1]


    
       
    plot(
        name=config['nome'],
        p=int(config['p']),
        clip=bool(config['clip']),
        y_limit_max=config['ymax']
    )

if __name__ == "__main__":
    main()

