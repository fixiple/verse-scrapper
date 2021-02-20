import xml.etree.ElementTree as ET
import ErrorHandling as EH
from pathlib import Path, PureWindowsPath 
#

class bibleSearch:
	"""
	DOCSTRING
	the bibleSearch class will parse through an given xml file
	
	
	
	"""
	#=========================
	#class variables
	#=========================
	
	#=========================
	#constructor
	#=========================
	def __init__(self, book, chapter, verse):
		self.book=book
		self.chapter=chapter
		self.verse=verse
	
	
	#==========================
	# Getters and Setters
	#==========================
	
	def getBook(self):
		
		return self.book
		
	def getchapter(self):
		
		return self.chapter
	
	def getverse(self):
		
		return self.verse
	
	#==========================
	#class methods
	#==========================
	@classmethod
	def parseFile(cls):
		"""
			TO DO: implement filesearch to find and parse the file selected
		"""
		file=Path("xml/bible_louis_second_french.xml")
		filePathWindows = PureWindowsPath(file)
		
		return ET.parse(file)

	@classmethod
	def showBooks(cls):
		"""
		voir l'utilité de cette methode
		shows all books available in the xml file
		"""
		#local variables
		books=cls.getBooks()
		i=1
		length=len(books) 
		
		for book in books: 
			print(book)
			# limit the itrable list to the number of books available in the list
			i+=1
			if i > length:
				break
				
				
	
	def getBooks(self):
		"""
		gets all books available in the xml file
		stores them in a list
		"""
		file=self.parseFile()
		#the head of the xml file
		root=file.getroot()
		i=1
		books=[]
		for child in root:
			books.append(child.get('bname'))
		return books
	
	def getChapters(self, book):
		"""
			returns a list of chapters available in the current book 
			of an instance of the class
		"""
		file=self.parseFile()
		
		
		chapter=[]
		
		#we find the book
		currentBook=file.find("./BIBLEBOOK/[@bname='{}']".format(book))
		
		#we get the chapter of the book and attach it in the list made declared earlier
		for currentChapter in currentBook:
			chapter.append(currentChapter.get('cnumber'))
		
		
		return chapter
		
	def getVerses(self, book, chapter):
		"""
			returns a list of verses available in the current chapter 
			of an instance of the class
		"""
		file=self.parseFile()
		verses=[]
	
		#we get the chapter of the book
		currentChapter=file.find("./BIBLEBOOK/[@bname='{}']/CHAPTER[@cnumber='{}']".format(book, chapter))
		
		for currentVerse in currentChapter:
			verses.append(currentVerse.get('vnumber'))
		
		return verses
		
	def parseBible(self, book, chapter, verse):
		"""
			returns the text of the current verse of the object
		"""
		
		
		file=self.parseFile()
		
		#we iterate through the appropriate children 
		currentVerse=file.find("./BIBLEBOOK/[@bname='{}']/CHAPTER[@cnumber='{}']/VERS[@vnumber='{}']".format(book, chapter, verse))
		try:
			return currentVerse.text
		except AttributeError:
			return "Veuillez verifier les données saisies"


# if __name__=="__main__":
	# BS1=bibleSearch("Jean",12,5)
	
	# print(BS1.parseBible(getattr(BS1,"book"),getattr(BS1,"chapter"),getattr(BS1,"verse")))