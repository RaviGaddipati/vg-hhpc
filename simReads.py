import random

MUT_RATE = 0.1
INDEL_RATE = 0.1
NUM_READS = 1000
READ_LEN = 100
READ_LEN_VAR = 0.5 # +/- read length
MAX_POS = 51999500
MIN_POS = 16000500
REF_FILE = 'C:\\Users\\Ravi\\OneDrive\\School\\LangmeadLab\\POASim\\data\\varSamples\\1a.fa'
OUT_FILE = 'C:\\Users\\Ravi\\OneDrive\\School\\LangmeadLab\\POASim\\data\\varSamples\\1aLarge10pr.sh'

vg = '16M-52M.vg'
vg_novar = '16M-52M_novar.vg'
out_dir = 'varSamples/1a_Alignment_10pr/'

alphabet = {0:'A', 1:'G', 2:'C', 3:'T'}

fa = open(REF_FILE, 'r')
sc = open(OUT_FILE, 'w')

sc.write('#!/bin/bash\n')

b=0
while b < NUM_READS:
	sc.write('echo simRead ' + str(b) +'\n')
	read = ''
	ambigCount = 0
	rand = random.randint(MIN_POS, MAX_POS)
	fa.seek(rand)
	read_len = int(READ_LEN + random.randint(0, READ_LEN_VAR * READ_LEN * 2) - (READ_LEN_VAR * READ_LEN))
	for c in range(read_len):
		char = fa.read(1);
		rand = random.randint(1,1000000)
		if rand < int((MUT_RATE * 1000000) / 4):
			char = 'G'
		elif rand < int((MUT_RATE * 1000000) / 2):
			char = 'C'
		elif rand < int((MUT_RATE * 1000000 * 3) / 4):
			char = 'A'
		elif rand < int(MUT_RATE * 1000000):
			char = 'T'

		rand = random.randint(1,1000000)

		if rand < int((INDEL_RATE * 1000000) / 2):
			char = ''
		elif rand < int(INDEL_RATE * 1000000):
			rand = random.randint(0,3)
			read += alphabet[rand]
		
		if char == 'N':
			ambigCount += 1
			
		if char =='\n':
			c -= 1
		else:
			read += char

	if ambigCount < READ_LEN / 2:
		sc.write('vg align -s '+ read + ' ' + vg + ' >'+ out_dir + str(b) + '_10prErr.vga &\n')
		sc.write('vg align -s '+ read + ' ' + vg_novar + ' >'+ out_dir + str(b) + '_novar_10prErr.vga &\n')
		sc.write('wait\n')
		b += 1

sc.write('echo "Done."')
fa.close()
sc.close()

