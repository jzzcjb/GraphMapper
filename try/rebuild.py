import graphviz
import re
import networkx as nx
import matplotlib.pyplot as plt
import csv
inputpath = './output/'
# inputpath = '../testcases/3host/'
class Node(object):
    def __init__(self, id = -1, data = "",shape = "", type = None, depth = 0, childnum = 0):
        self.id = id
        self.data = data
        self.shape = shape
        self.type = type
        self.score = []
        self.depth = depth
        self.cut = 0
        self.childnum = childnum
        self.children = []

Nodes = []
CVE_scores = {}

# def del_rules(x):
#     # print(x.id)
#     if(x.childnum == 0):
#         return
#     if(vis[x.id] == 1):
#         return
#     vis[x.id] = 1
#     for child in x.children:
#         if(child.type == True):
#             x.childnum += child.childnum
#             x.children.extend(child.children)
#     i=0
#     while i < x.childnum:
#         if x.children[i].type == True:
#             x.children.pop(i)
#             x.childnum -= 1
#             i -= 1
#         i += 1
#     # for child in x.children:
#     #     print("son",child.id, child.type)
#     for child in x.children:
#         del_rules(child)

def calc_depth(x):
    # print(x.id, x.data, x.score)
    if(x.childnum == 0):
        x.depth = 0
        return
    if(vis[x.id] == 1):
        return
    vis[x.id] = 1
    for child in x.children:
        calc_depth(child)
        # print("fa", x.id, "son", child.id, "change? ",child.depth+1, x.depth)
        if(child.depth+1>x.depth):
            x.depth = child.depth+1
    # for child in x.children:
        

def merge_attack_cost(x=[], y=[], op = ''):
    # print(x,y,op)
    if(len(x) == 0):
        return y
    if(len(y) == 0):
        return x
    if(op=='OR'):
        z = []
        z.extend(x)
        z.extend(y)
        z = [round(i,2) for i in z]
        return list(set(z))
    if(op=='AND'):
        z = []
        for xx in x:
            for yy in y:
                z.append(xx+yy)
        z = [round(i,2) for i in z]
        return list(set(z))

def merge_block_cost(x, y, op = ''):
    # print(x,y)
    if(x == 0):
        return y
    if(y == 0):
        return x
    if(op=='OR'):
        return x+y
    if(op=='AND'):
        return min(x,y)

def calc_attack_cost(x):
    # print(x.id, x.depth, x.score)
    if(x.childnum == 0):
        return
    if(vis[x.id] == 1):
        return
    vis[x.id] = 1
    for child in x.children:
        if(child.shape == 'LEAF'):
            # print(x.id, x.data, x.depth, x.score)
            if(len(child.score)>0):
                child.score[0] = round(child.score[0]*x.depth, 4)
                
        else:
            calc_attack_cost(child)
        x.score = merge_attack_cost(x.score, child.score, x.shape)
        
def calc_block_cost(x):
    if(x.childnum == 0):
        if(len(x.score)>0):
            x.cut = x.score[0]
        return
    if(vis[x.id] == 1):
        return
    vis[x.id] = 1
    for child in x.children:
        calc_block_cost(child)
        x.cut = merge_block_cost(x.cut, child.cut, x.shape)
        

def print_tree(x):
    print(x.id, x.data, x.depth, len(x.score), x.score)
    if(x.childnum == 0):
        return
    if(vis[x.id] == 1):
        return
    vis[x.id] = 1
    for child in x.children:
        print_tree(child)

