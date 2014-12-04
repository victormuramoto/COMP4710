V = list()

def knapsack(vi, wi, n, W):
	V.append([0]*W)
	for i in range(1,n):
		V.append([0]*W)
		for j in range(W)
			if(wi[j] <= j)
			
# argumentos para a DP:
# - eliminar todos os itens de L que contenham alguma carta que não pertença ao deck
# - peso da mochila é igual à quantidade de cartas inseridas
# - V será medido pela radiciação de grau igual a quantidade de itemsets sobre o valor da 
# multiplicação do support de cada itemset envolvido.
# - o resultado da D.P. dará o valor da sinergia / coerência do Deck.