
def isP(word):
	l = len(word)
	for i in range(l/2):
		if word[i]!=word[l-i-1]:
			return False
	return True

def solution(slist):
	myset = set()
	for x in slist:
		myset.add(x)
	l = len(slist)
	ans = []

	for i in range(l):
		word = slist[i]
		print 'word:',word
		for j in range(len(word)+1):
			sub1 = word[:j]
			sub2 = word[j:]
			if isP(sub1):
				rvs = sub2[::-1]
				if rvs in myset and rvs!=word:
					print 'sub1',sub1,word
					ans.append([word,rvs])
			if isP(sub2):
				rvs = sub1[::-1]
				if rvs in myset and rvs!=word:
					print 'sub2',sub2,word
					ans.append([word,rvs])
	return ans

mylist = ['abcd', 'dcba', 'lls', 's', 'sssll']
print solution(mylist)

