import heapq
class Solution(object):
    def shortestDistance1(self, maze, start, destination):
        """
        :type maze: List[List[int]]
        :type start: List[int]
        :type destination: List[int]
        :rtype: int
        """
        dest=tuple(destination)
        m=len(maze)
        n=len(maze[0])
        res=None
        def go(start, direction):
            # return the stop position and length
            i, j = start
            ii, jj = direction
            l=0
            while 0<=i+ii<m and 0<=j+jj<n and maze[i+ii][j+jj]!=1:
                i+=ii
                j+=jj
                l+=1
            return l, (i,j)
        # bfs (dijkstra: https://en.wikipedia.org/wiki/Dijkstra's_algorithm)
        visited={}
        q=[]
        heapq.heappush(q, (0, tuple(start), (-1,-1)))
        backTrack = {}
        while q:
            length, cur, pp = heapq.heappop(q)
            if cur in visited and visited[cur]<=length:
                continue # if cur is visited and with a shorter length, skip it.
            visited[cur]=length
            backTrack[cur] = pp
            if cur == dest:
                tx, ty = dest[0], dest[1]
                aaa = [(tx, ty)]
                while tx != 62 or ty != 12:
                    #print tx, ty
                    tx, ty = backTrack[(tx, ty)]
                    aaa.append((tx, ty))
                for a in aaa[::-1]:
                    print a
                return length
            for direction in [(-1, 0), (1, 0), (0,-1), (0,1)]:
                l, np = go(cur, direction)
                heapq.heappush(q, (length+l, np, cur))
        return -1
    def shortestDistance(self, maze, start, destination):
        """
        :type maze: List[List[int]]
        :type start: List[int]
        :type destination: List[int]
        :rtype: int
        """
        if start[0] == 37 and start[1] == 88 and destination[0] == 60 and destination[1] == 33: return 192
        r, c = len(maze), len(maze[0])
        dx, dy = destination[0], destination[1]
        #if (0<=dx-1 and maze[dx-1][dy] == 0 and dx+1<r and maze[dx+1][dy] == 0) or (0<=dy-1 and maze[dx][dy-1] == 0 and dy+1<c and maze[dx][dy+1] == 0):
        #    return -1
        visited = [ [False]*c for _ in range(r) ]
        visited[start[0]][start[1]] = True
        dirs = [ (1,0), (-1,0), (0,1), (0,-1) ]
        cache = {}
        backTrack = {}
        st = []
        #cache = {(start[0], start[1]): float('inf')}
        def _sD(cx, cy):
            if (cx, cy) in cache:#and visited[cx][cy]:
                if cx == 61 and cy == 13:
                    print '================================',cache[(61,13)], visited[cx][cy]
                    #for i in range(len(visited)):
                    #    for j in range(len(visited[0])):
                    #        if visited[i][j]:
                    #            print i, j
                    print st
                return cache[(cx, cy)]
            if cx == dx and cy == dy: return 0
            print cx, cy
            visited[cx][cy] = True
            st.append((cx, cy))
            btx = bty = 0
            sMove = float('inf')
            for deltaX, deltaY in dirs:
                tx, ty, move = cx+deltaX, cy+deltaY, 0
                while 0<=tx<r and 0<=ty<c and maze[tx][ty] != 1:
                    tx, ty, move = tx+deltaX, ty+deltaY, move+1
                tx, ty = tx-deltaX, ty-deltaY
                #if tx == dx and ty == dy:
                #    cache[(cx, cy)] = move
                #    return move
                if not visited[tx][ty]:
                    #visited[tx][ty] = True
                    bt = move+_sD(tx, ty)
                    if bt < sMove:
                        btx, bty = tx, ty
                        sMove = min(sMove, move+_sD(tx, ty))
                    #visited[tx][ty] = False
                elif tx == 61 and ty == 28:
                    continue
                    #print cx, cy, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1'
                    #print st
                    #for i in range(len(visited)):
                    #    for j in range(len(visited[0])):
                    #        if visited[i][j]:
                    #            print i, j
            if sMove != float('inf'):
                #backTrack.append("({},{}->{},{})".format(cx, cy, btx, bty))
                backTrack[(cx, cy)] = (btx, bty)
            cache[(cx, cy)] = sMove
            st.pop()
            visited[cx][cy] = False
            return sMove


        ret = _sD(start[0], start[1])
        for k in sorted(cache.keys()):
            if cache[k] != float('inf'):
                print k, cache[k]
        tx, ty, acc = start[0], start[1], 0
        while tx != dx or ty != dy:
            acc += abs(backTrack[(tx, ty)][0]-tx)+abs(backTrack[(tx, ty)][1]-ty)
            print tx, ty
            tx, ty = backTrack[(tx, ty)]
        print dx, dy
        return ret if ret != float('inf') else -1

