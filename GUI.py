from bibleSearch import *
import PySimpleGUI as sg
import os
import ErrorHandling as EH
from pathlib import PurePath 
from xml.etree.ElementTree import parse

#-----------------------------------------
# relire la doc pysimpleGUI
# implementer une genre de suggestion lors de l'écriture du livre, du chapitre, du verset(utiliser getchapters, getbooks,getversets)
# trouver moyen d'afficher text(.txt) en bold ou en italique (changer en .rtf?)
# use regular expressions to parse book with similar names (in bibleSearch)
# ajouter un bouton dans le popup des versets permettant de les enregistrer(les versts courants affichées)
# --> creer une liste avec les differents instances d'objets à l'intérieur puis iterer dedans et recu les versets
# ajouter un bouton permettant d'ajouter les versets enregistrées dans le fichier xml concernant l'église (freeworship) (en train!)
# export app from .py to .exe
#-----------------------------------------

def xmlParser(Path):
	tree = parse(Path)
	root = tree.getroot()
	bible = None
	for parent in root[0]:
		#DEBUG
		#print(parent)
		for child in parent:
			#DEBUG
			#print(child.text)
			if child.text=="Bible ().xml":
				bible = child.text
				break
	return bible
	
	
	
def main_window():
# "target" a specific element, needs to get an "enable_events=True", to trigger an event, if this specific element changes
	layout = [[sg.Text('book'), sg.Input(do_not_clear=(False))],
          [sg.Text('chapter'), sg.Input(do_not_clear=(False))],
          [sg.Text('verse'), sg.Input(size=(15,1),do_not_clear=(False)),sg.Text('to'), sg.Input(size=(15,1),do_not_clear=(False))],
          [sg.Button('parse', key='-RECH-', bind_return_key=True), sg.FileBrowse('XML File', target='-T-', file_types = [("fws", '*.fws')]), sg.Text('Church file not selected', font=('bold'), text_color="Red", key='-TEXT-')], 
		  [sg.Input('', key='-T-', visible=False, enable_events=True)]]

	window = sg.Window('Verse Helper', layout, return_keyboard_events=True, auto_close=False)
	
	return window
	

def main():
	window=main_window()
	pathOfFile=os.getcwd()
	#DEBUG
	#print(pathOfFile+"\fichier.txt")
	#we check if the file already exists and we remove it
	if os.path.isfile(pathOfFile+"\\fichier.txt"):#returns true if file exists
		os.remove(pathOfFile+"\\fichier.txt")

	while True:
	#using rtf because txt doesn't have text decorators??(check for texdecorators in txt file)
		event, values = window.read()
		#DEBUG
		#print(values)
		if event == None:
			#we check if the file still exists
			if os.path.isfile(pathOfFile+"\\fichier.txt"): #returns true if exists
				print("file still there")
				os.remove(pathOfFile+"\\fichier.txt")
				print("now file is deleted")
			print("now Closing GUI")
			break
		elif event == '-RECH-':
			try:
				livre = values[0]
				chap = int(values[1])
				Debut = int(values[2])
				Fin = int(values[3])
			except (EH.NomDeLivreInvalide, EH.ChapitreInvalide, EH.VersetInvalide, ValueError, TypeError) as e:
				if (e==ValueError and e==EH.NomDeLivreInvalide or e==EH.ChapitreInvalide or e==EH.VersetInvalide or e==TypeError):
					sg.Popup("Veuillez écrire la bonne donnée dans les champs concernés!")
					continue
				else:
					sg.Popup("Erreur: ", e)
					continue
			
			with open("fichier.txt","x") as w:
				print("file created")
				try:
					BS1=bibleSearch(livre,chap,Debut)
				except NameError:
					sg.Popup("Hi")
				
				#recupère le livre de l'instance en cours
				livreobtenu=BS1.getBook()
				#chapitreobtenu=BS1.getattr(BS1, chapter)
				
				w.write(livreobtenu+"\n")
				try:
					for verse in range(Debut, Fin+1):
						versetext=BS1.parseBible(livre, chap, verse)
						w.write(str(verse)+". "+versetext+"\n")	
				except EH.ParsingError as e:
					sg.Popup("Erreur: ", e)
					continue
			with open("fichier.txt","r") as r:
				#ouverture du fichier en mode lecture
				text=r.read()
				
				n=0
				while n<1:
					#ouverture d'une popup avec le contenu du texte
					sg.PopupScrolled(text, title="Verses")
					n=n+1
					if n > 1:
						break
		elif event == '-T-':
			
			#storing the value of -T- event
			val = values["-T-"]
			
			#TO DO: file selection of church XML file -DONE- (later automate to find it? -LATER-)
			print("event change Triggered in '-T-'")
			
			if PurePath(val).match('*.fws'):
				print("selected an xml file")
				window['-TEXT-'].update(text_color="Green")
				window['-TEXT-'].update("XML File Selected")
			else:
				sg.popup("Select an .fws file, please!")
			
			parsed=xmlParser(val)
			print(parsed)
			# TODO : 
			# 1) find a way to get the path where the freeworship docs are installed by the user
			# 2) navigate towards the Bible.xml file used by freeworship 
			# 3) add the data
			
			continue



if __name__ == '__main__':
    main()
		
