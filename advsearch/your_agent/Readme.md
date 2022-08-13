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

    
