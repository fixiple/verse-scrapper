from xml.etree.ElementTree import Element, SubElement, ElementTree, tostring, dump
from pathlib import Path, PureWindowsPath 
import os

class populator:

	def __init__(self):
		global fileName
	
	@classmethod
	def getCurrentPath(self):
		""" returns the path of the current python file """
		dir_path = os.getcwd()
		return dir_path
	
	@classmethod
	def setPath(self, path=r"C:\Users\Wild\Desktop\Code\Python\Verse_helper"):
		"""
		sets the path to where the file will be stored.
		if the folder "parsedxml" doesn't exists, creates it and access it	
		"""
		try:
			path=os.chdir(path+r"\parsedxml")
			print("getting into 'parsedxml' folder...")
		except FileNotFoundError:
			print("folder not found, creating '\parsedxml'...")
			os.mkdir(path+r"\parsedxml")
			path=os.chdir(path+r"\parsedxml")
			return path
	
	
	@classmethod
	def createXmlFile(self, fileName):
		"""
		 creates the XML file with given Name
		"""

		try:
			xmlFile=open(fileName+".xml", "x") #x mode = create an empty file
			return xmlFile
			if FileExistsError:
				raise FileExistsError('file already exists')
		except FileExistsError as e:
			print(e)		
	
	
	@classmethod
	def xmlInit(self):
		"""
			requires no arguments
			this function returns the name of created file
		"""
		path=self.setPath()
		
		# to get a list of files contained inside
		# files=os.listdir(os.getcwd())
		
		try:
			name=input("filename ?:")
			if not name:
				raise TypeError('put a valid name for the xmlFile')
		except TypeError as e:
			print(e)
		
		try:
			xmlFile=self.createXmlFile(name)
		except TypeError:
			os.remove(xmlFile)
		
		# To parse a list of files and select the file with the given name
		
		# for file in files:
			# if os.path.exists('{}.xml'.format(xmlFile)) and file==fileName+'.xml':
				# print("file exists...")
				# break
			# else:
				# print("file doesn't exists")

		return xmlFile #returns the file name
	
	@classmethod
	def xmlAddNodes(self, main, *parents, **children):
		"""
		Used to add Nodes inside an xml file
		requires: 
		-  main : must be string
		-  args = parents: must be string, can take multiple arguments
		-  kwargs = children : must be string, can take multiple arguments
		Usage example: 
		xmlAddElements(YourMainNode, YourParentNode1, YourParentNode2,...,YourParentNodeN, subElem1=YourChildNode1, subElem2=YourChildNode2, subElem3=YourChildNode3, ..., subElemN=YourChildNodeN)
		"""
		file=None
		while file==None:
			file=self.xmlInit() #stores the file objet
		
		fileName=file.name
		path = self.getCurrentPath() #gets the current path
		fullfilePath=os.path.join(path, fileName) #creates the full path of the file  
		
		#debug, print the file object
		#print(file)
		
		#print(fullfilePath)
		
		topNode=Element(main)
		childNode = None
		SubChildNode = None
		
		for child in parents:
			childNode = SubElement(topNode, child)
		
		for key, value in children.items():
			#transforms the child item in a dictionnary
			#Debug :
			#print("key={} value={}".format(key, value))
			#we retrieve the value of the dictionnary on every key and store it inside subChild
			subChild=value
				#Debug :
				#print(subChild)
			SubChildNode = SubElement(childNode, subChild)
			
			#we need to pass some data for the closing tags to appear(<videoID>text</videoID> instead of <videoID/>)
			#SubChildNode.text = "Kappa"
		
		#Debug: 
		#print(dump(top))
		
		data=ElementTree(topNode)
		
		with open(fullfilePath, 'w+') as f:
			data=tostring(topNode, encoding="unicode") 
			#tostring returns a byte, need encoding='unicode' to force the change to string
			print("writing data...")
			f.write(data)
		#change permissions 0o777 ; o = Octal number
		#7*8^2+7*8^1+7*8^0 = 511 
		# corresponds to file permission code 511 
		# 5 = Owner read and execute (4+1) 
		# 1 = Group can only execute
		# 1 = World can only execute
		os.chmod(fileName, 0o777)

if __name__=="__main__":
		p1 = populator
		main="Playlist"
		# * in function argument = we unpack it, we basically just take every item in the list we pass, one by one
		p1.xmlAddNodes("Playlist", "PlaylistName", "PlaylistItems", subElem1="VideoId", subElem2="VideoTitle", subElem3="length")