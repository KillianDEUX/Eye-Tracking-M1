from tkinter import *
import webbrowser
from src import dragAndDrop
from src import videoCalibration
import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton
from PyQt5.QtCore import Qt, QUrl
from tkinter import messagebox

# Se rendre sur le site Pupil Lab
def ouvrirPupilSiteWeb():
    webbrowser.open_new('https://pupil-labs.com')

# Listener bouton génération vidéo avec Code QR
def genererQRCode():
    app = QApplication(sys.argv)
    demo = dragAndDrop.AppDemo(True)
    demo.show()
    app.exec_()
    del app

# Listener bouton lire 4 vidéos simultanément
def lire4Videos():
    app = QApplication(sys.argv)
    demo = dragAndDrop.AppDemo(False)
    demo.show()
    app.exec_()
    del app

# Lire la vidéo de calibration
def lireVideo():
    messagebox.showinfo('Instruction','Appuyez sur la touche espace pour lancer la vidéo ou la mettre en pause. Et sur la touche q pour quitter')
    vid = videoCalibration.VideoCalibration()
    vid.lire()

# Pop up quitter
def on_closing():
    if messagebox.askokcancel("Quit", "Souhaitez-vous quitter l'application?"):
        fenetre.destroy()


background = "#4065A4"

#Création de la fenêtre
fenetre = Tk()
fenetre.title("Application Eye-Tracking Pupil Core")
fenetre.config(background=background)

# Centrer la fenêtre
largeurEcran = fenetre.winfo_screenwidth()
hauteurEcran = fenetre.winfo_screenheight()
hauteurFenetre = int(hauteurEcran / 1.7)
largeurFenetre = int(largeurEcran /  1.7)
x = int((largeurEcran/2) - (largeurFenetre/2))
y = int((hauteurEcran/2) - (hauteurFenetre/2))
fenetre.geometry("{}x{}+{}+{}".format(largeurFenetre, hauteurFenetre, x, y))

# Frame
frame = Frame(fenetre, bg=background)

# Texte bienvenue
label_bienvenu = Label(frame, text="Bienvenue sur l'application", font=("Helvetica",40), bg=background, fg='#FFFFFF')
label_bienvenu.pack()

# Logo (gratuit pixabay : https://pixabay.com/fr/vectors/audio-bouton-jouer-bleu-159307/)
l = 165
L = 165
imageLogo = PhotoImage(file="Images/logo.png").zoom(1).subsample(4)
canvas = Canvas(frame, width=l, height=L, bg='#4065A4', highlightthickness=0)
canvas.create_image(l/2, L/2, image=imageLogo)
canvas.pack(pady=10)

# Boutons

# Vidéo QR code
gen_vidQR = Button(frame, text="Générer une vidéo avec les codes QR",
    font=("Courier",20), fg=background, command=genererQRCode)

# Vidéo calibration
voir_viCali = Button(frame, text="Voir la vidéo de calibration",
    font=("Courier",20), fg=background, command=lireVideo)

# 3 vidéo
reg_3vid = Button(frame, text="Regarder 4 vidéos simultanément",
    font=("Courier",20), fg=background, command=lire4Videos)

# Site pour les lunettes
pupil_core = Button(frame, text="Accéder au site Pupil-Lab",
    font=("Courier",20), fg=background, command=ouvrirPupilSiteWeb)

gen_vidQR.pack(pady=15, fill=X)
voir_viCali.pack(pady=10, fill=X)
reg_3vid.pack(pady=10, fill=X)
pupil_core.pack(pady=10, fill=X)

frame.pack(expand=YES)

fenetre.protocol("WM_DELETE_WINDOW", on_closing)

fenetre.mainloop()
