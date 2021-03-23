import cv2
import wx
import numpy as np

#fonction vide ne renvoyant rien
def nothing(emp):
    pass

#classe permettant de lire les vidéos et de les gérer
class VideoPlayer(wx.App):

    cap = [0,0,0,0]
    namedWindow = ['video1','video2','video3','video4'] #toutes les fenetres contenant les vidéos

    def load(self, videoarray):
        #Chargement des vidéos et création de leurs fenêtres
        for i in range(len(videoarray)) :
            cv2.namedWindow(self.namedWindow[i])
            cap = cv2.VideoCapture(videoarray[i])
            self.cap[i] = cv2.VideoCapture(videoarray[i])
            self.cap[i].set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.play()

    def play(self):
        loopflag = [0,0,0,0]
        pos = [0,0,0,0]
        etatVideo = ["play","play","play","play"] #on met les vidéos en route quand l'app se lance
        frame = [0,0,0,0]
        success = [False,False,False,False]
        img = [0,0,0,0]
        #on récupère la taille de l'écran et du milieu de celui-ci
        width, height = wx.GetDisplaySize()
        midWidth_Window = width / 2
        midHeight_Window = height / 2
        # récupération du nombre de frame des vidéos et création des trackbar
        for i in range(len(self.cap)) :
            frame[i] = int(self.cap[i].get(cv2.CAP_PROP_FRAME_COUNT))
            cv2.createTrackbar('time', self.namedWindow[i], 0, frame[i], nothing)


        #Affichage des controls dans une fenetre à part
        cv2.namedWindow('controls')
        controls = np.zeros((50,1000),np.uint8)
        cv2.putText(controls, "espace : pause/lecture toutes videos, a: pause/lecture video1, z : pause/lecture video2, e: pause/lecture video3, r: pause/lecture video4, q: Quitter", (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, 280)

        #première lecture des vidéos permettant la disposition des fenetres
        for i in range(len(self.cap)) :
            success[i], img[i] = self.cap[i].read()

        #s'il s'agit de vidéos rectangulaire horiuzontalement on les dispose en carré et on gère leur taille
        if(img[0].shape[1] < img[0].shape[0]):
            cvwindow = height / 1.4
            r = (cvwindow) / img[0].shape[1]
            w = img[0].shape[0] * r
            window1_width = int(midWidth_Window - cvwindow)
            window1_heigth = int(midHeight_Window - w - 80)
            cv2.moveWindow(self.namedWindow[0], window1_width, window1_heigth)
            cv2.moveWindow(self.namedWindow[1], int(midWidth_Window), window1_heigth)
            cv2.moveWindow(self.namedWindow[2], window1_width, int(midHeight_Window))
            cv2.moveWindow(self.namedWindow[3], int(midWidth_Window), int(midHeight_Window))
            cv2.moveWindow('controls',int(midWidth_Window),int(midHeight_Window))
        #s'il s'agit de vidéos carré ou rectangulaire verticalement on les dispose en ligne et on gère leur taille différemment
        else :
            cvwindow = (height / 2) - 90
            cv2.moveWindow(self.namedWindow[0], 0,0)
            cv2.moveWindow(self.namedWindow[1], int(cvwindow) ,0)
            cv2.moveWindow(self.namedWindow[2], int(cvwindow * 2),0)
            cv2.moveWindow(self.namedWindow[3], int(cvwindow * 3),0)
            cv2.moveWindow('controls',int(midWidth_Window -cvwindow),int(midHeight_Window))
            cv2.imshow("controls",controls)

        #lecture de toutes les vidéos
        while True:
            check = 0
            for i in range(len(self.cap)) :
                if etatVideo[i] == "play":
                    #si la trackbar est au meme niveau que la position on set la trackar
                    if loopflag[i] == pos[i]:
                        loopflag[i] = loopflag[i] + 1
                        cv2.setTrackbarPos('time', self.namedWindow[i], loopflag[i])
                    #sinon on récupère la valeur et on met la vidéo à la bonne frame
                    else:
                        pos[i] = cv2.getTrackbarPos('time', self.namedWindow[i])
                        loopflag[i] = pos[i]
                        self.cap[i].set(cv2.CAP_PROP_POS_FRAMES, pos[i])
                else:
                    pos[i] = cv2.getTrackbarPos('time', self.namedWindow[i])
                    loopflag[i] = pos[i]
                    self.cap[i].set(cv2.CAP_PROP_POS_FRAMES, pos[i])

                success[i], img[i] = self.cap[i].read()

                #
                if(img[0].shape[1] < img[0].shape[0]):
                    cvwindow = height / 1.4
                else:
                    cvwindow = (height / 2) - 90
                r = cvwindow / img[i].shape[1]
                dim = (int(cvwindow), int(img[i].shape[0] * r))
                img[i] = cv2.resize(img[i], dim, interpolation = cv2.INTER_AREA)
                if img[i].shape[0]>600:
                    img[i] = cv2.resize(img[i], (500,500))
                    controls = cv2.resize(controls, (img[i].shape[1],25))



            # Si les vidéos ont bien été chargées
            if success[0] == True and success[1] == True and success[2] == True and success[3] == True:
                for i in range(len(self.cap)) :
                    if etatVideo[i] == "play":
                        cv2.imshow(self.namedWindow[i], img[i])


                key = cv2.waitKey(1) & 0xFF

                #Si la touche q est pressée on ferme tous
                if key == ord("q"):
                    break

                #si une vidéo est terminée on la met en pause
                for i in range(len(self.cap)) :
                    if etatVideo[i] == "play":
                        if loopflag[i] == frame[i]-1:
                            etatVideo[i] = "pause"
                            loopflag[i] = 0

                #si la touche espace est pressée, on met toutes les vidéos en pause ou en route
                if key == ord(" "):
                    for i in range(len(self.cap)) :
                        if etatVideo[i] == "play":
                            check += 1
                    if check == len(self.cap):
                        for i in range(len(self.cap)) :
                            etatVideo[i] = "pause"
                    if check == 0:
                        for i in range(len(self.cap)) :
                            if(loopflag[i] != frame[i]-1):
                                etatVideo[i] = "play"
                    else:
                        for i in range(len(self.cap)) :
                            etatVideo[i] = "pause"

                #quand la touche a est pressée : pause ou play de la première vidéo en fct de son état
                if key == ord("a"):
                    if etatVideo[0] == "pause" and loopflag[0] != frame[0]-1:
                      etatVideo[0] = "play"
                    else:
                      etatVideo[0] = "pause"
                #quand la touche a est pressée : pause ou play de la première vidéo en fct de son état
                if key == ord("z"):
                    if etatVideo[1] == "pause" and loopflag[1] != frame[1]-1:
                      etatVideo[1] = "play"
                    else:
                      etatVideo[1] = "pause"

                #quand la touche a est pressée : pause ou play de la première vidéo en fct de son état
                if key == ord("e"):
                    if etatVideo[2] == "pause" and loopflag[2] != frame[2]-1:
                      etatVideo[2] = "play"
                    else:
                      etatVideo[2] = "pause"
                #quand la touche a est pressée : pause ou play de la première vidéo en fct de son état
                if key == ord("r"):
                    if etatVideo[3] == "pause" and loopflag[3] != frame[3]-1:
                      etatVideo[3] = "play"
                    else:
                      etatVideo[3] = "pause"
            # Break the loop
            else:
                break


        for i in range(len(self.cap)) :
            self.cap[i].release()

        cv2.destroyAllWindows()
