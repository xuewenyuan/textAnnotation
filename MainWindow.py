from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import json
import os
from os.path import join as osj

class MainWindow(QMainWindow):
    def __init__(self,  parent = None):
         super(MainWindow,  self).__init__(parent)
         self.setWindowTitle("Annotation Tool")
         self.setMinimumHeight(768)
         self.setMinimumWidth(1360)

         # Dock1---Image
         #-------------------------------------------------------------------------------
         self.dockWidget1 = QDockWidget('Image')
         self.dockWidget1.setAllowedAreas(Qt.LeftDockWidgetArea or Qt.RightDockWidgetArea)

         self.inform=[]
         self.filename = ''

         self.btn_open = QPushButton("Open")
         self.btn_open.clicked.connect(self.on_btn_open_clicked)
         self.label_img = QLabel("Image Name")
         self.label_img.setAlignment(Qt.AlignCenter)
         self.btn_prev_img = QPushButton("< Prev")
         self.btn_prev_img.clicked.connect(self.on_btn_prev_img_clicked)
         self.btn_next_img = QPushButton("Next >")
         self.btn_next_img.clicked.connect(self.on_btn_next_img_clicked)
         self.label_img_sig = QLabel("0/0")
         self.label_img_sig.setAlignment(Qt.AlignCenter)

         self.dock1_layout = QGridLayout()
         self.dock1_layout.setRowStretch(3,1)
         #self.dock1_layout.setColumnStretch(17,1)

         self.dock1_layout.addWidget(self.btn_open, 1, 1, 1, 3)
         self.dock1_layout.addWidget(self.label_img, 1, 5, 1, 7)
         self.dock1_layout.addWidget(self.btn_prev_img, 2, 1, 1, 3)
         self.dock1_layout.addWidget(self.label_img_sig, 2, 5, 1, 3)
         self.dock1_layout.addWidget(self.btn_next_img, 2, 9, 1, 3)

         self.dock1_widget = QWidget()
         self.dock1_widget.setLayout(self.dock1_layout)
         self.dockWidget1.setWidget(self.dock1_widget)
         self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget1)

         # Dock2---Annotation
         #-------------------------------------------------------------------------------
         self.dockWidget2 = QDockWidget('Annotation')
         self.dockWidget2.setAllowedAreas(Qt.LeftDockWidgetArea or Qt.RightDockWidgetArea)

         #self.btn_prev_anno = QPushButton("∧")
         self.btn_prev_anno = QPushButton("< Prev")
         self.btn_prev_anno.clicked.connect(self.on_btn_prev_anno_clicked)
         #self.btn_next_anno = QPushButton("∨")
         self.btn_next_anno = QPushButton("Next >")
         self.btn_next_anno.clicked.connect(self.on_btn_next_anno_clicked)
         self.label_anno_sig = QLabel("0/0")
         self.label_anno_sig.setAlignment(Qt.AlignCenter)
         self.label_anno_text = QLabel("Text:")
         self.edit_text = QLineEdit()
         self.label_table_text = QLabel("Table_No:")
         self.edit_table = QLineEdit()
         self.label_row_text = QLabel("Cell_Row:")
         self.edit_row = QLineEdit()
         self.label_line_text = QLabel("Cell_Line:")
         self.edit_line = QLineEdit()
         self.save_anno = QPushButton("Save Annotation")
         self.save_anno.clicked.connect(self.on_save_anno_clicked)

         self.dock2_layout = QGridLayout()
         self.dock2_layout.setRowStretch(7,1)
         #self.dock1_layout.setColumnStretch(17,1)

         self.dock2_layout.addWidget(self.btn_prev_anno, 1, 1, 1, 3)
         self.dock2_layout.addWidget(self.label_anno_sig, 1, 5, 1, 3)
         self.dock2_layout.addWidget(self.btn_next_anno, 1, 9, 1, 3)
         self.dock2_layout.addWidget(self.label_anno_text, 2, 1, 1, 3)
         self.dock2_layout.addWidget(self.edit_text, 2, 5, 1, 7)
         self.dock2_layout.addWidget(self.label_table_text, 3, 1, 1, 3)
         self.dock2_layout.addWidget(self.edit_table, 3, 5, 1, 7)
         self.dock2_layout.addWidget(self.label_row_text, 4, 1, 1, 3)
         self.dock2_layout.addWidget(self.edit_row, 4, 5, 1, 7)
         self.dock2_layout.addWidget(self.label_line_text, 5, 1, 1, 3)
         self.dock2_layout.addWidget(self.edit_line, 5, 5, 1, 7)
         self.dock2_layout.addWidget(self.save_anno, 6, 1, 1, 11)

         self.dock2_widget = QWidget()
         self.dock2_widget.setLayout(self.dock2_layout)
         self.dockWidget2.setWidget(self.dock2_widget)
         self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget2)

         # ---Annotation
         #-------------------------------------------------------------------------------
         self.scene = QGraphicsScene()

         #Bbox
         self.pen = QPen(Qt.red, 3, Qt.SolidLine, Qt.SquareCap, Qt.RoundJoin)
         self.bbox_x = 0.0
         self.bbox_y = 0.0
         self.bbox_width = 0.0
         self.bbox_height = 0.0
         self.bbox = self.scene.addRect(self.bbox_x, self.bbox_y, self.bbox_width, self.bbox_height, self.pen)
         self.bbox.setZValue(1)
         #self.scene.setFocusItem(self.bbox)
         #pixMap
         self.pixMap = QGraphicsPixmapItem()
         self.scene.addItem(self.pixMap)

         #print(self.scene.items())
         #self.scene.removeItem(self.bbox)
         #print(self.scene.items())

         self.view = QGraphicsView(self)
         self.view.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
         self.view.setScene(self.scene)
         #self.view.centerOn(self.bbox)
         self.central_widget = QWidget()
         self.central_layout = QVBoxLayout()
         self.central_layout.addWidget(self.view)
         self.central_widget.setLayout(self.central_layout)
         self.setCentralWidget(self.central_widget)

    @pyqtSlot(bool)
    def on_btn_open_clicked(self, checked):

        if len(self.inform):
            self.f = open(self.filename,'w')
            json.dump(self.inform, self.f)
            self.f.close()

        self.filename = QFileDialog.getOpenFileName(self, "OpenFile", ".",
            "JSON Files(labels.json)")[0]
        if len(self.filename):
            self.f = open(self.filename,'r')
            self.inform = json.load(self.f)
            self.f.close()
            self.img_index = 0
            self.unsave_changes = 0
            self.img_amount = len(self.inform)
            self.anno_amount = len(self.inform[self.img_index]['annotations'])
            self.anno_index = 0

            self.setText(True)

            self.setImg()
            #
            self.setBbox()




    @pyqtSlot(bool)
    def on_btn_next_img_clicked(self, checked):
        self.informSave()

        if len(self.inform) and self.img_index != len(self.inform)-1:
            self.img_index += 1
            self.anno_amount = len(self.inform[self.img_index]['annotations'])
            self.anno_index = 0

            self.setText(True)

            self.setImg()
            #
            self.setBbox()


    @pyqtSlot(bool)
    def on_btn_prev_img_clicked(self, checked):

        self.informSave()

        if len(self.inform) and self.img_index != 0:
            self.img_index -= 1
            self.anno_amount = len(self.inform[self.img_index]['annotations'])
            self.anno_index = 0

            self.setText(True)

            self.setImg()
            #
            self.setBbox()


    @pyqtSlot(bool)
    def on_btn_prev_anno_clicked(self, checked):

        self.informSave()

        if self.anno_amount and self.anno_index != 0:
            self.anno_index -= 1
            #
            self.setText(False)
            #
            self.setBbox()

    @pyqtSlot(bool)
    def on_btn_next_anno_clicked(self, checked):

        self.informSave()

        if self.anno_amount and self.anno_index != self.anno_amount-1:
            self.anno_index += 1
            #
            self.setText(False)
            #
            self.setBbox()

    @pyqtSlot(bool)
    def on_save_anno_clicked(self, checked):
        self.fileSave()

