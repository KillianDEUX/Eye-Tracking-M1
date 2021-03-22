import os
import platform
import subprocess

def ajouterTag(nomVideo):
    syst = platform.system()
    os.chdir("sh")
    if(syst == 'Windows'):
        lien = 'addTag.bat ' + nomVideo
    else:
        lien = "./addTag.sh " + nomVideo

    sortie=os.popen(lien, "r").read()


# ajouterTag("../ajout_tag/Calibration1")
