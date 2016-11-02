import math, requests, re, sys

def check_sqrt(n, p):
	q = int(math.sqrt(n))
	for i in range(q, q + p):
		if n % q == 0:
			return q, n / q
	return None, None
	
def find_small_factor(n, p):
	for i in range(0, p):
		if n % p == 0:
			return p, n / p
	return None, None
    
def check_factordb(n):
    r = requests.get('http://factordb.com/index.php?query=' + str(n))
    if 'FF' in r.text: return 1
    if 'CF' in r.text: return 2
    else: return 0

if len(sys.argv) > 1:
    n = int(sys.argv[1])
else:
    sys.exit()

print 'Prime: {0}'.format(n)
print '[ ] Checking factor.db'

if check_factordb(n) != 0:
    if n == 1: print '[+] Fully factored'
    else: print '[+] Factor known!'
    sys.exit()
else: 
    print '[-] No factors found...'

print '[ ] Checking small factor (delta = 1e6)'
p, q = find_small_factor(n, int(1e6))
    
if p != None:
    print 'N = {0} * {1}'.format(p, q)
    sys.exit()
else: print '[-] No factors found...'
    
print '[ ] Checking factor close to sqrt(n) (delta = 1e6)'
p, q = check_sqrt(n, int(1e6))
    
if p != None:
    print 'N = {0} * {1}'.format(p, q)
    sys.exit()
else: print '[-] No factors found...'