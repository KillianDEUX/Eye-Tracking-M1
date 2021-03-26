import os
import platform

def ajouterTag(nomVideo):
    syst = platform.system()

    if(syst == 'Windows'):
        lienDossier = os.getcwd().split("\\")
        lien = 'addTag.bat ' + nomVideo
    else:
        lienDossier = os.getcwd().split("/")
        lien = "./addTag.sh " + "\"" + nomVideo + "\""

    # On récupère le dossier dans lequel on est
    dossier = lienDossier[len(lienDossier) - 1]

    # Accéder au dossier si on y est pas déjà
    if dossier != "sh":
        os.chdir("sh")

    sortie=os.popen(lien, "r").read()

    os.chdir("../")
