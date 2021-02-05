import math
import numpy as np
import pandas as pd

from ortools.linear_solver import pywraplp

def otimizar_filas(hs,
                   vs,
                   hc,
                   vc,
                   m,
                   n, #LISTA COM LARGURAS DOS CORREDORES VERTICAIS
                   dmin):
  #PAINEL DE CONTROLE
  #hs = 10 #largura da sala
  #vs = 7 #comprimento da sala

  #hc = 0.5 #largura da cadeira
  #vc = 0.5 #comprimento da cadeira

  vr = (vs-m*vc)/(m) #comprimento do corredor horizontal

  #dmin = 1 #ditancia minima entre pessoas

  #CALCULO DOS PARAMETROS
  cadeiras = []
  coordenada_y = 0
  for j in range(m):
    if j > 0: 
      coordenada_y += vc + vr
    coordenada_x = 0
    for i in (range(len(n)+1)):
      if i > 0:
        coordenada_x = coordenada_x + hc + n[i-1]
      cadeira = {
          'id' : j*(len(n)+1)+i,
          'fileira' : i+1,
          'cadeira' : j+1,
          'x' : coordenada_x,   #coordenadas consideradas do canto superior
          'y' : coordenada_y    #esquerdo do retangulo de ocupacao do aluno
      }
      cadeiras.append(cadeira)
  print(pd.DataFrame(cadeiras))

  #print("Tabela de nao adjacencia entre as cadeiras da sala:")
  nao_adjacencia = []
  for cadeira_l in cadeiras:
    for cadeira_k in cadeiras:
      if cadeira_l['id'] < cadeira_k['id']:
        if math.sqrt((cadeira_l['x']-cadeira_k['x'])**2+(cadeira_l['y']-cadeira_k['y'])**2) < dmin:
          nao_vizinho = {
              'id_cadeira_1' : cadeira_l['id'],
              'id_cadeira_k' : cadeira_k['id'],
              'distancia' : math.sqrt((cadeira_l['x']-cadeira_k['x'])**2+
                                      (cadeira_l['y']-cadeira_k['y'])**2)
          }
          nao_adjacencia.append(nao_vizinho)
  #print(pd.DataFrame(nao_adjacencia))


  # [START solver]
  # Create the mip solver with the CBC backend.
  solver = pywraplp.Solver('otimizacao_fileiras',
                            pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  # [END solver]

  # [START variables]
  # x binary integer variable.
  x = {}
  for cadeira in cadeiras:
    x[cadeira['id']] = solver.BoolVar('x[%i]' % cadeira['id'])

  print('Numero de variaveis =', solver.NumVariables())
  # [END variables]

  # [START constraints]
  # x_{l}\cdot (1-\Delta_{l,k})\leq 1 - x_{k}
  for cadeira_l in cadeiras:
    for cadeira_k in cadeiras:
      if cadeira_l['id'] != cadeira_k['id']:
        if math.sqrt((cadeira_l['x']-cadeira_k['x'])**2+(cadeira_l['y']-cadeira_k['y'])**2) < dmin:
          solver.Add(x[cadeira_l['id']] + x[cadeira_k['id']] <= 1)

  print('Numero de restricoes =', solver.NumConstraints())
  # [END constraints]

  # [START objective]
  # Maximize \sum\limits_{l\in L}x_l
  solver.Maximize(solver.Sum(x[cadeira['id']] for cadeira in cadeiras))
  # [END objective]

  # [START solve]
  status = solver.Solve()
  # [END solve]

  # [START print_solution]
  if status == pywraplp.Solver.OPTIMAL:
      print('Solucao:')
      print('Funcao objetivo =', solver.Objective().Value())
      resposta = []
      for l in range(solver.NumVariables()):
        resposta.append(x[l].solution_value())
      resposta = np.reshape(resposta,(m,(len(n)+1)))
      return {'status' : 1,
              'num_alunos' : solver.Objective().Value(),
              'num_fileiras' : (len(n)+1),
              'num_carteiras' : m,
              "largura_corredores_verticais": n,
 	            "largura_corredor_horizontal": vr,
              'resposta' : resposta.T.tolist(),
              'tempo_resolucao' : solver.wall_time(),
              'num_iteracoes' : solver.iterations(),
              'num_nodes' : solver.nodes()}
  else:
      return {'status' : 0,
              'resposta':'O problema nao tem solucao otima.'}
  # [END print_solution]

  # [START advanced]
  #print('\nEstatistica de resolucao:')
  #print('Problema resolvido em %f milisegundos' % solver.wall_time())
  #print('Problema resolvido em %d iteracoes' % solver.iterations())
  #print('Problema resolvido em %d nos do branch-and-bound' % solver.nodes())
  # [END advanced]

def otimizar_distancia(hs,
                        vs,
                        hc,
                        vc,
                        m,
                        n, #LISTA COM LARGURAS DOS CORREDORES VERTICAIS
                        num_alunos):
  #PAINEL DE CONTROLE
  #hs = 10 #largura da sala
  #vs = 7 #comprimento da sala

  #hc = 0.5 #largura da cadeira
  #vc = 0.5 #comprimento da cadeira

  vr = (vs-m*vc)/(m) #comprimento do corredor horizontal

  #dmin = 1 #ditancia minima entre pessoas

  #CALCULO DOS PARAMETROS
  cadeiras = []
  coordenada_y = 0
  for j in range(m):
    if j > 0: 
      coordenada_y += vc + vr
    coordenada_x = 0
    for i in (range(len(n)+1)):
      if i > 0:
        coordenada_x = coordenada_x + hc + n[i-1]
      cadeira = {
          'id' : j*(len(n)+1)+i,
          'fileira' : i+1,
          'cadeira' : j+1,
          'x' : coordenada_x,   #coordenadas consideradas do canto superior
          'y' : coordenada_y    #esquerdo do retangulo de ocupacao do aluno
      }
      cadeiras.append(cadeira)
  #print(pd.DataFrame(cadeiras))
  
  M = 0.0

  distancias = {}
  for cadeira_l in cadeiras:
    for cadeira_k in cadeiras:
      if cadeira_l['id'] < cadeira_k['id']:
        distancia = {
            'id_cadeira_1' : cadeira_l['id'],
            'id_cadeira_k' : cadeira_k['id'],
            'distancia' : math.sqrt((cadeira_l['x']-cadeira_k['x'])**2+
                                    (cadeira_l['y']-cadeira_k['y'])**2)
        }
        if distancia['distancia'] > M:
          M = distancia['distancia']
        if cadeira_l['id'] in distancias:
          distancias[cadeira_l['id']][cadeira_k['id']] = distancia['distancia']
        else:
          distancias[cadeira_l['id']] = {}
          distancias[cadeira_l['id']][cadeira_k['id']] = distancia['distancia']
    
  #GARANTIA
  M += 1

  # [START solver]
  # Create the mip solver with the CBC backend.
  solver = pywraplp.Solver('otimizacao_distancias',
                            pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
  # [END solver]
  # [START variables]
  # x binary integer variable.
  x = {}
  for cadeira in cadeiras:
    x[cadeira['id']] = solver.BoolVar('x[%i]' % cadeira['id'])

  r = solver.NumVar(0.0, M, 'r')
  print('Numero de variaveis =', solver.NumVariables())
  # [END variables]
  # [START constraints]
  for cadeira_l in cadeiras:
    for cadeira_k in cadeiras:
      if cadeira_l['id'] < cadeira_k['id']:
        solver.Add(M*(2-x[cadeira_l['id']] -x[cadeira_k['id']]) + distancias[cadeira_l['id']][cadeira_k['id']] - r >= 0)
  solver.Add(solver.Sum(x[cadeira['id']] for cadeira in cadeiras) == num_alunos)
  
  print('Numero de restricoes =', solver.NumConstraints())
  # [END constraints]
  # [START objective]
  # Maximize \sum\limits_{l\in L}x_l
  solver.Maximize(r)
  # [END objective]

  # [START solve]
  status = solver.Solve()
  # [END solve]

  # [START print_solution]
  if status == pywraplp.Solver.OPTIMAL:
      print('Solucao:')
      print('Funcao objetivo =', solver.Objective().Value())
      resposta = []
      for l in range(len(x)):
        resposta.append(x[l].solution_value())
      resposta = np.reshape(resposta,(m,(len(n)+1)))
      return {'status' : 1,
              'distancia_minima' : solver.Objective().Value(),
              'numero_alunos' : num_alunos,
              'num_fileiras' : (len(n)+1),
              'num_carteiras' : m,
              "largura_corredores_verticais": n,
 	            "largura_corredor_horizontal": vr,
              'resposta' : resposta.T.tolist(),
              'tempo_resolucao' : solver.wall_time(),
              'num_iteracoes' : solver.iterations(),
              'num_nodes' : solver.nodes()}
  else:
      return {'status' : 0,
              'resposta':'O problema nao tem solucao otima.'}
  # [END print_solution]

  # [START advanced]
  #print('\nEstatistica de resolucao:')
  #print('Problema resolvido em %f milisegundos' % solver.wall_time())
  #print('Problema resolvido em %d iteracoes' % solver.iterations())
  #print('Problema resolvido em %d nos do branch-and-bound' % solver.nodes())
  # [END advanced]

def main():
  hs = 10
  vs = 7
  hc = 0.5
  vc = 0.5
  m = 6
  n = [1,2,1,1,2,1]
  #dmin = 1.0
  num_alunos = 20
  #print(otimizar_filas(hs,vs,hc,vc,m,n, dmin))
  print(otimizar_distancia(hs,vs,hc,vc,m,n, num_alunos))
  
if __name__ == "__main__":
  main()