#
#Global Function
#-------------------------------------------------------------------------------
    def informSave(self):
        if self.edit_text.text() !='':
            self.inform[self.img_index]['annotations'][self.anno_index]['text'] = self.edit_text.text()
            self.unsave_changes += 1
        if self.edit_table.text() != '':
            self.inform[self.img_index]['annotations'][self.anno_index]['table_no'] = self.edit_table.text()
            self.unsave_changes += 1
        if self.edit_line.text() != '':
            self.inform[self.img_index]['annotations'][self.anno_index]['cell_line'] = self.edit_line.text()
            self.unsave_changes += 1
        if self.edit_row.text() != '':
            self.inform[self.img_index]['annotations'][self.anno_index]['cell_row'] = self.edit_row.text()
            self.unsave_changes += 1
        self.edit_text.clear()
        self.edit_table.clear()
        self.edit_line.clear()
        self.edit_row.clear()

    def setText(self, btn_img):
        if btn_img:
            self.label_img.setText(self.inform[self.img_index]['filename'])
            self.label_img_sig.setText(str(self.img_index+1)+'/'+str(self.img_amount))

        self.label_anno_sig.setText(str(self.anno_index+1)+'/'+str(self.anno_amount))
        self.edit_text.setPlaceholderText(self.inform[self.img_index]['annotations'][self.anno_index]['text'])
        self.edit_table.setPlaceholderText(self.inform[self.img_index]['annotations'][self.anno_index]['table_no'])
        self.edit_line.setPlaceholderText(self.inform[self.img_index]['annotations'][self.anno_index]['cell_line'])
        self.edit_row.setPlaceholderText(self.inform[self.img_index]['annotations'][self.anno_index]['cell_row'])

    def setBbox(self):
        self.bbox_x = self.inform[self.img_index]['annotations'][self.anno_index]['x']
        self.bbox_y = self.inform[self.img_index]['annotations'][self.anno_index]['y']
        self.bbox_width = self.inform[self.img_index]['annotations'][self.anno_index]['width']
        self.bbox_height = self.inform[self.img_index]['annotations'][self.anno_index]['height']
        self.bbox.setRect(self.bbox_x, self.bbox_y, self.bbox_width, self.bbox_height)
        self.view.centerOn(self.bbox)

    def setImg(self):
        self.image = QImage(self.filename.replace("labels.json",self.inform[self.img_index]['filename']))
        self.pixMap.setPixmap(QPixmap.fromImage(self.image))

#Global event handing
#-------------------------------------------------------------------------------
    def fileSave(self):
        if len(self.filename):
            if self.edit_text.text() != '':
                self.inform[self.img_index]['annotations'][self.anno_index]['text'] = self.edit_text.text()
                self.unsave_changes += 1
            self.f = open(self.filename,'w')
            json.dump(self.inform, self.f)
            self.f.close()
            msgBox = QMessageBox(self)
            msgBox.setText("Changes have been saved!")
            msgBox.exec()
        else:
            msgBox = QMessageBox(self)
            msgBox.setText("No file is loaded!")
            msgBox.exec()

    def okToContinue(self):
        reply = QMessageBox.question(self, "%d unsaved changes!" % self.unsave_changes, "Save unsaved changes?", QMessageBox.Yes|QMessageBox.No|QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.fileSave()
            return True
        elif reply == QMessageBox.Cancel:
            return False
        return True

    def closeEvent(self, event):
        if self.okToContinue() == False:
            event.ignore()