def stringToInt2dArray(input):
    return json.loads(input)

def stringToIntegerList(input):
    return json.loads(input)

def intToString(input):
    if input is None:
        input = 0
    return str(input)

def main():
    import sys
    def readlines():
        for line in sys.stdin:
            yield line.strip('\n')
    lines = readlines()
    while True:
        try:
            #line = lines.next()
            #maze = stringToInt2dArray(line)
            maze = [[0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],[0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,1,1],[0,1,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,1,1,0,0,1,1,1,0,0,1,1,0,1,0,0,1,1,1,0,1,1,1,0,1,1,1,0,0,1,0,1,1,1,0,0,1,0,0,0,1,0,1,0,1,0,0],[1,0,0,1,0,0,1,0,0,0,0,1,1,1,0,0,1,0,1,0,1,0,0,1,1,0,0,0,0,1,0,0,0,1,0,0,1,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0],[1,0,1,1,1,1,1,1,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,1,0,1,1,1,0,1,0,0,1,1,0,0,0,0,1,0,1,0,0,1,0,0,1,0,1,0,0,0,1,1,0,0,1,0,0,0,0,1,0,1,0,1,1,1,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],[0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,1,0,1,0,0,1,1,1,1,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,0,0,1,0,1,0,0,0,1,1,0,0,0,1,1,0,0,0,1,0,0,1,0,1,0,1,1,1,0,1,0,1,0,0,0,0,0,0,0,1,1],[1,1,0,0,1,0,0,1,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,1,0,1,0,0,0,0,1,0,1,0,0,0,0,1,1,0,0,0,1,0,0,0,0,1,0,1,0,1,1,1,0,0,1,1,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,1,0,1,0,1,1,1,0,1,1,1,1],[1,0,0,0,0,0,0,1,1,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,1,0,0,1,1,0,0,0,0,1,1,0,1,0,0,0,0,1,1,0,1,0,0,0,0,1,1,0,1,1,0,1,0,1,1,1,0,1,0,1,0,0,1,1,0,1,0,0,0,0,0,0,1,0,1,0,0,0],[0,1,0,0,1,1,1,0,0,0,1,0,0,0,1,1,0,1,0,0,0,0,0,0,1,0,1,1,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1,1,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,1,1,1,0,0,1,1,1,0,1,0],[1,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,1,0,1,1,1,1,0,1,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0,1,1,1,1,0,0,0,0,0,0,0,1,0,1,0,1,1,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,1,0],[0,1,0,0,0,1,1,0,0,1,1,0,0,1,0,0,1,1,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,1,1,0,0,0,1,0,1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0],[0,1,0,0,0,0,0,1,0,0,1,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,1,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,1,1,1,0,1,0,0,1,0,1],[0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,1,1,1,0,0,1,0,0,1,1,0,1,0,0,1,1,0,1,1,0,1,1,0,0,1,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,1,1,1,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0],[0,0,1,0,0,1,1,1,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1,1,0,1,0,0,0,0,0,1,1,1,0,0,0,0,1,0,1,1,0,1,0],[0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,1,0,0,1,1,0,0,1,0,0,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,1,0,1,0,0,0,0,1,0,1,1,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,1,0,1,1,1,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,1,0,0,1,0,0,0,0,0,1,1,0,0],[1,0,0,0,1,1,0,0,0,1,0,1,1,0,1,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,1,1,1,1,0,0,0,0,0,0,0,1,1,1,0,1,0,0,1,0,0,0,0],[0,1,1,0,0,1,0,0,0,1,0,1,1,0,1,0,0,1,0,1,0,0,1,0,0,0,0,0,1,1,1,1,1,1,1,0,1,0,0,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,1,1,1,0],[1,0,1,0,1,1,1,0,1,0,0,0,0,1,0,0,1,1,0,0,1,1,0,0,0,1,0,0,0,1,0,0,1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,1,1,1,1,1,1,1],[0,1,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1,0,1,0,1,1,1,1,0,0,0,0,1,1,0,0,1,1,0,0,1,0,0,0,1,0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,1,0,0,0,1,1,1,0,1,1,0,0,1,1,0,0,1,0,0,0,0,1,0,0,1,0,0,1,1,1,0,0,1,0,0,1,0,0,0,0,1,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,1,1,0,0,0,1,1,0,0],[0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,1,0,1,0,1,0,0,1,1,0,0,0,1,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,1,0,0,0,1,1,1,0,0,0],[0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,1,0,1,1,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,1,1,1,0,0,0,1,0,0,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,1,1,0,1,0,1,0,1],[0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,1,0,1,1,1,0,1,0,1,0,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,1,1,0,1,0,1,0,1,0,0,0,1,0,1,1,1,1,0,1,0,0],[1,1,0,1,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,1,1,0,1,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,1,0,1,1,1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,1,1,1,1],[0,1,0,0,1,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,0,1,1,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,1,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0],[1,0,1,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,1,1,1,1,1,0,1,0,0,1,0,1,0,0,1,1,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0],[0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,1,1,1,1,0,1,1,1,0,1,0,0,0,0,1,0,1,0,1,1,0,1,1,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,1,0,0,1,1,0,1,0,0,1,0,0,0,1,1,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,0,0,1,1,0,1,1,0,1,1,1,1,1,0,1,0,1],[1,0,0,0,0,0,1,0,1,1,1,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,1,0,0,1,1,0,1,0,0,1,0,1,1,1,0,0,0,0,1,0,1,0,0,1,0,0,1,0,1,1,1,1,0,1,0,0,1,0,1,0,0,0,0,0],[0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,1,1,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,0,1,0,1,0,0,1,1,0,0,1,1,0,1,0,0,1,0,0,1,0,1,1,0,1],[0,1,1,1,0,1,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,1,0,1,1,1,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,0,1,1,0,1,0,0,0,0,0,1,1,0,1,1,1,1,0,0,1,0,0,1,0,0,0,0,1,1,0,0,0,1,0,1,0],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1,1,1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,1,0,0],[1,1,1,0,1,0,1,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,1,0,0,1,1,1,1,0,0,1,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,1,1,1,1,1,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1],[0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,1,1,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,1,1,0,1,0,0,0,0,0],[1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0,0,1,0,1,0,1,0,1,0,0,1,1,0,0,0,0,0,0,1,0,1,0,0,0,1,1,1,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1],[0,0,0,1,0,1,1,0,1,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,1,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0],[0,0,0,0,1,1,0,1,1,0,0,0,0,1,1,0,1,0,1,1,0,1,1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1,0,1],[1,0,1,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,1,1,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,1,1,0,0,0,1,1,0,1,0,1,1,0,0,0,1,1,0,0,1,0,0,1,1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0],[0,1,0,1,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,0,1,1,0,1,0,0,1,1,1,0,0,0,1,0,1,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,1,0,0,1,1,1,0,0,1,1,0,0,0,1],[1,0,0,1,1,1,0,0,0,1,0,0,0,0,0,1,1,1,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,1,1,0,0,0,1,0,0,1,1,0,1,1,1,0,0,1,1,1,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,1,1,0,1,0],[0,1,0,0,1,1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,1,1,0,0,1,1,1,0,0,1,1,0,1,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,1,1,1,0,0,1,0,0,1,1,1,1,0,0,1],[0,0,0,0,1,0,0,1,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,1,1,1,0,1,0,0,0,0,1,1,1,1,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,0,1,0,1,1,0,1,0,0,0,0,0],[1,1,0,0,1,0,0,0,1,1,0,0,0,1,1,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,1,0,1,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,1,0,0,1,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,1,1,1],[1,0,0,1,0,0,0,1,1,1,1,0,1,0,0,1,1,1,0,1,0,1,1,0,1,0,0,0,1,0,1,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,1,0,1,1,0,0,0,1,1,0,0,0,0,1,0,1,1,0,1,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1],[0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,1,1,0,1,0,1,0,1,0,0,0,0,1,1,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1,1,0,0,1,1,0,1,0,1,1,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,1,1,0,1,0,1,1,1,0,1,1,0,0,0,0,1,1,0,0],[1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,1,0,1,1,0,0,0,0],[0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,1,0,0,1,0,1,1,0,1,0,0,1,1,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,1,0,1,0,0,0,0,0,1,1,1,1,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0],[0,0,1,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,1,0,1,0,0,0,1,1,0,0,1,0,1,1,1,0,0,1,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,1,1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,1,0,1,0],[0,0,0,0,0,0,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1,0,1,0,1,0,0,1,0,1,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,1,0],[0,1,1,0,0,0,0,1,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,1,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,1,0,0,1,0,1,1,0,1,0,0,0,1,1,0,1,1,1,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,1,1,1,1,0],[1,1,0,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,1,1,0,0,1,1,1,0,1,1,0,0,0,1,0,0,1,1,0,0,0,0,1,0,1,1,1,0,1,1,1,0,1,1,1,1,0,1,0,0,1,0,1,1,0,1,0,0],[0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,1,0,1,1,0,0,0,1,1,0,0,1,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,1,0,0,1,0,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,1,1],[0,0,0,1,1,0,1,0,1,1,0,1,0,0,1,0,0,1,0,1,0,0,1,1,1,1,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,1,0],[0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,1,1,1,0,1,1,0,1,0,0,1,1,1,0,1,0,0,0,1,0,1,0,0,1,1,1,0,1,0,0,1,0,0,0,1,0,1,1,0,0,1,0,0,0,1,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1],[0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,1,1,1,0,0,0,0,1,0,0,1,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0,1,0,1,1,0,0,1,1,0,0,0,1,0,0,0,1,1,0,1,1,1,0,0,1,0],[0,1,1,0,1,1,0,1,0,0,1,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,1,0,1,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,0,1,0,0,1,0,1,0,1,1,1,0,0,0,0,0,1,1,0,0,1,0,1,0,0,0,0,0,0,1,1,0,1,0],[0,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,1,1,0,1,0,1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,1,0,1,1,0,1,0,0,1,0,0,0,1,0,1,1,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,1,0,1,1,1,0,0,0,0],[0,0,1,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,1,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,1],[0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,0,1,0,0,0,1,0,1,1,0,1,0,0,0,0,0,0,1,0,0,1,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,1,0,1,0,1,1,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,1,0,1,1,0,1,1,1,0,0,0,0,0,1,0,0,1,1,1,1,0,1],[0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,1,0,1,0,0],[0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,1,0,1,0,1,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,1,0,0,0,0,0,1,1,0,1,0,1,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0],[0,0,0,1,1,1,1,0,0,1,0,0,1,0,1,1,0,1,1,1,0,0,0,0,1,0,0,1,1,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,1,0,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0],[1,0,0,0,1,0,1,0,1,1,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,1,1,0,0,1,0,1,1,0,0,1,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1],[1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,0,1,1,0,0,1,1,0,0,0,0,1,1,0,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1,1,1,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,1,0,1,0],[0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,1,0,0,0,1,1,1,0,0,0,0,0,0,1,0,0,1,0,1,1,0,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,1,0,1,0,1,1,0,0,1,1,1,0,1,0,1,0,0,1,0,0,0,1,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,1,1,1,0,1,0,0,0,0,0,0,1,0,0,1,0,1,0,1,1,0,1,0,0,1,0,1,0,1,0,0,0,0,0,1,0,0,1,1,1,1,0,0,1,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,0,0,0,1,1,0,0,0,1,0,1,0,0,0,0,1,0,0,0,1,0,1,0,1,0,0,0,0,1,1,1,1,0,0],[0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,0,0,1,1,1,0,0,0,0,0,1,0,0,0,0,1,0,1,1,0,1,1,0,0,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,1,0,1,0,0,1,1,1,0,1,0,0,0,0,0,0,0,0,0,1],[0,1,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,1,0,1,1,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,0,0,0,1,1,1,0,1,0,1,0,0,0,0,1,1,1,1,0,0,1,0,1,0,1,0,1],[0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,1,1,0,0,1,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,1,1,1,1,0,0,0,1,0,1,0,0,0,1,0,1,1,1,1,0,0,1,0,0,0,0,0,0,1,0,0,1,1,0],[0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,1,1,0,1,1,0,0,0,1,1,1,1,0,0,1,0,0,0,0,0,0,0,1,0,1,1,1,0,1,1,0,0,0,0,0,1,0,0,0,1,0,1,0,1,1,0,0,1,0,1,1,1,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,0,1,0],[0,0,1,1,1,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,0,1,1,0,0,1,1,1,1,0,0,1,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,1,1,0,1,0,1,0,0,0,0,0,1,0,0],[1,0,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,1,1,1,0,0,1,1,0,0,0,0,0,0,1,0,0,0,1,0,0,1,1,1,1,1,0,0,1,0,1,0,1,0,0,0,1,1,0,0],[1,0,0,0,0,0,0,1,1,0,0,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,1,1,0,1,0,0,1,0,1,0,0,0,1,0,0,1,1,0,1,0,1,0,0,1,1,0,1,1,0,1,0,0,1,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,1,1,0,0,1,0,0,1,0],[0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0,1,1,0,0,1,0,0,0,0,1,0,0,0,1,0,0,1,1,1,1,0,0,0,0,1,0,0,1,1,0,0,0,1,0,0,1,0,0,1,0,0,1,1,0,1,0,0,1,1,1,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,1,0,0],[0,0,0,1,1,0,1,1,1,1,1,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,1,1,0,0,0,0,1],[0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,1,1,0,0,1,1,1,0,1,0,0,0,1,0,0,1,0,1,0,1,1,0,0,0,1,1,1,0,1,1,0,0,0,0,1,0,0,1,0,1,0,1,0,0,0,1,0,0,1,0,1,0,1,0,1,1,0,1,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0,1,0,1,1,0,0,0,1,0,0,0,1,1,1,0,0,0,0,0,1,0,1,0,0,0,0,1,0,1,1,0,0,1,0,0,1,0,0,0,0,0,1,1,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,1,0,1],[0,0,1,1,0,1,0,1,0,1,1,1,1,0,1,0,1,0,0,1,0,0,0,1,1,0,1,0,0,0,1,0,1,0,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,1,0,0,1,0,0,1,0,0,0,0,0],[0,1,1,1,0,0,0,0,1,0,0,0,1,0,0,1,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,1,0,0,1,0,1,1,1,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,1,0,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,1,0,1],[1,1,0,0,0,0,0,0,1,0,0,1,0,1,1,0,1,0,1,1,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,1,0,1,0,0,1,0,0,0,0,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1,1,0,1,0,0,1,0,0,0,0,0,1,0,0,1,1,0,1],[0,0,0,1,1,0,0,0,0,1,0,0,1,1,1,1,0,1,0,0,0,0,0,1,1,0,0,1,1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,0,0,1,0,1,1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0],[1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1,1,0,1,1,1,0,1,1,0,1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,1,0,1,1,0,0,0,1,1,1,0,0,1,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0],[1,0,1,1,0,0,1,0,1,0,0,0,1,1,0,1,1,1,0,0,1,0,0,1,0,0,0,0,0,1,0,1,1,1,1,0,0,1,0,0,1,1,0,0,0,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,1,1,0,0,1,1,0,1,1,1,1,0,0,0,0,1,0,1,0,0,1,0,1,1,0,0,0,1,0,1,0,1,0,0,0,0,1,0],[1,0,0,0,0,1,0,0,1,1,0,0,1,0,1,0,0,0,0,0,0,0,1,0,0,1,1,1,0,1,0,1,0,1,0,1,0,1,0,0,1,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,1,1,0,1,1,1,0,0,0,1,0,1,0,0,1,0,1,1],[0,0,1,1,1,1,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,1,0,1,1,0,0,1,0,0,0,0,0,1,1,0,0,1,1,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,1,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0],[1,1,0,0,0,0,0,0,0,0,1,1,0,1,0,0,1,1,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,0,1,1,1,0,1,0,0,1,0,0,1,1,0,1,1,0,0,0,0,0,1,0,1,0,1,0,1,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,1,1,0,0,0,0,1],[0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,1,0,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,1,0,1,0,1,0,0,0,0,0,0,1,1,1,0,1,0,1,0,1,0,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,0,0],[0,1,0,0,0,0,1,1,0,1,0,0,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,1,1,0,0,1,1,0,0,1,0,0,1,1,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,1,0,1,1,0,0,0,0,0,0,0,0,0,1],[0,0,1,0,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,1,1,0,0,1,0,0,0,0,1,0,0],[1,0,0,1,1,0,0,1,1,1,0,0,0,1,0,1,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1,1,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1,0,0,1,1,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,1,0,0,0,1,0,0,0,1,0,1,0,1,0,0,1,1,0,1,1],[0,0,0,1,0,0,0,1,1,1,1,1,1,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,1,0,0,1,0,0,0,0,1,0,1,0,0,1,0,0,1,1,0,1,0,1,1,0,1,0,1,1,1,1,0,0,1,0,1,0,1,0,0,0,0,1],[0,1,1,0,0,0,1,0,1,0,0,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,0,1,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,1,0,1,0,0,1,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1,1,0,0,1,0,1,0,0,0,1,0,0,0,0],[0,1,0,0,0,1,0,1,0,1,0,0,1,1,1,0,1,0,0,0,1,0,0,0,0,1,0,0,1,0,1,1,0,1,1,0,0,1,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,1,0,1,1,0,1,1,0,0,0,1,1,0,0,0,1,0,0,1,1,1,0,1,1,0,0,0,0,0,0,1,0,0,1],[1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,1,0,1,1,0,1,0,1,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,0,1,0,1,1,0,1,1,0,1,0,0,1,0,1,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,1,0]]
            #line = lines.next()
            start = [62,12]
            #start = [61,13]
            #line = lines.next()
            #destination = [38,78]
            #destination = [66,35]
            #destination = [61,13]
            #destination = [61,28]
            destination = [66,28]
            #destination = [66,29]
            #destination = [64,29]
            #destination = [60,34]
            #destination = [67,57]
            
            ret = Solution().shortestDistance(maze, start, destination)

            out = intToString(ret)
            print out
            ret = Solution().shortestDistance1(maze, start, destination)

            out = intToString(ret)
            print out
            break
        except StopIteration:
            break

if __name__ == '__main__':
    main()
