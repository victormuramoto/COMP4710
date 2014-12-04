V = list()
def knapsack(vi, wi, n, W):
	V.append([0]*W)
	for i in range(1,n):
		