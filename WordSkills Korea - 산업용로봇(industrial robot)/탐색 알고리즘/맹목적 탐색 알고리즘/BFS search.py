from time import time

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

def exchange(m,s,e):
    m = list(m)
    m[s],m[e] = m[e],m[s]
    dire = '↑→↓←'[[-3,1,3,-1].index(s-e)]
    info = [e,s,dire,m[s]]
    return [''.join(m),info]
    
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

def expand(m):
    res = []
    for i in range(size):       
        if m[i] != '0' or i in fix:
            continue        
        for j in [j for j in around(i) if m[j] != '0' and j not in fix]:            
            res.append(exchange(m,i,j))
    return res

def bfs(m,leaf,pos = -1,pack = -1):
    global res
    cur = m[:]
    que = [cur]
    mkd,step = {cur:-1},{cur:-1}
    while 1:
        cur = que.pop(0)
        if (pos == -1 and cur == leaf) or (pos != -1 and cur[pos] == pack):
            break
        for i,j in expand(cur):
            if i not in mkd:
                que.append(i)
                mkd[i],step[i] = cur,j
    mkd[-2] = cur
    path = [[cur,step[cur]]]
    while mkd[cur] != -1:
        cur = mkd[cur]
        path.append([cur,step[cur]])
    res += path[::-1][1:]
    return mkd[-2]

m = '034570612'
leaf = '123456700'

print('init_state')
printm(m,3,3)

print('leaf_state')
printm(leaf,3,3)

sy,sx = 3,3
size = sy * sx
fix = []
res = []
cache = {}

ts = time()

# Optimal
# bfs(m,leaf)

# not Optimal
for i in range(3):
    m = bfs(m,leaf,i,leaf[i])
    fix.append(i)
bfs(m,leaf)

te = time() - ts

for m,info in res:
    s,e,dire,pack = info
    print(' "{}" | [{}] ( {} to {} )\n'.format(pack,dire,s,e))
    printm(m,3,3)

print("{}step, {}s\n".format(len(res),round(te,3)))