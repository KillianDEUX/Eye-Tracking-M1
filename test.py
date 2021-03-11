import cv2
import numpy as np
import os
import wx
import wx.lib.statbmp as SB
from PIL import Image
from wx.lib.pubsub import pub
PhotoMaxSize = 240

frameWidth = 640
frameHeight = 480


class VideoPlayer():

    cap = [0,0,0,0]

    def load(self, videoarray):
        #Chargement vidéo 1
        self.cap[0] = cv2.VideoCapture(videoarray[0])
        self.cap[0].set(1, frameWidth)
        self.cap[0].set(1, frameHeight)

        #Chargement vidéo 2
        self.cap[1] = cv2.VideoCapture(videoarray[1])
        self.cap[1].set(1, frameWidth)
        self.cap[1].set(1, frameHeight)

        #Chargement vidéo 2
        self.cap[2] = cv2.VideoCapture(videoarray[2])
        self.cap[2].set(1, frameWidth)
        self.cap[2].set(1, frameHeight)

        #Chargement vidéo 2
        self.cap[3] = cv2.VideoCapture(videoarray[3])
        self.cap[3].set(1, frameWidth)
        self.cap[3].set(1, frameHeight)
        self.play()

    # Affichage des vidéos dans la même fenêtre
    def stackImages(imgArray,scale,lables=[]):

        sizeW = imgArray[0][0].shape[1]
        sizeH = imgArray[0][0].shape[0]
        rows = len(imgArray)
        cols = len(imgArray[0])
        rowsAvailable = isinstance(imgArray[0], list)
        width = imgArray[0][0].shape[1]
        height = imgArray[0][0].shape[0]

        if rowsAvailable:
            for x in range ( 0, rows):
                for y in range(0, cols):
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (sizeW, sizeH), None, scale, scale)
                    if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
            imageBlank = np.zeros((height, width, 3), np.uint8)
            hor = [imageBlank]*rows
            hor_con = [imageBlank]*rows
            for x in range(0, rows):
                hor[x] = np.hstack(imgArray[x])
                hor_con[x] = np.concatenate(imgArray[x])
            ver = np.vstack(hor)
            ver_con = np.concatenate(hor)

        else:
            for x in range(0, rows):
                imgArray[x] = cv2.resize(imgArray[x], (sizeW, sizeH), None, scale, scale)
                if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
            hor= np.hstack(imgArray)
            hor_con= np.concatenate(imgArray)
            ver = hor

        if len(lables) != 0:
            eachImgWidth= int(ver.shape[1] / cols)
            eachImgHeight = int(ver.shape[0] / rows)
            print(eachImgHeight)
            for d in range(0, rows):
                for c in range (0,cols):
                    cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                    cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
        return ver

    def play(self):
        while True:
            # Lecture vidéo 1
            success, img = self.cap[0].read()
            # Lecture vidéo 2
            success2, img2 = self.cap[1].read()
            success3, img3 = self.cap[2].read()
            success4, img4 = self.cap[3].read()
            kernel = np.ones((5,5),np.uint8)
            print(kernel)
            print(success, success2, success3,success4)
            # Si les vidéos ont été chargées
            if success == True and success2 == True and success3 == True and success4 == True:
                print("oui")
                StackedImages = self.stackImages(([img,img2],
                                               [img3,img4]),0.2)
                cv2.imshow("Staked Images", StackedImages)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            # Break the loop
            else:
                break


class DropTarget(wx.FileDropTarget):

    def __init__(self, widget):
        wx.FileDropTarget.__init__(self)
        self.widget = widget

    def OnDropFiles(self, x, y, filenames):
        print(filenames[0])
        pub.sendMessage('dnd', filepath=filenames[0])
        return True


class PhotoCtrl(wx.App):

    video = ["","","",""]

    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = wx.Frame(None, title='Photo Control')
        self.panel = wx.Panel(self.frame)
        pub.subscribe(self.update_image_on_dnd, 'dnd')
        self.createWidgets()
        self.frame.Show()

    def createWidgets(self):
        instructions = 'Browse for an image or Drag and Drop'
        img = wx.Image(240,240)
        self.imageCtrl = SB.GenStaticBitmap(self.panel, wx.ID_ANY, wx.Bitmap(img))
        filedroptarget = DropTarget(self)
        self.imageCtrl.SetDropTarget(filedroptarget)
        instructLbl = wx.StaticText(self.panel, label=instructions)
        self.photoTxt = wx.TextCtrl(self.panel, size=(200,-1))
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                           0, wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(instructLbl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        self.sizer.Add(self.photoTxt, 0, wx.ALL, 5)
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        self.panel.Layout()

    def update_image_on_dnd(self, filepath):
        fin = 0
        j = 0
        for i in range(4):
            if(fin == 0):
                if(self.video[i] == ""):
                    self.video[i] = filepath
                    fin = 1

        print(self.video)
        for i in range(4):
            if(self.video[i] != ""):
                j+=1

        if(j == 4):
            self.frame.Destroy()
            VideoPlayer().load(self.video)



if __name__ == '__main__':
    app = PhotoCtrl()
    app.MainLoop()
