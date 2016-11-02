import string, base64
import argparse, copy
from bisect import bisect_left

def find_words(trellis):
    
    def subword_exists(word_fragment):
        try:
            match = words[bisect_left(words, word_fragment)]
            if match.startswith(word_fragment):
                if match == word_fragment:
                    return 1
                return 2
            else:
                return -1
                
        except IndexError:
            return -1
    
    layer_index = 0
    layer = list(set([c[0].lower() for c in trellis[layer_index]]))
    filtered_layer = copy.copy(layer)
    completed_at = []
    
    while layer_index < len(trellis) - 1:
        
        layer_index += 1
        layer = list(set([c[0].lower() for c in trellis[layer_index]]))
        new_filtered_layer = []
        
        for prefix in filtered_layer:
            subword = prefix
            
            for fragment in layer:
                
                subword += fragment[0].lower()
                r = subword_exists(subword)
                
                if r != -1:
                    new_filtered_layer.append(subword)
                
                subword = subword[:-1]
        
        if len(new_filtered_layer) == 0:
            break
        
        filtered_layer = new_filtered_layer
    
    return filtered_layer
    
alphabet = string.ascii_letters + ' ,.?!'
max_keylength = 6
wordlist = '/usr/share/dict/words'

parser = argparse.ArgumentParser(description='XOR tool')
parser = argparse.ArgumentParser()

parser.add_argument('-c',  nargs=1, help='Specify ciphertext')
parser.add_argument('-k',  nargs=1, help='Specify maximum keylength')
parser.add_argument('-a',  nargs=1, help='Specify alphabet')
parser.add_argument('-w',  nargs=1, help='Specify wordlist (default: {0})'.format(wordlist))

args = vars(parser.parse_args())

if args['c'] != None:
    
    f = open(args['c'][0], 'r')
    data = f.read()
    f.close
    
    if args['w'] != None:
        wordlist = args['wordlist'][0]
    
    if args['a'] != None:
        alphabet = args['alphabet'][0]


data = 'NXIS24CuEq@uEq@uEq@u'

print 'String length:    {0}'.format(len(data))
print 'Maximum keylen:   {0}'.format(max_keylength)
print 'Wordlist:         {0}'.format(wordlist)
print 'Alphabet:         {0}'.format(alphabet)

words = []

with open(wordlist, 'r') as f:
    for line in f:
        words.append(line.strip('\n'))

for keylength in range(1, max_keylength + 1):
    offset_lengths = []
    offset_plaintexts = []
    
    for offset in range(0, keylength):
        plaintexts = []
    
        for xor in range(0, 256):
            plaintext = ''.join([chr((ord(char) ^ xor) % 256) for char in data][offset::keylength])
    
            if all(char in alphabet for char in plaintext):
                plaintexts.append(plaintext)
                
        offset_plaintexts.append(list(set(plaintexts)))
        offset_lengths.append(len(plaintexts))
        
    cartesian_product = 1
    
    if all(count > 0 for count in offset_lengths):
        
        print '\nKey length {0}:    ({1})'.format(keylength, str(offset_lengths)[1:-1])
        
        for plaintext in offset_plaintexts:
            cartesian_product *= len(plaintext)
            #print str(plaintext)[1:-1]
    
        print 'Possible strings: {0}'.format(cartesian_product)
        

        print find_words(offset_plaintexts)