from bibleSearch import *
import PySimpleGUI as sg
import os
import ErrorHandling as EH

#-----------------------------------------
# relire la doc pysimpleGUI
# implementer une genre de suggestion lors de l'écriture du livre, du chapitre, du verset(utiliser getchapters, getbooks,getversets)
# trouver moyen d'afficher text(.txt) en bold ou en italique (changer en .rtf?)
# use regular expressions to parse book with similar names (in bibleSearch)
# ajouter un bouton dans le popup des versets permettant de les enregistrer(les versts courants affichées)
# --> creer une liste avec les differents instances d'objets à l'intérieur puis iterer dedans et recu les versets
# ajouter un bouton permettant d'ajouter les versets enregistrées dans le fichier xml concernant l'église (freeworship)
# export app from .py to .exe
#-----------------------------------------



def main_window():
	layout = [[sg.Text('book'), sg.Input(do_not_clear=(False))],
          [sg.Text('chapter'), sg.Input(do_not_clear=(False))],
          [sg.Text('verse'), sg.Input(size=(15,1),do_not_clear=(False)),sg.Text('to'), sg.Input(size=(15,1),do_not_clear=(False))],
          [sg.Button('parse', key='-RECH-', bind_return_key=True), sg.Button('reset')] ]

	window = sg.Window('Verse Helper', layout, return_keyboard_events=True, auto_close=False)
	
	return window
	

def main():
	window=main_window()
	
	while True:
	#using rtf because txt doesn't have text decorators??(check for texdecorators in txt file)
	#we check if the file already exists
		if os.path.isfile("/fichier.txt"):#returns true if exists
			os.remove("fichier.txt")
		else:
			pass
	
		event, values = window.read()
		if event == '-RECH-':
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
		


			with open("fichier.txt","w") as w:
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
						w.write(versetext+"\n")	
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
		
		elif event == None:
			#we check if the file still exists
			if os.path.isfile("/fichier.txt"): #returns true if exists
				os.remove("fichier.txt")
			
			window.close()
			break

if __name__ == '__main__':
    main()
		
