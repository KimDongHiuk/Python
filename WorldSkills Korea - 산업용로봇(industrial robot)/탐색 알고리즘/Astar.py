from time import time
from random import shuffle

def printm(m,x,y,z=1):      # UseFont : consalas
    m = ''.join([' ' if str(i) is 'x' else str(i) for i in m])
    for i in range(z-1,-1,-1):
        if z > 1:
            print('{} Floor'.format(i+1))
        print(''.join(['┌───',''.join(['┬───'] * (x - 1)),'┐']))
        for j in range(y):
            n = x * j
            print('│',' │ '.join(m[(0 + ((y * x) * i) + n):(x + ((y * x) * i) + n)]),'│')
            if j != y - 1:
                print(''.join(['├───',''.join(['┼───'] * (x - 1)),'┤']))
        print(''.join(['└───',''.join(['┴───'] * (x - 1)),'┘']))
    print('')

def heuristic(m):        # Calcurating Heuristic
    res = 0
    for i in range(9):
        if m[i] != '0':
            y1,x1 = divmod(i,3)
            y2,x2 = divmod(leaf.index(m[i]),3)
            res += abs(y1 - y2) + abs(x1 - x2)        
    return res

def f(state):
    m,g,h = state
    return g + h

def exchange(state,s,e):
    m,g,h = state
    m = list(m)
    m[s],m[e] = m[e],m[s]
    dire = '↑→↓←'[[-3,1,3,-1].index(s-e)]
    info = [e,s,dire,m[s]]
    return [(''.join(m),g + 1,heuristic(m)),info]
    
def around(pos):
    if pos in cache:
        return cache[pos]
    res = []
    dy,dx = [-1,0,1,0],[0,1,0,-1]
    y,x = divmod(pos,sx)
    for i in range(4):
        ny,nx = y + dy[i],x + dx[i]
        if -1 < ny < sy and -1 < nx < sx:
            res.append(ny * sx + nx)
    cache[pos] = res
    return res

def expand(state):
    res = []
    m,g,h = state
    for i in range(size):       
        if m[i] != '0' or i in fix:
            continue        
        for j in [j for j in around(i) if m[j] != '0' and j not in fix]:            
            res.append(exchange(state,i,j))
    return res

def Astar(state):
    global res
    cur = state[:]
    Pque = [cur]
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = min(Pque,key = lambda state : f(state))
        Pque.remove(cur)
        if cur[0] == leaf:
            break
        for i,j in expand(cur):
            if i not in mkd:
                Pque.append(i)
                mkd[i],step[i] = cur,j
    mkd[-2] = cur
    path = [[cur,step[cur]]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append([cur,step[cur]])
    res += path[::-1][1:]
    return mkd[-2]

leaf = '123456700'
m = [1,2,3,4,5,6,7,0,0]
shuffle(m)
m = ''.join(map(str,m))
state = (m,0,heuristic(m))      # m, cost, heuristic

print('init_state')
m,g,h = state
print('f({}) = g({}) + h({})'.format(g + h, g, h))
printm(m,3,3)

print('leaf_state')
printm(leaf,3,3)

sy,sx = 3,3
size = sy * sx
fix = []
res = []
cache = {}

ts = time()             # timeStart

Astar(state)

te = time() - ts        # timeEnd

for state,info in res:
    m,g,h = state
    s,e,dire,pack = info
    print(' "{}" | [{}] ( {} to {} )\n'.format(pack,dire,s,e))
    print(' f({}) = g({}) + h({})'.format(g + h, g, h))
    printm(m,3,3)

print("{}step, {}s\n".format(len(res),round(te,3)))