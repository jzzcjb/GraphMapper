import networkx as nx
import matplotlib.pyplot as plt
import csv
import os
import re
import random

import matplotlib.pyplot as plt

pointList = ['A','B','C','D','E','F','G']
linkList = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('E', 'F'), ('F', 'G'),]

CVEs = []
def load_CVEs():
    H = os.walk("../dataset/cvss_dataset")
    t = open("./cvss.csv","w")
    for path, dir_list, file_list in H:
        for file_name in file_list[1:2]:
            file = open(path+'/'+file_name,"r")
            lines = csv.reader(file)
            next(lines)
            for line in lines:
                CVEs.append(line[0])
                t.write(line[0]+','+line[4]+'\n')
    t.close()

load_CVEs()
f = open("./output/input.P",'w')
H = os.walk("../dataset/graph_topologyzoo/sources")
Nodes = []
G = nx.DiGraph()
for path, dir_list, file_list in H:
    for file_name in file_list[1:2]:   ##################
        Graph = nx.read_graphml(path+'/'+file_name)
        for i in Graph.nodes:
            Nodes.append(i+file_name[0:5])
            G.add_node(i)
    attackerLocated = Nodes[0]
    attackGoal = Nodes[len(Nodes)-1]
    CVE = CVEs[int(random.random()*len(CVEs))]
    f.write('attackerLocated(internet).\n')
    f.write('attackGoal(execCode('+attackGoal+',_)).\n\n')
    f.write('networkServiceInfo(fileServer, mountd, rpc, 100005, root).\n')
    f.write("nfsExportInfo(fileServer, '/export', _anyAccess, "+attackerLocated+').\n')
    f.write("nfsExportInfo(fileServer, '/export', _anyAccess, webServer).\n")
    f.write("vulExists(fileServer, '"+CVE+"', mountd).\n")
    f.write("vulProperty('"+CVE+"', remoteExploit, privEscalation).\n")
    f.write("localFileProtection(fileServer, root, _, _).\n\n")
    f.write("vulExists(webServer, 'CAN-2002-0392', httpd).\n")
    f.write("vulProperty('CAN-2002-0392', remoteExploit, privEscalation).\n")
    f.write("networkServiceInfo(webServer , httpd, tcp , 80 , apache).\n\n")
    f.write("nfsMounted("+attackerLocated+", '/usr/local/share', fileServer, '/export', read).\n\n")
    f.write("hacl(internet, webServer, tcp, 80).\n")
    f.write("hacl(webServer, _,  _, _).\n")
    f.write("hacl(fileServer, webServer, _, _).\n")
    f.write("hacl(fileServer, "+attackerLocated+", _, _).\n")
    for file_name in file_list[1:2]:   ##################
        Graph = nx.read_graphml(path+'/'+file_name)
        for j in Graph.edges:
            G.add_edge(j[0], j[1])
            hcl="hacl("+j[0]+file_name[0:5]+","+j[1]+file_name[0:5]+",tcp,80).\n"
            f.write(hcl)
pos = nx.circular_layout(G)
# nx.draw_networkx(G, pos=pos, with_labels=True)
# plt.show()




for node in Nodes:
    f.write('networkServiceInfo('+node+',httpd,tcp,80,root).\n')
for node in Nodes:
    CVE = CVEs[int(random.random()*len(CVEs))]
    f.write("\nvulProperty('"+CVE+"', remoteExploit, privEscalation).\n")
    f.write("vulExists("+node+", '"+CVE+"', _).\n")

print("OKOK")



f.close()

# cd ./output
# graph_gen.sh input.P -v -p
