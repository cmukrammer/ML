import collections
class Solution(object):
    def alienOrder(self, words):
        """
        :type words: List[str]
        :rtype: str
        """
        d = collections.defaultdict(set)
        indegree = collections.defaultdict(int)
        n = len(words)
        for word in words:
            for c in word:
                d[c] = set()
                indegree[c] = 0
        for i in xrange(1, n):
            j = 0
            while j < len(words[i-1]) and j < len(words[i]) and words[i-1][j] == words[i][j]:
                j += 1
            if j != len(words[i-1]) and j != len(words[i]):
                a, b = words[i-1][j], words[i][j]
                if b not in d[a]:
                    indegree[b] += 1
                d[a].add(b)
        print d
        print indegree
        q = list()
        for c in indegree:
            if indegree[c] == 0:
                q.append(c)
        res = ''
        while q:
            c = q.pop(0)
            res += c
            for cchild in d[c]:
                indegree[cchild] -= 1
                if indegree[cchild] == 0:
                    q.append(cchild)
        return '' if len(res) != len(indegree) else res

def stringToStringArray(input):
    return json.loads(input)

def main():
    import sys
    def readlines():
        for line in sys.stdin:
            yield line.strip('\n')
    #lines = readlines()
    try:
        #line = lines.next()
        words = ["wrt","wrf","er","ett","rftt"]
            
        ret = Solution().alienOrder(words)

        out = (ret)
        print out
    except StopIteration:
        print 1

if __name__ == '__main__':
    main()
