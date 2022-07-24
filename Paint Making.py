from PySide6.QtUiTools import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from functools import partial
import cv2
import numpy as np

class ColorPicker(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.ui = loader.load("form.ui")
        self.ui.show()
        
        self.img = np.zeros((500, 500, 1), dtype="uint8")
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        
        self.edit_Show_Image_Label()
        
        self.ui.B_Slider.valueChanged.connect(partial(self.reset_Label_Value, "B"))
        self.ui.R_Slider.valueChanged.connect(partial(self.reset_Label_Value, "R"))
        self.ui.G_Slider.valueChanged.connect(partial(self.reset_Label_Value, "G"))
        
    def reset_Label_Value(self, color, value):
        if color == "B":
            self.ui.B_label.setText(str(f"B: {value}"))
            self.img[:, :, 2] = value
        elif color == "R":
            self.ui.R_label.setText(str(f"R: {value}"))
            self.img[:, :, 0] = value
        elif color == "G":
            self.ui.G_label.setText(str(f"G: {value}"))
            self.img[:, :, 1] = value
       
        
        self.edit_Show_Image_Label()
        
    def edit_Show_Image_Label(self):
        img = QImage(self.img,self.img.shape[0], self.img.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(img)
        
        self.ui.show_img_label.setPixmap(pixmap)
        self.ui.show_rgb_color_label.setText(f"Red & Green & Blue({self.img[0, 0, 0]}, {self.img[0, 0, 1]}, {self.img[0, 0, 2]})")
        
app = QApplication([])
window = ColorPicker()
app.exec()