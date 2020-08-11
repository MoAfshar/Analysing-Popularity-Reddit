import networkx as nx
import csv 
import pandas as pd 
import numpy as np
import collections
import matplotlib.pyplot as plt

def createEdgePath():
	sub = pd.read_csv("submissions.csv")

	edge_list = []
	for i in range(1, len(sub)):
		if(sub.loc[i, 'imageNum'] == sub.loc[i-1, 'imageNum']): 
			edge_list.append(tuple((sub.loc[i-1, 'id'], sub.loc[i, 'id'])))

	#get rid of self loops for rich club coeffecient 
	j = 0
	while(j < len(edge_list)):
		if(edge_list[j][0] == edge_list[j][1]): 
			edge_list.pop(j)
		else: 
			j += 1
	#print(edge_list)
	return edge_list

def createNodes(): 
	sub = pd.read_csv("submissions.csv")

	node_list = []
	for i in range(0, len(sub)):
		if(sub.loc[i, 'id'] not in node_list):
			node_list.append(sub.loc[i, 'id'])
	#print(len(node_list))
	return node_list

#Graph cannot have any self loops and cannot be directed
def computeRichClubCoefficient(G):
	d = nx.rich_club_coefficient(G, normalized=False)
	e = nx.rich_club_coefficient(G)
	d_Val = sorted(set(d.keys()))
	plt.figure()
	plt.ticklabel_format(axis='y', style='sci', scilimits=(0,5))
	plt.plot(list(d.keys()), list(d.values()), 'ro-')
	plt.plot(list(e.keys()), list(e.values()), 'bx-')
	plt.legend(['Before Normalization','Normalized'])
	plt.xlabel('degree')
	plt.ylabel('Rich Club Coefficient')
	plt.title('Reddit Resubmission Network')
	plt.show()
	plt.savefig('richclub2.jpg')

def computeAssortativity(G): 
	r = nx.degree_assortativity_coefficient(G) #= -0.0326169173416, more towards neutral mixing 
	print(r)

#Graph needs to be directed 
def computeInandOutDegree(G):
	list_of_in = G.in_degree() 
	in_degrees = dict(list_of_in) # dictionary node:degree
	in_values = sorted(set(in_degrees.values()))
	in_hist = [list(in_degrees.values()).count(x)/len(G.in_degree()) for x in in_values]
	list_of_out = G.out_degree() 
	out_degrees = dict(list_of_out) 
	out_values = sorted(set(out_degrees.values()))
	out_hist = [list(out_degrees.values()).count(x)/len(G.out_degree()) for x in out_values]
	plt.figure()
	plt.ticklabel_format(axis='y', style='sci', scilimits=(0,5))
	plt.loglog(in_values, in_hist,'ro-') # in-degree
	plt.loglog(out_values, out_hist,'bv-') # out-degree
	plt.legend(['In-degree','Out-degree'])
	plt.xlabel('log(in and out Degree)')
	plt.ylabel('log(Number of nodes)')
	plt.title('Reddit Resubmission Network')
	plt.show()
	plt.savefig('RedditInandOut.jpg')

def degreePlot(G): 
	d = dict(G.degree())
	k_degree = sorted(set(d.values()))
	k_nodes = [list(d.values()).count(x)/len(G.degree()) for x in k_degree]
	plt.figure()
	plt.ticklabel_format(axis='y', style='sci')
	plt.loglog(k_degree, k_nodes,'bo-')
	plt.xlabel('log(Number of nodes with k links)')
	plt.ylabel('log(p(k))')
	plt.title('Reddit Resubmission Network')
	plt.show()
	plt.savefig('degreePlot.jpg')

def avgNeighbourDegree(G):
	data = {}
	for n in G.nodes():
		#Get rid of nodes which have a degree 0
		if G.degree(n):
			data[n] = float(sum(G.degree(i) for i in G[n]))/G.degree(n)

	od = collections.OrderedDict(sorted(data.items()))	
	result = {}
	node_list = G.nodes()

	for key, value in od.items():
		result[G.degree(key)] = value 

				
	fig = plt.figure()
	plt.plot(list(result.keys()), list(result.values()), 'bx-')
	plt.title('Degree correlation measured by nearest neighbours average degree')
	plt.xlabel('Node degree')
	plt.ylabel('Nearest neighbours average degree')
	fig.savefig('avgNeighbour.jpg')
	plt.show()


def writeOutInAndOutDegree():
	list_of_in = G.out_degree() 
	in_degrees = dict(list_of_in) # dictionary node:degree
	with open('outVal.csv','w', newline='') as out:
	    	csv_out = csv.writer(out)
	    	csv_out.writerow(['id','out_degree'])
	    	for row in in_degrees.items():
	        	csv_out.writerow(row)

	
G = nx.Graph() #Undreicted Graph
#G = nx.DiGraph() #Directed Graph
G.add_edges_from(createEdgePath())
G.add_nodes_from(createNodes())
print("Finished Initialising the Graph")

#Run different types of analysis
computeRichClubCoefficient(G)
#computeInandOutDegree(G)
#createNodes()
#avgNeighbourDegree(G)
#degreePlot(G)
