from time import time
from random import shuffle
from printer import printm

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

def Bidirectional_Search(m):
    global res
    cur = m[:]
    que = [cur,leaf]
    mkd_right,mkd_left = {cur : -1},{leaf : -1}
    dir = {cur : 'right', leaf : 'left'}
    step = {cur : -1, leaf : -1}

    while 1:
        cur = que.pop(0)
        if cur in mkd_right and cur in mkd_left:
            intersection = cur[:]
            break
        for i,j in expand(cur):
            cur_dir = dir[cur]
            isRight = cur_dir == 'right'
            if (isRight and i not in mkd_right) or \
               (not isRight and i not in mkd_left):
                que.append(i)
                (mkd_right if isRight else mkd_left)[i] = cur
                step[i],dir[i] = j,cur_dir

    for i in range(2):
        mkd = [mkd_right,mkd_left][i]
        cur = intersection[:]
        path = [[cur,step[cur]]]
        while mkd[cur] != -1:
            cur = mkd[cur]
            path.append([cur,step[cur]])
        res += (path if i else path[::-1])[1:]

    print(res)

    # "left" 방향의 노드들의 스텝은 반대로 연결할 것
    

    



# def path(mkd,step,cur):
#     path = [[cur,step[cur]]]
#     while mkd[cur] != -1:
#         cur = mkd[cur]
#         path.append([cur,step[cur]])
#     res += path[::-1][1:]
#     return mkd[-2]

m = [1,2,3,4,5,6,7,0,0]
shuffle(m)
m = ''.join(map(str,m))
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

Bidirectional_Search(m)

te = time() - ts

for m,info in res:
    s,e,dire,pack = info
    print(' "{}" | [{}] ( {} to {} )\n'.format(pack,dire,s,e))
    printm(m,3,3)

print("{}step, {}s\n".format(len(res),round(te,3)))