def write_attack_cost2dot():
    f = open("attack_cost.dot", "w")
    S = "digraph G {\n"
    f.write(S)
    maxx = 0
    minn = 100100
    var = 0
    aver = 0
    for val in Nodes[0].score:
        if(val>maxx):
            maxx = val
        if(val<minn):
            minn = val
        aver += val
    aver = round(float(aver/len(Nodes[0].score)),4)
    for val in Nodes[0].score:
        var += (val-aver)*(val-aver)
    var = round(float(var/len(Nodes[0].score)),4)
    S = '\t0 [label="Attack cost:'+chr(92)+'nmax ='+str(maxx)+chr(92)+'nmin ='+str(minn)+chr(92)+ 'naver ='+str(aver)+chr(92)+'nvar ='+str(var)+chr(92)+'n'+str(len(Nodes[0].score))+' ways in total'+'",shape=ellipse];\n'
    f.write(S)
    for x in Nodes:
        if(x.shape == 'OR'):
            shape = 'diamond'
        elif(x.shape == 'AND'):
            shape = 'ellipse'
        else:
            shape = 'box'
        S = '\t'+str(x.id)+' [label="'+str(x.id)+':'+x.data+':'+str(int(x.shape == 'LEAF'))+'",shape='+shape+"];\n"
        f.write(S)
    S = '\t'+str(Nodes[0].id)+' -> 0 ;\n'
    f.write(S)
    for x in Nodes:
        for child in x.children:
            # if(child.shape == 'LEAF'):
            #     S = '\t'+str(child.id)+' -> '+str(x.id)+' [label="'+str(len(child.score))+'*'+str(x.depth)+'"];\n'
            # else:
            #     S = '\t'+str(child.id)+' -> '+str(x.id)+' [label='+str(len(child.score))+'];\n'
            if(len(child.score)>0):
                S = '\t'+str(child.id)+' -> '+str(x.id)+' [label="'+str(child.score)+'"];\n'
            else:
                S = '\t'+str(child.id)+' -> '+str(x.id)+';\n'
            f.write(S)
    
    S = "}\n"
    f.write(S)
    f.close()
    print("Write to file done!")

def write_block_cost2dot():
    f = open("block_cost.dot", "w")
    S = "digraph G {\n"
    f.write(S)
    S = '\t0 [label="Block cost:'+str(Nodes[0].cut)+'",shape=ellipse];\n'
    f.write(S)
    for x in Nodes:
        if(x.shape == 'OR'):
            shape = 'diamond'
        elif(x.shape == 'AND'):
            shape = 'ellipse'
        else:
            shape = 'box'
        S = '\t'+str(x.id)+' [label="'+str(x.id)+':'+x.data+chr(92)+'n'+str(x.shape)+'",shape='+shape+"];\n"
        f.write(S)
    S = '\t'+str(Nodes[0].id)+' -> 0 ;\n'
    f.write(S)
    for x in Nodes:
        for child in x.children:
            if(len(child.score)>0):
                S = '\t'+str(child.id)+' -> '+str(x.id)+' [label="'+str(child.cut)+'"];\n'
            else:
                S = '\t'+str(child.id)+' -> '+str(x.id)+';\n'
            f.write(S)
    
    S = "}\n"
    f.write(S)
    f.close()
    print("Write to file done!")
def load_CVEs():
    t = open("./cvss.csv", "r")
    lines = csv.reader(t)
    for line in lines:
        CVE_scores[line[0]]=line[1]
    t.close()


def load_vertices():
    f = open(inputpath+"VERTICES.CSV", "r")
    res = f.readlines()
    for line in res:
        # 匹配所有双引号内的内容
        pattern = re.compile(r'"(.*?)"')
        result = re.findall(pattern, line)
        type = re.match("RULE", result[0])

        pattern = r'\d+'
        number = re.match(pattern,line).group()
        res = []
        if(re.match('vulExists', result[0])):
            pattern = re.compile(r"'(.*?)'")
            res = re.findall(pattern, result[0])
        if(len(res)>0):
            if(res[0]!='CAN-2002-0392'):
                score = CVE_scores[res[0]]
                node = Node(int(number), result[0], result[1], type!=None)
                node.score.append(float(score))
        else:
            node = Node(int(number), result[0], result[1], type!=None)
        # print(node.id,node.type)
        Nodes.append(node)
    f.close()

def load_arcs():
    f = open(inputpath+"ARCS.CSV", "r")
    res = f.readlines()
    for line in res:
        pattern = re.compile(r',')
        res = re.split(pattern, line)
        father = Nodes[int(res[0])-1]
        son = Nodes[int(res[1])-1]
        father.children.append(son)
        father.childnum += 1
        # print("son, father, father.child_size",son.id, father.id,len(father.children))
    f.close()

load_CVEs()
load_vertices()
load_arcs()
# vis = [0]*(len(Nodes)+1)
# del_rules(Nodes[0])
vis = [0]*(len(Nodes)+1)
calc_depth(Nodes[0])
vis = [0]*(len(Nodes)+1)
calc_attack_cost(Nodes[0])

# vis = [0]*(len(Nodes)+1)
# print_tree(Nodes[0])
write_attack_cost2dot()
vis = [0]*(len(Nodes)+1)
calc_block_cost(Nodes[0])
write_block_cost2dot()


# dot -Tps attack_cost.dot > attack_cost.eps
# dot -Tps block_cost.dot > block_cost.eps
# epstopdf attack_cost.eps