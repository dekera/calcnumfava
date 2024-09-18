import numpy as np
import pandas as pd

# Função para calcular a função de recorrência P_d(t)
def P(d, t):
    if d == 0:
        return 1  # P0(t)
    elif d == 1:
        return t  # P1(t)
    else:
        return ((2 * (d - 1) + 1) / d) * t * P(d - 1, t) - ((d - 1) / d) * P(d - 2, t)

# Função para calcular a derivada de P_d(t)
def dP(d, t):
    if d == 0:
        return 0  # P0'(t) é 0
    elif d == 1:
        return 1  # P1'(t) é 1
    else:
        if t == 1 or t == -1:  # Evitar divisão por zero
            return 0
        return (d / (1 - t**2)) * (P(d - 1, t) - t * P(d, t))

# Método de Newton-Raphson
def newtonRaphson(f, df, x0, tol=1e-6, maxIter=1000):
    x = x0
    for _ in range(maxIter):
        fx = f(x)
        dfx = df(x)
        if abs(dfx) < 1e-10:  # Evitar divisões por zero
            return None  # Não convergiu
        x_new = x - fx / dfx
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    return None  # Não convergiu

# Função para buscar raízes usando Newton-Raphson para diferentes valores de d (dias da semana)
def encontrar_raizes(d, chutes_iniciais):
    raizes_encontradas = set()
    for chute in chutes_iniciais:
        raiz = newtonRaphson(lambda t: P(d, t), lambda t: dP(d, t), chute)
        if raiz is not None and 0 <= raiz:  # Garantir que a raiz seja maior que 0
            raizes_encontradas.add(round(raiz, 6))  # Armazenar com precisão de 6 casas decimais
    return list(raizes_encontradas) if raizes_encontradas else 'Não há raízes'

# Testar chutes de t no intervalo 0 a 23 nos dá restultado de raízes entre 0 e 1 somente,
# Daí vem o gatilho de pegar raízes entre 0 e 1.
# Chutes iniciais para as raízes (agora valores entre 0 e 1)
chutes_iniciais = np.linspace(0, 1, 10)

# Dicionário para armazenar os resultados
raizes_dict = {'Dia da Semana': [], 'Raízes': []}

# Adicionando a informação para P0 (Domingo), que não possui raízes
raizes_dict['Dia da Semana'].append('Segunda-Feira')
raizes_dict['Raízes'].append('Não há raízes')

# Dias da semana e suas respectivas funções P_d(t)
dias_da_semana = ['Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado','Domingo']

# Encontrar raízes para os dias da semana de P1 a P6
for d, dia in enumerate(dias_da_semana, start=1):
    raizes_dict['Dia da Semana'].append(dia)
    raizes_dict['Raízes'].append(encontrar_raizes(d, chutes_iniciais))

# Criar tabela pandas
df_raizes = pd.DataFrame(raizes_dict)

# Exibir o DataFrame de forma padrão
print(df_raizes)