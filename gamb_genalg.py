import random
import pandas as pd
import numpy as np
import math


# Define a classe disciplina com ID, Área e Quantidade de Créditos
class Disciplina:

    def __init__(self, cod: str, tipo: str, cred: int):
        self.id = cod
        self.tipo = tipo
        self.cred = cred


# Define a classe período com uma lista de disciplinas
class Periodo:

    def __init__(self, disciplinas: list = []):
        self.disciplinas = disciplinas
        self.qnt_disc = len(disciplinas)
        self.variedade = 0
        tot_cred = 0
        f_tipos = ''
        for DISC in self.disciplinas:
            tot_cred += DISC.cred
            f_tipos += DISC.tipo
        self.tot_cred = tot_cred
        if len(f_tipos) != 0:
            self.variedade = len("".join(dict.fromkeys(f_tipos))) / len(f_tipos)
        self.med_cred = self.tot_cred/self.qnt_disc if self.qnt_disc != 0 else 0

    def add_disc(self, disciplinas: list):
        for DISC in disciplinas:
            self.disciplinas.append(DISC)


# Define a classe Grade com uma lista de 10 períodos (conforme a Engenharia Ambiental no CEFET)
class Grade:

    def __init__(self, periodos: list = []):
        self.periodos = periodos
        self.valido = True
        self.pts_var = 0
        self.pts_ch = 0
        self.pts_tot = 0

    def pontuacao(self):
        soma_var = 0
        soma_cred = 0
        for period in self.periodos:
            soma_var += period.variedade
            soma_cred += period.med_cred
        media_creditos = soma_cred/10
        self.pts_var = soma_var/10
        self.pts_ch = (1 - (abs((media_creditos - 3)/3)))
        self.pts_tot = 2/(self.pts_var**(-1) + self.pts_ch**(-1))

    def exibir(self):
        CONT = 0
        for period in self.periodos:
            CONT += 1
            pre_df = {"IDs": [], "Creditos": []}
            for DISC in period.disciplinas:
                pre_df["IDs"].append(DISC.id)
                pre_df["Creditos"].append(DISC.cred)

            df = pd.DataFrame(pre_df)
            print(f'----- {CONT}° Periodo -----')
            print(df)

    def add_period(self, periodo: Periodo):
        self.periodos.append(periodo)

    def invalidar(self):
        self.valido = False

    def mostrar_pontos(self):
        print(f'Pontuação por Variedade: {self.pts_var * 100}% \n'
              f'Pontuação por Carga Horária: {self.pts_ch * 100}% \n'
              f'Pontuação Total: {self.pts_tot * 100}%')


# Tipos de Disciplina:
# H - Humanas
# B - Biologia
# Q - Quimica
# M - Matematica
# F - Fisica
# C - Computacao
# D - Desenho
# A - Ambiental
# E - Estagio
# P - Projeto Final
# T - Horas Complementares
lista_disc = [

    ['CalcI', 'M', 5], ['AlgI', 'M', 2], ['Des', 'D', 4], ['QuimIn', 'Q', 4],
    ['BioAmb', 'B', 4], ['Intro', 'A', 2], ['Comp', 'C', 3], ['CalcII', 'M', 4],
    ['AlgII', 'M', 3], ['QuimOrg', 'Q', 3], ['MecBas', 'F', 4], ['Metod', 'H', 2],
    ['Eco', 'B', 2], ['DesTec', 'D', 3], ['ExpOE', 'H', 2], ['EDO', 'M', 4],
    ['CalVet', 'M', 2], ['MecGer', 'F', 3], ['EltBas', 'F', 4], ['QuimAmb', 'Q', 4],
    ['Estat', 'M', 3], ['Adm', 'H', 2], ['EDPS', 'M', 3], ['FES', 'H', 3],
    ['FisTer', 'F', 3], ['ResMat', 'F', 3], ['Econ', 'H', 2], ['TopGeo', 'D', 3],
    ['CalNum', 'M', 3], ['Geo', 'A', 3], ['FeTrans', 'F', 3], ['BioQuim', 'Q', 4],
    ['HCS', 'H', 2], ['GesQua', 'H', 3], ['CartGeo', 'D', 3], ['CPI', 'A', 4],
    ['SanSau', 'A', 3], ['MecSolo', 'F', 4], ['RecHid', 'A', 4], ['Micro', 'B', 4],
    ['RSU', 'A', 3], ['CPII', 'A', 4], ['RNCE', 'A', 4], ['AnFiQiI', 'Q', 3],
    ['ModAmb', 'C', 3], ['AnMicro', 'B', 3], ['Hidra', 'F', 4], ['Abast', 'A', 3],
    ['Esgoto', 'A', 3], ['FPI', 'Q', 3], ['AnFiQiII', 'Q', 3], ['TratRS', 'A', 3],
    ['SisDren', 'A', 3], ['TratAgu', 'A', 4], ['TratEfl', 'A', 4], ['PlanAmb', 'A', 4],
    ['Estagio', 'E', 7], ['GesAmbI', 'A', 4], ['LegAmb', 'A', 4], ['TCCI', 'P', 2],
    ['GesAmbII', 'A', 4], ['RiscAmb', 'A', 4], ['TCCII', 'P', 2], ['AC', 'T', 0]

]

# Lista com disciplinas convertidas para o formato de objeto
lista_disc_obj = [Disciplina(disc[0], disc[1], disc[2]) for disc in lista_disc]


# Funcao de criacao de populacao
def popular(tam: int):
    populacao = []
    for i in range(tam):
        individuo = []
        for j in range(10):
            individuo.append([])
        for disciplina in lista_disc_obj:
            random.choice(individuo).append(disciplina)
        periodos = []
        for peri in individuo:
            periodos.append(Periodo(peri))
        indv_fin = Grade(periodos)
        populacao.append(indv_fin)
    return populacao


# Funcao de selecao por pontuacao total
def selecionar(populacao: list):
    for individuo in populacao:
        for gene in individuo.periodos:
            if gene.qnt_disc > 9:
                individuo.invalidar()
            else:
                individuo.pontuacao()
    ranking = sorted(populacao, key=lambda x: x.pts_tot, reverse=True)
    while len(ranking) > 20:
        ranking.remove(ranking[-1])
    return ranking


# Funcao de cruzamento a nível gene
def cruzamento_por_gene(grupo: list):
    maes = grupo[:10]
    pais = grupo[10:]
    filhos = []
    for i in maes:
        for j in pais:
            feto = []
            for counter in range(0, 10, 2):
                feto.append(i.periodos[counter])
                feto.append(j.periodos[counter + 1])
            filhos.append(Grade(feto))
    return filhos


# Zona de Teste
pop = popular(100)
cont = 1

for amt in range(200):
    print(f'------- Geração n°{amt + 1} -------')
    selec = selecionar(pop)
    crux = cruzamento_por_gene(selec)
    pop = crux

for indv in selec:
    print(f'------ Grade nº{cont} ------')
    indv.mostrar_pontos()
    print('-' * 20)
    cont += 1

selec[0].exibir()




