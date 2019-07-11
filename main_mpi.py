import sys
import os
from mpi4py import MPI
import timeit 
from datetime import datetime

nmax = 4000000 #Número máximo hasta el que queremos buscar primos
inputs = range(0, nmax)


def isPrime(num):
    if num < 1:
        return [num,False]
    elif num == 2:
        return [num,True]
    else:
        for i in range(2, num):
            if num % i == 0:
                return [num,False]
        return [num,True]


if __name__ == "__main__":

	starTime= timeit.default_timer()
	
	comm = MPI.COMM_WORLD
	size = comm.Get_size()
	rank = comm.Get_rank()



	if rank == 0:
	
		chunks = [[] for _ in range(size)]
		for i, chunk in enumerate(inputs):
			chunks[i % size].append(chunk)		
		timeFlag = datetime.now().strftime("%Y%m%d%H%M%S") 


	else:
		#data = None
		chunks = None
		timeFlag = None	


	data = comm.scatter(chunks, root=0)

	print ('rank %s recibidos %s' % (rank, len(data)))


	lista = [isPrime(d) for d in data]


	lista = comm.gather(lista, root=0)

	# Checking all process have finished
	if rank == 0:
		listaT = []
		for r in range(size):			
			listaT += [number[0] for number in lista[r] if number[1] ]

		

		print ('encontrados %s primos...' % len(listaT))
	