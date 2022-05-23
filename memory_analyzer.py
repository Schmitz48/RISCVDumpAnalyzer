import re
import string

hex_values = set(string.digits + 'a'+'b'+'c'+'d'+'e'+'f')


def isBadLine(line):
	return line[0] == 'b' or line[0] == 'D'

def isHex(instruction):
	return set(instruction) <= hex_values and instruction != 'add'



addresses = []
dump_val = []
dump = []
miss_alligned_val = []
addr = 0x80000000
addresses_log = []
val_log = []

t = 0
hit_three_dots = 0
with open('dump.s','r') as file: # adjust the input file name/path
	for line in file:

		if not line.isspace() and not isBadLine(line):

			#three possibilities for first word in line: address of new section -> skip over; address of instruction -> insert; ... -> mark and fill gaps with 00000000

				#print(hex(addr))

			if(line.split()[0] == '...'):
				addr = addr
			else:#(int(inst_address,16) == int(addr)):
				#alligned
				inst_address = int(line.split()[0].split(':')[0],16)
				if(not line.split()[1][0] == '<'): #address of new section -> skip over;
					#in case of ...
					if(addr < inst_address):
						while(addr < inst_address):
							addr = addr + 2 #increment address
							miss_alligned_val.append('0000')
							if(len(miss_alligned_val)==2):
								dump_val.append(miss_alligned_val[1]+miss_alligned_val[0])
								miss_alligned_val.clear()
								addresses.append((hex(addr-2)))
								dump.append(zip(hex(addr-2),dump_val[-1]))
					if((addr)%4 == 0):
						
					#alligned long instruction just commit
						split_id = 1
						while(isHex(line.split()[split_id])):
							if(len(line.split()[split_id])>4):
								addresses.append(hex(addr))
								dump_val.append(line.split()[split_id])
								dump.append(zip(hex(addr-2),dump_val[-1]))
								addr = addr + 4 #increment address
							else:#first compressed instruction mybe also third
								miss_alligned_val.append(line.split()[split_id])
								addr = addr + 2
								if(len(miss_alligned_val)==2):
									dump_val.append(miss_alligned_val[1]+miss_alligned_val[0])
									miss_alligned_val.clear()
									addresses.append((hex(addr)))
									dump.append(zip(hex(addr-2),dump_val[-1]))

									#miss_alligned_val.append(line.split()[1][len(miss_alligned_val)*4:len(miss_alligned_val)*4+4])

							#misalligned
							split_id = split_id + 1
					else:
						split_id = 1
						while(isHex(line.split()[split_id])):
							if(len(line.split()[1])>4):
								addr = addr + 4 #increment address
								miss_alligned_val.append(line.split()[split_id][len(miss_alligned_val)*4:len(miss_alligned_val)*4+4])
								if(len(miss_alligned_val)==2):
									dump_val.append(miss_alligned_val[1]+miss_alligned_val[0])
									miss_alligned_val.clear()
									addresses.append((hex(addr-4)))
									dump.append(zip(hex(addr-4),dump_val[-1]))
								miss_alligned_val.append(line.split()[split_id][len(miss_alligned_val)*4:len(miss_alligned_val)*4+4])
							else:#first compressed instruction
								miss_alligned_val.append(line.split()[split_id])
								addr = addr + 2
							#misalligned
							if(len(miss_alligned_val)==2):
								dump_val.append(miss_alligned_val[1]+miss_alligned_val[0])
								miss_alligned_val.clear()
								addresses.append((hex(addr-4)))
								dump.append(zip(hex(addr-4),dump_val[-1]))
							#misalligned
							split_id = split_id + 1



with open('~/putty.log','r') as file: # adjust the input file name/path
	print('cutecom')
	for line in file:
			j = 0
			for word in line.split():
				if j == 0:
					addresses_log.append('0x' + word.split(';')[0])
					if(word.split(';')[0] == '80bfc'):
						for it in range(29):
							addresses_log.append('0x' + word.split(';')[0])
							val_log.append(line.split()[1])

					j = 1
				elif j == 1:
					j = 0
					if(not word.split(';')[0] == '80bfc'):
						val_log.append(line.split()[1])

coupled_idx = enumerate(zip(val_log, dump_val))
res = next( (idx for idx, (x, y) in coupled_idx if x!=y), None )

n = 0
diff_ids = []
for item in val_log:

	if dump_val[n] != item:
		diff_ids.append(n)
	n = n+1

print(res)
print('Log: ')
print(addresses_log[res] , end='')
print('; ', end='')
print(val_log[res])
print('Expected: ')
print(addresses[res] , end='')
print('; ', end='')
print(dump_val[res])
kk = 0


#with open('memory.csv','w') as file:
#	for i in range(1000000):
#		file.write(addresses_log[i] + ',' + dump_val[i] + ',' + val_log[i] + ',' +',' + '=IDENTISCH(B' + str(i+1) + ';C' + str(i+1) + ')\n')
#with open('memory1.csv','w') as file:
#	for i in range(1000000,2000000):
#		file.write(addresses_log[i] + ',' + dump_val[i] + ',' + val_log[i] + ',' +',' + '=IDENTISCH(B' + str(i+1 -1000000) + ';C' + str(i+1-1000000) + ')\n')
#with open('memory2.csv','w') as file:
#	for i in range(2000000,3000000):
#		file.write(addresses_log[i] + ',' + dump_val[i] + ',' + val_log[i] + ',' +',' + '=IDENTISCH(B' + str(i+1-2000000) + ';C' + str(i+1-2000000) + ')\n')
#with open('memory3.csv','w') as file:
#	for i in range(3000000,4000000):
#		file.write(addresses_log[i] + ',' + dump_val[i] + ',' + val_log[i] + ',' +',' + '=IDENTISCH(B' + str(i+1-3000000) + ';C' + str(i+1-3000000) + ')\n')
#with open('memory4.csv','w') as file:
#	for i in range(4000000,5000000):
#		file.write(addresses_log[i] + ',' + dump_val[i] + ',' + val_log[i] + ',' +',' + '=IDENTISCH(B' + str(i+1-4000000) + ';C' + str(i+1-4000000) + ')\n')
#with open('memory5.csv','w') as file:
#	for i in range(5000000,6000000):
#		file.write(addresses_log[i] + ',' + dump_val[i] + ',' + val_log[i] + ',' +',' + '=IDENTISCH(B' + str(i+1-5000000) + ';C' + str(i+1-5000000) + ')\n')
#with open('memory6.csv','w') as file:
#	for i in range(6000000,len(dump_val)):
#		file.write(addresses_log[i] + ',' + dump_val[i] + ',' + val_log[i] + ',' +',' + '=IDENTISCH(B' + str(i+1-6000000) + ';C' + str(i+1-6000000) + ')\n')

