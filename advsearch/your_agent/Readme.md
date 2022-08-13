### Heurística CoinDifference
 - De acordo com o atual estado do tabuleiro, calcula a diferença de pontos entre o MAX e MIN, ela é mais eficiente no final do jogo, seguindo a fórmula abaixo:

- `(maxPlayerCoins - minPlayerCoins) / (maxPlayerCoins + minPlayerCoins)`


### Heurística Mobilidade 
- Tenta obter a diferença entre o número de movimentos possíveis para o MAX e MIN, com o objetivo de restringir a mobilidade do MIN e aumentar a mobilidade do MAX. A heurística é calculada seguindo a fórmula abaixo: 

```
if (maxPlayerMoves + minPlayerMoves )!= 0 :
            mobilityHeuristic = (maxPlayerMoves - minPlayerMoves) / (maxPlayerMoves + minPlayerMoves)
  else: mobilityHeuristic = 0
  
```

### Heurística Corners Captured
- Valoriza os cantos, pois eles são importantes para o desenvolvimento do jogo, uma vez capturados, não podem ser revertidos pelo adversário e permitem que o player construa moedas ao seu redor.

```
if (maxPlayerMoves + minPlayerMoves ) != 0:
    cornersCapturedHeuristc = (maxPlayerMoves - minPlayerMoves) / (maxPlayerMoves + minPlayerMoves)
else: cornersCapturedHeuristc = 0 

```

 ### Heurística Pesos Estáticos
 - O valor da heurística é calculada somando os pesos dos quadrados em que o player possui moedas, cada posição do tabuleiro possui um peso, e está
 Heurística encoraja o player a capturar os cantos.

````
[[120, -20, 20, 5, 5, 20, -20, 120]
[-20, -40, -5, -5, -5, -5, -40, -20]
[20, -5, 15, 3, 3, 15, -5, 20],
[5, -5, 3, 3, 3, 3, -5, 5],
[5, -5, 3, 3, 3, 3, -5, 5],
[20, -5, 15, 3, 3, 15, -5, 20],
[-20, -40, -5, -5, -5, -5, -40, -20]
[120, -20, 20, 5, 5, 20, -20, 120]]

````

### Pesos para as Heurística
Com as Heurística já definidas, para avaliar um estado, cada heuristica tem um determinado peso com base na quantidade de peças do jogo.
>> Início/Meio[4-40]: 1Mobility + 40CornersCaptured + 1StaticWeights (Foco na mobilidade e bom posicionamento)
>> Meio/Fim [40-54]: 4Mobility + 3CoinParity + 40CornersCaptured + 4StaticWeights (Foco em cantos e moedas)
>> Fim [54-64]: 1CoinParity (Foco em ganhar o jogo)

## Condição de Parada
Foi implementado uma poda Alfa-Beta com aprofundamento iterativo para encontrar a melhor jogada para o Agente. Inicialmente, o aprofundamento base é 3 ou 4 (depenendo da quantidade de peças do tabuleiro), porém enquanto tiver tempo restante (considerado os 5s base) a arvore continua incrementando em 1 sua profundidade. Então, a condição de parada é ou estado atual do tabueiro é um estado final ou a arvore atingiu a profundidade máxima naquele momento.

## Bibliografia
- https://www.ic.unicamp.br/~rocha/teaching/2011s2/mc906/seminarios/2011s2-mc906-seminario-04.pdf
- https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
    
