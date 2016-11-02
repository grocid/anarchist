import gmpy2, requests, re, sys

def sieve(n):
    """ http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n/3035188#3035188 """
    n, correction = n-n%6+6, 2-(n%6>1)
    sieve = [True] * (n/3)
    for i in xrange(1,int(n**0.5)/3+1):
      if sieve[i]:
        k=3*i+1|1
        sieve[      k*k/3      ::2*k] = [False] * ((n/6-k*k/6-1)/k+1)
        sieve[k*(k-2*(i&1)+4)/3::2*k] = [False] * ((n/6-k*(k-2*(i&1)+4)/6-1)/k+1)
    return [2,3] + [3*i+1|1 for i in xrange(1,n/3-correction) if sieve[i]]

def check_sqrt(n, p):
	q = int(gmpy2.iroot(n, 2)[0])
	for i in range(q, q + p):
		if n % i == 0:
			return i, n / i
	return None, None
	
def find_small_factor(n, p):
	for i in p:
		if n % i == 0:
			return i, n / i
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

print 'Number (n): {0}'.format(n)
print '[ ] Checking factor.db'

if check_factordb(n) != 0:
    if n == 1: print '[+] Fully factored'
    else: print '[+] Factor known!'
    sys.exit()
else: 
    print '[-] No factors found...'

print '[ ] Checking small factor (delta = 1e8)'
primes = sieve(int(1e8))
p, q = find_small_factor(n, primes)
    
if p != None:
    print 'N = {0} * {1}'.format(p, q)
    sys.exit()
else: print '[-] No factors found...'
    
print '[ ] Checking factor close to sqrt(n) (delta = 1e8)'
p, q = check_sqrt(n, int(1e8))
    
if p != None:
    print 'N = {0} * {1}'.format(p, q)
    sys.exit()
else: print '[-] No factors found...'

print int(gmpy2.iroot(n, 2)[0])