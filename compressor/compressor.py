from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QGroupBox, QGridLayout, \
    QDesktopWidget, QApplication, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, \
    QFileDialog, QLineEdit, QMessageBox, QErrorMessage 
import sys, zipfile, os 
from os.path import expanduser, basename
from datetime import datetime


class Main(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.homepath  = expanduser("~")
        self.pathToSaveDescompressFiles = "" 
        self.pathSourceDescompress = "" 
        self.pathdstcompress = "" 

        self.groupBoxMain = QGroupBox("Compress Files")
        self.groupBoxMain.setStyleSheet("font-size: 16px; color: 444;")

        self.containerLayout = QVBoxLayout()
        self.containerLayout.addWidget(self.groupBoxMain)
        self.setLayout(self.containerLayout)

        self.mainLayout = QGridLayout()
        self.groupBoxMain.setLayout(self.mainLayout)

        self.groupBoxCompress = QGroupBox("Compress:")
        self.groupBoxCompress.setStyleSheet("font-size: 12px;")
        self.compressLayout = QGridLayout()
        self.groupBoxCompress.setLayout(self.compressLayout)
        self.mainLayout.addWidget(self.groupBoxCompress, 0, 0)

        self.labelFiles = QLabel("Select files:")
        self.labelFiles.setStyleSheet("color: #444; font-size: 15px;")
        self.compressLayout.addWidget(self.labelFiles, 0, 0)

        self.txtFilesSelected = QLineEdit("Files selected")
        self.txtFilesSelected.setEnabled(False)
        self.compressLayout.addWidget(self.txtFilesSelected, 0, 1)

        self.btnSelectFiles = QPushButton("Search")
        self.btnSelectFiles.setMaximumWidth(100)
        self.btnSelectFiles.clicked.connect(self.selectFilesToCompress)
        self.compressLayout.addWidget(self.btnSelectFiles, 1, 0)

        self.labelDst = QLabel("Select destination:")
        self.labelDst.setStyleSheet("color: #444; font-size: 15px;")
        self.compressLayout.addWidget(self.labelDst, 2, 0)

        self.txtDstCompress = QLineEdit(self.homepath)
        self.txtDstCompress.setEnabled(False)
        self.compressLayout.addWidget(self.txtDstCompress, 3, 0, 1, 2)

        self.btnPathCompress = QPushButton("Search")
        self.btnPathCompress.setMaximumWidth(100)
        self.btnPathCompress.clicked.connect(self.selectPathDestinationToCompress)
        self.compressLayout.addWidget(self.btnPathCompress, 4, 0)

        self.btnCompress = QPushButton("Zip")
        self.btnCompress.setMaximumWidth(100)
        self.btnCompress.setStyleSheet("background-color: #0096c7; color: white;")
        self.btnCompress.clicked.connect(self.compress)
        self.compressLayout.addWidget(self.btnCompress, 5, 0)

        self.groupBoxDescompress = QGroupBox("Decompress:")
        self.groupBoxDescompress.setStyleSheet("font-size: 12px;")
        self.descompressLayout = QGridLayout()
        self.groupBoxDescompress.setLayout(self.descompressLayout)
        self.mainLayout.addWidget(self.groupBoxDescompress, 0, 1)

        self.labelSource = QLabel("Select source:")
        self.labelSource.setStyleSheet("color: #444; font-size: 15px;")
        self.descompressLayout.addWidget(self.labelSource, 2, 0)

        self.txtSourceDescompress = QLineEdit(self.homepath)
        self.txtSourceDescompress.setEnabled(False)
        self.descompressLayout.addWidget(self.txtSourceDescompress, 3, 0)

        self.btnPathDecompress = QPushButton("Search")
        self.btnPathDecompress.clicked.connect(self.selectFileToDescompress)
        self.descompressLayout.addWidget(self.btnPathDecompress, 3, 1)

        self.labelDstDescompress = QLabel("Select destination:")
        self.labelDstDescompress.setStyleSheet("color: #444; font-size: 15px;")
        self.descompressLayout.addWidget(self.labelDstDescompress, 4, 0)

        self.txtDstDescompress = QLineEdit(self.homepath)
        self.txtDstDescompress.setEnabled(False)
        self.descompressLayout.addWidget(self.txtDstDescompress, 5, 0)

        self.btnPathDestination = QPushButton("Search")
        self.btnPathDestination.clicked.connect(self.selectPathToSaveDescompressFiles)
        self.descompressLayout.addWidget(self.btnPathDestination, 5, 1)

        self.btnDescompress = QPushButton("UnZip")
        self.btnDescompress.setMaximumWidth(100)
        self.btnDescompress.setStyleSheet("background-color: brown; color: white;")
        self.btnDescompress.clicked.connect(self.descompress)
        self.descompressLayout.addWidget(self.btnDescompress, 6, 0)
    
    def getFileNamesDialog(self):
        files, _ = QFileDialog.getOpenFileNames(self,"Files", "","All Files (*);")
        return files
    
    def selectFilesToCompress(self):
        self.filesToCompress = self.getFileNamesDialog()  
        self.txtFilesSelected.setText(str(self.filesToCompress))

    def selectPathDestinationToCompress(self):
        self.pathdstcompress, _ = QFileDialog.getSaveFileName(self,"Files","","Zip files(*.zip)")
        self.txtDstCompress.setText(self.pathdstcompress) 

    def selectFileToDescompress(self):
        filepath, _ = QFileDialog.getOpenFileNames(self,"File", "","Zip File *.zip;")

        if filepath:
            self.pathSourceDescompress = filepath[0]
            self.txtSourceDescompress.setText(filepath[0])

    def selectPathToSaveDescompressFiles(self):
        self.pathToSaveDescompressFiles = QFileDialog.getExistingDirectory(self, "Folders")
        self.txtDstDescompress.setText(self.pathToSaveDescompressFiles)

    def compress(self):

        if not self.pathdstcompress or not os.path.isdir(self.pathdstcompress):
            QErrorMessage().showMessage("Destination path not established or not correct: " + self.pathdstcompress)

        if self.filesToCompress:
            zf = zipfile.ZipFile(self.pathdstcompress, mode="w")
                                                       
            try:
                for filepath in self.filesToCompress:
                    zf.write(filepath)

            except Exception:
                dialog = QErrorMessage()
                dialog.showMessage("Error compressing files")
            else:
                dialog = QErrorMessage()
                dialog.showMessage("Successfully compressed files")

            finally:
                zf.close()
        else:
            dialog = QErrorMessage()
            dialog.showMessage("You must select at least one file")

    def descompress(self):

        if not self.pathSourceDescompress: 
            QErrorMessage().showMessage("Destination path not established or not correct: " + self.pathdstcompress)
            return

        if not self.pathToSaveDescompressFiles or not os.path.isdir(self.pathToSaveDescompressFiles):
            QErrorMessage().showMessage("Destination path not established or not correct: " + self.pathToSaveDescompressFiles)
            return

        try:
            zf = zipfile.ZipFile(self.pathSourceDescompress, mode="r")
            zf.extractall(self.pathToSaveDescompressFiles)

            dialog2 = QErrorMessage()
            dialog2.showMessage("Successfully unzipped files")

            zf.close()
        except Exception as e:
            print(e)
            dialog = QErrorMessage()
            dialog.showMessage("Error unzipping files")
        
class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()

        self.width = 700
        self.height = 240
        self.title = "Zip Files"
        self.left = 100
        self.top = 100

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.setStyleSheet("background-color: #eee;")
        self.setWindowIcon(QIcon("logo.png"))
        self.setFixedSize(self.width, self.height)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.widget = Main(self)
        self.setCentralWidget(self.widget)       

        self.show()

def run():
    app = QApplication(sys.argv)
    ex = MainApplication()

    q = QMessageBox()
    q.setText("Hello")

    sys.exit(app.exec_())