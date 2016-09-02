import csv
import sys
import itertools
import math

alist=[]  # list for rules

def read_config():
    dic = dict()
    config = open('config.csv', 'rt')
    try:
        reader = csv.reader(config)
        for row in reader:
            dic[row[0]]= row[1]
    finally:
        config.close()
    
    return dic



dic = read_config() #dic contains config.csv input parameters
f = open(dic['input'])
count=0
for row in f:
    count+=1

records = float(count)          # transaction id's count
minsup = float(dic['support'])      #min support 
minsup=math.ceil(minsup*records)
conf = float(dic['confidence'])     #confidence value
   
sys.stdout = open(dic['output'], 'w')


class TrieNode:
    #data structure of node in Trie
    def __init__(self,val,count):
        self.val = val
        self.count=count
        self.pointers = {}

    #adding node to the Trie
        
    def addelement(self,itemlist,count):
        if itemlist[0] not in self.pointers:
            newNode = TrieNode(itemlist[0],count)
            self.pointers[itemlist[0]] = newNode
        else:
             self.pointers[itemlist[0]].addelement(itemlist[1:],count)

    #returns count of some item list
             
    def count_item(self,lis):
        if len(lis) == 1:
            return self.pointers[lis[0]].count
        else:
            return self.pointers[lis[0]].count_item(lis[1:])

    #returns true if itemlist is present
        
    def search(self,itemlist):
        if len(itemlist)==0:
            return True
        elif itemlist[0] not in self.pointers:
            return False
        else:
            return self.pointers[itemlist[0]].search(itemlist[1:])

    # print frequent itemsets
    
    def print_trie(self,lis):
        if len(self.pointers)==0:
            return
        for i in self.pointers:
            m = lis + [i]
            print (',').join(m)
            self.pointers[i].print_trie(m)



#print rules
def print_rules(r,lis):
    if len(r.pointers)==0:
        return
    for i in r.pointers:
        m = lis + [i]
        alist.append(m)
        print_rules(r.pointers[i],m)
            
        
            

def rules(r):
    print_rules(r,[])
    x=[]
    for i in alist:
        icount = r.count_item(i)
        for j in range(1,len(i)):
            for k in itertools.combinations(i,j):
                if float(float(icount)/float(r.count_item(k)))>=conf:
                    x.append((',').join(k)+'=>'+(',').join(set(i)-set(k)))

    print len(x)    
    for i in x:
        print i


def freq_list(lis,k):           #generating the frequent item list and return its counts
    d = [0 for j in range(0,len(lis))]
    f = open(dic['input'])
    for tid in f:
        tid = tid.strip().split(",")
        for key in lis:
            if set(key).issubset(set(tid)):
                d[lis.index(key)]=d[lis.index(key)]+1  


     
    l1=[]            
    d1=[]
    for i in lis:
        if d[lis.index(i)] >= minsup:
            l1.append(i)
            d1.append(d[lis.index(i)])
    if k==1:
        l1.sort()
    return l1,d1
    

#generate list of 1 length item sets
def gen_list():
    lis=[]
    f = open(dic['input'])
    for i in f:
        i = i.strip().split(",")
        for j in i:
            if [j] not in lis:
                lis.append([j])
    return lis

#generate next itemlist
def gen_next(flisk,k):
    lis = []
    n = len(flisk)
    for i in range(0,n):
        for j in range(i+1,n):
            l1 = flisk[i][:k-2]
            l2 = flisk[j][:k-2]
            if l1==l2:
                if flisk[i][-1]!=flisk[j][-1]:
                    m=flisk[i]+[flisk[j][-1]]
                    lis.append(m)
                    
    return lis

#pruning the itemlist
def prune(lis,r):
    if len(lis)>0:
        l = len(lis[0])
    else:
        return []
    retlis=[]
    for i in lis:
        flag=True
        for j in range(0,l):
            m = i[:j]+i[j+1:]
            if not r.search(m):
                flag=False
        if flag:
            retlis.append(i)
    return retlis

            

#flisk --> frequency list of length k
#glk --> generated list of each item set of length k
                
def apriori(ff):
    tot=0
    glk = gen_list() #k=1
    ulis=glk
    k=1
    flisk,d = freq_list(glk,k)
    r = TrieNode('None',0)
    for i in flisk:
        tot+=1
        r.addelement(i,d[flisk.index(i)])
    k = 2
    while len(flisk)>0:
        glk = gen_next(flisk,k)
        retlis = prune(glk,r)
        flisk,d = freq_list(retlis,k)
        for i in flisk:
            tot+=1
            r.addelement(i,d[flisk.index(i)])  
        k+=1
    print tot    
    r.print_trie([])
    if ff=='1':
        rules(r)



apriori(dic['flag'])


sys.stdout.close()
