class Solution(object):
    def minAbbreviation(self, target, dictionary):
        """
        :type target: str
        :type dictionary: List[str]
        :rtype: str
        """
        def abbLen(s):
            r = 0
            for i in range(len(s)):
                if s[i].isdigit():
                    if i>0 and s[i-1].isdigit(): continue
                r += 1
            return r
        def match(word, abb):
            cur, l, a, la, number = 0, len(word), 0, len(abb), 0
            while a < la or number != 0:
                if a < la and abb[a].isdigit():
                    number = number*10 + int(abb[a])
                    a += 1
                    continue
                if number:
                    cur += number
                    if cur > l: return False
                    number = 0
                    continue
                else:
                    if cur == l or word[cur] != abb[a]: return False
                    cur += 1
                    a += 1
            #print cur, l
            if cur<l: return False
            return True
        cache = {}
        def _gA(s):
            if not s: return [""]
            if s in cache: return cache[s]
            l = len(s)
            r = [ str(l) ]
            for i in range(l-1, 0, -1):
                for x in _gA(s[i+1:]):
                    r.append(str(i)+s[i]+x)
            for x in _gA(s[1:]):
                r.append(s[0]+x)
            cache[s] = r
            return r
        print 'pre gA'
        a = _gA(target)
        print 'after gA'
        a.sort(key=abbLen)
        print len(a)
        for x in a:
            conflict = False
            for d in dictionary:
                if match(d, x):
                    conflict = True
                    break
            if not conflict:
                return x

def stringToString(input):
    return input[1:-1].decode('string_escape')

def stringToStringArray(input):
    return json.loads(input)

def main():
    import sys
    def readlines():
        for line in sys.stdin:
            yield line.strip('\n')
    lines = readlines()
    while True:
        try:
            #line = lines.next()
            target = "usaandchinaarefriends"
            #line = lines.next()
            dictionary = []
            
            ret = Solution().minAbbreviation(target, dictionary)

            out = (ret)
            print out
        except StopIteration:
            break

if __name__ == '__main__':
    main()
