###############################################################################
#
#  This program read the tiff.metadeta file and find the temperture
#  and the Direct Intesity of the X'ray beam and write it into a differnt file
#
#
################################################################################

import numpy as np
import os,sys
import glob
import re

def Temp_Intensity():
	path=os.path.join(os.getcwd())
	print path
	#A = glob.glob(os.path.join(path, '*.metadata')) 
	A = glob.glob('*metadata')
	A = np.sort(A)
	
	# Write Temperture data and Direct Intensity of
	# X-ray's ( Before hiting the sample S[5]) data  in the (metadata) file to 2 differnet files
	f = open("Temp.dat","w")
	f1 = open("I0.dat","w")
	
	for file in A:
		file1 = open(file,"r")
		for line in file1:
        		if 'temperature' in line:
				y=(line.split("temperature=")[1])
				y1=re.sub('["]', '', y)
				y1=float(y1)
				f.write("%f \n" %y1)
			if 'S[5]' in line:
				s = (line.split('S[5]=')[1])
				s = s.partition('S')
				s1 = re.sub('["]', '', s[0])
				s1 = float(s1)
				f1.write("%s \n" %s1)
						
	f.close()
	f1.close()	

if __name__ == "__main__":
    Temp_Intensity()
    
