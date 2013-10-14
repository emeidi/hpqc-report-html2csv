import sys
import os

from bs4 import BeautifulSoup

def out(msg):
	# http://stackoverflow.com/questions/5419/python-unicode-and-the-windows-console
	
	if msg is None:
		return
	
	try:
		#print(msg + "\n")
		print(msg)
	except UnicodeEncodeError:
		if sys.version_info >= (3,):
			print(msg.encode('utf8').decode(sys.stdout.encoding))
		else:
			print(msg.encode('utf8'))

def cleanShittyHPFormatting(raw):
	if raw is None:
		return
	
	# Remove trailing whitespace
	raw = raw.strip()
	
	# Tab
	raw = raw.replace("\t",'')
	
	# Remove newlines
	raw = raw.replace("\r",'')
	raw = raw.replace("\n",' ');

	# Remove whitespace
	raw = ' '.join(raw.split())
	
	return raw

def dictToList(dict):
	maxlength = 0
	
	for key in dict.keys():
		length = len(key)
		
		if length > maxlength:
			maxlength = length
		
	for key in dict.keys():
		if key is None:
			continue;
		
		if key in dict:
			length = len(key)
			spaces = maxlength - length
			
			out("    " + key + ": " + (' ' * spaces) + str(dict[key]))

def dictToCSV(dict):
	out = ""
	
	for key in dict:
		out += '"' + cleanCSVString(str(dict[key])) + '"' + csvSep
	
	return out

def dictToCSVLegend(dict):
	out = '"Test Title"' + csvSep;
	
	for key in dict:
		out += '"' + cleanCSVString(str(key)) + '"' + csvSep
	
	return out
	
def cleanCSVString(raw):
	raw = raw.replace(csvSep,',')	
	raw = raw.replace('"','`')
	return raw

csvSep = ';'
	
scriptPath = os.path.abspath(__file__)
scriptDir = os.path.dirname(scriptPath)

htmlPath = scriptDir + "/Planning Report.html"
#htmlPath = scriptDir + "/Planning Report Lean.html"

csvPath = scriptDir + "/export.csv"

f = open(htmlPath, 'r')
html = f.read() #htmlPath
soup = BeautifulSoup(html)

currentTestCaseKey = 1

attribs = {}
attribsTestcase = {}
counter = 0
testcaseAttribs = soup.findAll('td',{'width':'50%'})
for testcaseAttrib in testcaseAttribs:
	counter += 1
	
	#raw = testcaseAttrib.string
	#out(raw)
	#out("Looking at row " + str(counter))
	
	rows = testcaseAttrib.findAll('tr')
	
	for row in rows:
		cells = row.findAll('td')
		
		keyValPair = []
		for cell in cells:
			html = cleanShittyHPFormatting(cell.string)
			#out(html)
			
			keyValPair.append(html)
			#if html.endswith(':'):
				# legend
		
		key = keyValPair[0]
		key = key.replace(':','')
		
		val = keyValPair[1]
		attribsTestcase[key] = val
	
	#print(attribsTestcase)
	
	if counter % 2 == 0:
		attribs[currentTestCaseKey] = attribsTestcase
		
		# next row
		currentTestCaseKey += 1
		
		# reset attribs because we have a new testcase
		attribsTestcase = {}
	
#sys.exit(0)
#print(attribs)

csv = ""
counter = 0
testcaseTitles = soup.findAll('h3')
for testcaseTitle in testcaseTitles:
	counter += 1
	
	title = cleanShittyHPFormatting(testcaseTitle.string)	
	
	out(title)
	
	if counter in attribs:
		#print(attribs[counter])
		dictToList(attribs[counter])
		csv += title + csvSep + dictToCSV(attribs[counter]) + "\n"
	else:
		out("ERROR: attribs[" + counter + "] not set. Skipping.")
		continue
		
	out("")

#print("=" * 70)
#print(csv)

csv = dictToCSVLegend(attribs[counter]) + "\n" + csv

f = open(csvPath, 'w')
f.write(csv)
f.close()