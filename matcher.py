import json
from pprint import pprint
import os.path

align_dir = 'C:\\Users\\Ravi\\OneDrive\\School\\LangmeadLab\\POASim\\data\\varSamples\\1a_Alignment_10pr\\'
outputFile = 'C:\\Users\\Ravi\\OneDrive\\School\\LangmeadLab\\POASim\\data\\varSamples\\1a_Alignment_10pr\\alignments.csv'
align_suffix = '_10prErr.vga'
alignNoVar_suffix = '_novar_10prErr.vga'
NUMREADS = 1000

output = open(outputFile, 'w')
output.write('sequence, var score - novar score, overlap\n')

def alignDS(alignment):
	# Pull data from JSON alignment record
	# returns list of positions with assosciated offsets and edits
	# [[position, offset, [[edit 1],[edit2], ...]], ... ]
	alignmentNodes = []
	for i in alignment['path']['mapping']:
		edits = []
		node = []
		node.append(i['position']['node_id'])
		if 'offset' in i['position']:
			node.append(i['position']['offset'])
		else:
			node.append(0)
		for e in i['edit']:
			editPair = []
			if 'from_length' in e:
				editPair.append(e['from_length'])
			else:
				editPair.append(0)
			if 'to_length' in e:
				editPair.append(e['to_length'])
			else:
				editPair.append(0)
			edits.append(editPair)
		node.append(edits)
		alignmentNodes.append(node)
	return alignmentNodes

def main():
	match = 0
	total = 0
	avgScoreDiff = 0
	for readNum in range(0,NUMREADS):		
		
		# Load JSON data
		if not os.path.exists(align_dir + str(readNum) + align_suffix) or not os.path.exists(align_dir + str(readNum) + alignNoVar_suffix):
			print(str(readNum) + ' not found.')
			break
		with open(align_dir + str(readNum) + align_suffix) as dat:
			alignment = json.load(dat)
		with open(align_dir + str(readNum) + alignNoVar_suffix) as dat:
			alignmentNoVar = json.load(dat)

		# Make sure both files are for the same seq
		if not 'sequence' in alignment:
			print('Error: no sequence in ' + str(readNum) + align_suffix)
			quit()
		if not 'sequence' in alignmentNoVar:
			print('Error: no sequence in ' + str(readNum) + alignNoVar_suffix)
			quit()
		if alignment['sequence'] != alignmentNoVar['sequence']:
			print('Error: sequence mismatch in ' + str(readNum) + '\n')
		else:
				output.write('{0: <152}'.format(alignment['sequence'] + ',') + '{0: <10}'.format(str(alignment['score'] - alignmentNoVar['score']) + ','))
		avgScoreDiff += alignment['score'] - alignmentNoVar['score']
		alignDat = alignDS(alignment)
		alignNoVarDat = alignDS(alignmentNoVar)
		overlap = 0

		#Compute the overlapping regions in the same node
		# Each posiion in alignDat
		for pa in alignDat:
			# Each position in alignNoVarDat
			for pb in alignNoVarDat:
				# if same same node
				if pa[0] == pb[0]:
					pbMax = pb[1]
					# For each edit, add e[n] bp's
					for e in pb[2]:
						if e[0] >= e[1]:
							pbMax += e[0]
						else:
							pbMax += e[1]
					# Check if there's overlap in this node
					if (pbMax - pa[1]) > 0:
						overlap += pbMax - pa[1]

		output.write('{0: <10}'.format(str(overlap)) + '\n')
		if overlap > 0:
			match += 1
		else:
			print('\n Mismatch at read ' + str(readNum) + ':')
			pprint(alignDat)
			print('\n')
			pprint(alignNoVarDat)
		total += 1
	avgScoreDiff = avgScoreDiff / 1000
	output.write('#Matches: ' + str(match) + '/' + str(total) + '. Average score difference: ' + str(avgScoreDiff) + '\n')
	output.close()


if __name__ == "__main__":
	main()

