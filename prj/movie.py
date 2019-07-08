import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import datetime
import numpy as np

now = datetime.datetime.now()
dirname = 'test_{0:%Y%m%d}'.format(now)

class QtCapture(QtWidgets.QWidget):
    def __init__(self, *args):
        super(QtWidgets.QWidget, self).__init__()

        self.video_frame = QtWidgets.QLabel()
        lay = QtWidgets.QVBoxLayout()
        lay.setContentsMargins(0,0,0,0)
        lay.addWidget(self.video_frame)
        self.setLayout(lay)

        self.capture = None
        self.cap = cv2.VideoCapture('sample.mp4')
        
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) 
        self.video_len_sec = self.cap.get(cv2.CAP_PROP_FRAME_COUNT) // self.fps
        self.setFPS(1)
        
        self.start()
       
        # My webcam yields frames in BGR format
#        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#        self.frame = frame
#        self.img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
#        pix = QtGui.QPixmap.fromImage(self.img)
#        self.video_frame.setPixmap(pix)


        # ------ Modification ------ #
        self.isCapturing = False
        self.ith_frame = 1
        # ------ Modification ------ #
        

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        
        self.setWindowTitle('Control Panel')
        self.setGeometry(100,100,200,200)
        self.show()
        

    def optical_flow(self):

        ret, frame2 = self.cap.read()
        next = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(self.prev, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

#        self.hsv[...,0] = ang*180/np.pi/2
#        self.hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
#        rgb = cv2.cvtColor(self.hsv,cv2.COLOR_HSV2BGR)
    
        res_show = mag / mag.max()
        res_show = np.floor(res_show * 255)
        res_show = res_show.astype(np.uint8)
        res_show = cv2.applyColorMap(res_show, cv2.COLORMAP_JET)

        alpha = 0.6
        return cv2.addWeighted(frame2, alpha, res_show, 1 - alpha, 0)


    def setFPS(self, fps):
        self.fps = fps


    def nextFrameSlot(self):
        ret, frame = self.cap.read()        
        self.prev = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.hsv = np.zeros_like(frame)
        self.hsv[..., 1] = 255
        frame = self.optical_flow()
#        ret, frame = self.cap.read()
        # My webcam yields frames in BGR format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QtGui.QImage(frame, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)

    def start(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(self.video_len_sec)

    def stop(self):
        self.timer.stop()

    # ------ Modification ------ #
    def capture(self):
        if not self.isCapturing:
            self.isCapturing = True
        else:
            self.isCapturing = False
    # ------ Modification ------ #

    def deleteLater(self):
        self.cap.release()
        super(QtWidgets.QWidget, self).deleteLater()



        
#    def paintEvent(self, event):
#        
#        qp = QtGui.QPainter()
##        br = QtGui.QBrush(QtGui.QColor(100, 10, 10, 40)) 
##        qp.setBrush(br)
#        frame = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888)
#        qp.begin(frame)
#        pen = QtGui.QPen(Qt.red, 2, Qt.SolidLine)
#        qp.setPen(pen)   
#        
#        qp.drawRect(QtCore.QRect(self.begin, self.end))
#        
#        pix = QtGui.QPixmap.fromImage(frame)
#        self.video_frame.setPixmap(pix)
#        qp.end()
#
#        
#    def mousePressEvent(self, event):
#        print('test')
#        self.begin = event.pos()
#        self.end = event.pos()
#        self.update()
#
#    def mouseMoveEvent(self, event):
#        self.end = event.pos()
#        self.update()
#
#    def mouseReleaseEvent(self, event):
#        self.end = event.pos()
#        self.update()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = QtCapture()
    sys.exit(app.exec_())