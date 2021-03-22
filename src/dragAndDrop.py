import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton
from PyQt5.QtCore import Qt, QUrl
from src import ajoutTag
from tkinter import messagebox
from src import videoPlayer

video = []
generationTag = True

class ListBoxWidget(QListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(325, 200)
        self.bool = bool

    def verifierExistanceFichier(self, filePath):
        try:
            with open(filePath, 'r') as f:
                return True
        except FileNotFoundError as e:
            return False
        except IOError as e:
            return False

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                # On récupère l'extension du fichier
                if url.isLocalFile():
                    fichier = str(url.toLocalFile()).split(".")
                    extension = fichier[len(fichier) - 1]
                    # Ne récupérer que les mp4
                    if extension == "mp4":
                        if generationTag and len(video) < 1:
                            # Suppresion de l'extension
                            del(fichier[len(fichier) - 1])
                            fichAGen = "".join(fichier) + "-tag.mp4"
                            # Vérifier que le fichier tag n'existe pas déjà
                            if not self.verifierExistanceFichier(fichAGen):
                                links.append(str(url.toLocalFile()))
                                video.append("".join(fichier))
                                print(video)
                                self.addItems(links)
                            else :
                                messagebox.showinfo('Désolé','La vidéo avec les tags existe déjà')

                        elif len(video) < 4:
                            links.append(str(url.toLocalFile()))
                            video.append(str(url.toLocalFile()))
                            print(video)
                            self.addItems(links)

        else:
            event.ignore()

class AppDemo(QMainWindow):
    def __init__(self, bool):
        super().__init__()
        self.resize(500, 200)
        global video
        video = []
        global generationTag
        generationTag = bool

        self.listbox_view = ListBoxWidget(self)

        if bool :
            self.btn = QPushButton('Générer la vidéo', self)
            self.btn.clicked.connect(lambda: print(self.generVideoQR()))
        else :
            self.btn = QPushButton('Lire les vidéos', self)
            self.btn.clicked.connect(lambda: print(self.lireVideos()))

        self.btn.setGeometry(340, 75, 150, 50)

    def generVideoQR(self):
        # Si la vidéo à générer existe
        if video :
            ajoutTag.ajouterTag(video[0])
            messagebox.showinfo('Bravo!','Votre vidéo a été générée dans le même dossier que le fichier d\'origine')
            self.close()

    def lireVideos(self):
        # Si la vidéo à générer existe
        if len(video) == 4 :
            self.close()
            videoPlayer.VideoPlayer().load(video)
