import cv2

class VideoCalibration():

    def lire(self):
        cap = cv2.VideoCapture('../Videos/VideoCalibrationV1.mp4')
        cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Frame",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        if (cap.isOpened()== False):
          print("Error opening video stream or file")

        # Pour mettre la vidéo en pause à l'ouverture
        ouverture = True
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:

                cv2.imshow('Frame', frame)
                key = cv2.waitKey(50)

                # q pour quitter
                if key == ord('q'):
                    break

                # Mettre la vidéo en pause au début ou si elle vient d'être lancée
                if key == ord(' ') or ouverture:
                    cv2.waitKey(-1)
                    ouverture = False
            else:
                break

        cap.release()
        cv2.destroyAllWindows()
