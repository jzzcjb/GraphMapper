import networkx as nx
import matplotlib.pyplot as plt
import sys

graph_name = sys.argv[1]
G = nx.read_graphml(graph_name)
f = open("out.txt",'w')
for j in G.edges:
    # print(j)
    #hacl(internet, webServer, tcp, 80).
    hcl="hcl("+j[0]+","+j[1]+",tcp,80)\n"
    f.write(hcl)
f.close()
# nx.draw(G)
# plt.show()
