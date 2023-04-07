# Inspired by PyQt5 Creating Paint Application In 40 Minutes
#  https://www.youtube.com/watch?v=qEgyGyVA1ZQ
from zipfile import Path

# NB If the menus do not work then click on another application and then click back
# and they will work https://python-forum.io/Thread-Tkinter-macOS-Catalina-and-Python-menu-issue

# PyQt documentation links are prefixed with the word 'documentation' in the code below and can be accessed automatically
#  in PyCharm using the following technique https://www.jetbrains.com/help/pycharm/inline-documentation.html

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QFileDialog, QDockWidget, QPushButton, QVBoxLayout, \
    QLabel, QMessageBox, QTextEdit, QSlider, QComboBox
from PyQt6.QtGui import QIcon, QPainter, QPen, QAction, QPixmap
import sys
import csv, random
from PyQt6.QtCore import Qt, QPoint


class PictionaryGame(QMainWindow):  # documentation https://doc.qt.io/qt-6/qwidget.html
    '''
    Painting Application class
    '''

    def __init__(self):
        super().__init__()

        # set window title

        self.textEdit = QTextEdit()
        self.setWindowTitle("Pictionary Game")

        # set the windows dimensions
        top = 400
        left = 400
        width = 800
        height = 600
        self.setGeometry(top, left, width, height)

        # set the icon
        # windows version
        self.setWindowIcon(
            QIcon("./icons/paint-brush.png"))  # documentation: https://doc.qt.io/qt-6/qwidget.html#windowIcon-prop
        # mac version - not yet working
        # self.setWindowIcon(QIcon(QPixmap("./icons/paint-brush.png")))

        # image settings (default)
        self.image = QPixmap("./icons/canvas.png")  # documentation: https://doc.qt.io/qt-6/qpixmap.html
        self.image.fill(Qt.GlobalColor.white)  # documentation: https://doc.qt.io/qt-6/qpixmap.html#fill
        mainWidget = QWidget()
        mainWidget.setMaximumWidth(300)

        # draw settings (default)

        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black  # documentation: https://doc.qt.io/qt-6/qt.html#GlobalColor-enum

        # reference to last point recorded by mouse
        self.lastPoint = QPoint()  # documentation: https://doc.qt.io/qt-6/qpoint.html

        # keeping track of the game, scores and turn
        self.currentTurn = 1
        self.p1score = 0
        self.p2score = 0
        self.gameStarted = False

        # set up menus
        mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(
            " File")  # add the file menu to the menu bar, the space is required as "File" is reserved in Mac
        brushSizeMenu = mainMenu.addMenu(" Brush Size")  # add the "Brush Size" menu to the menu bar
        brushColorMenu = mainMenu.addMenu(" Brush Colour")  # add the "Brush Colour" menu to the menu bar
        helpMenu = mainMenu.addMenu("Help")  # add help menu to main menu
        aboutMenu = mainMenu.addMenu("About")  # add about menu to main menu

        # main menu styling
        mainMenu.setStyleSheet(
            """
          
                 width: 100%; 
                 padding:25px;
                 text-align: center; 
                 font-size: 15px;
                 font-family:Lucida Sans;
                 background: #DDC7A0 ;
                
                 
               } 
               
               
            """
        )

        # open file item
        openAction = QAction(QIcon("./icons/open.png"), 'Open', self)  # create an open action with a png as an icon
        openAction.setShortcut('Ctrl+O')  # connect this open action to a keyboard shortcut
        fileMenu.addAction(openAction)  # add this action to the file menu
        openAction.triggered.connect(
            self.open)  # when the menu option is selected or the shortcut is used the open file
        # slot is triggered

        # save menu item
        saveAction = QAction(QIcon("./icons/save.png"), "Save",
                             self)  # create a save action with a png as an icon, documentation:
        # https://doc.qt.io/qt-6/qaction.html
        saveAction.setShortcut(
            "Ctrl+S")  # connect this save action to a keyboard shortcut, documentation:
        # https://doc.qt.io/qt-6/qaction.html#shortcut-prop
        fileMenu.addAction(
            saveAction)  # add the save action to the file menu, documentation:
        # https://doc.qt.io/qt-6/qwidget.html#addAction
        saveAction.triggered.connect(
            self.save)  # when the menu option is selected or the shortcut is used the save slot is triggered,
        # documentation: https://doc.qt.io/qt-6/qaction.html#triggered

        # clear
        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self)  # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")  # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)  # add this action to the file menu
        clearAction.triggered.connect(
            self.clear)  # when the menu option is selected or the shortcut is used the clear slot is triggered

        # exit menu
        exitAction = QAction(QIcon('./icons/exit.png'), 'Exit', self)  # create an exit action with a png as an icon
        exitAction.setShortcut('Ctrl+E')  # connect this exit action to a keyboard shortcut
        fileMenu.addAction(exitAction)  # add this action to the file menu
        exitAction.triggered.connect(self.close)  # when the menu option is selected or the shortcut is used the exit
        # slot is triggered

        # brush thickness
        threepxAction = QAction(QIcon("./icons/threepx.png"), "3px", self)
        threepxAction.setShortcut("Ctrl+3")
        brushSizeMenu.addAction(threepxAction)  # connect the action to the function below
        threepxAction.triggered.connect(self.threepx)

        fivepxAction = QAction(QIcon("./icons/fivepx.png"), "5px", self)
        fivepxAction.setShortcut("Ctrl+5")
        brushSizeMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivepx)

        sevenpxAction = QAction(QIcon("./icons/sevenpx.png"), "7px", self)
        sevenpxAction.setShortcut("Ctrl+7")
        brushSizeMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenpx)

        ninepxAction = QAction(QIcon("./icons/ninepx.png"), "9px", self)
        ninepxAction.setShortcut("Ctrl+9")
        brushSizeMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninepx)

        # brush colors
        blackAction = QAction(QIcon("./icons/black.png"), "Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColorMenu.addAction(blackAction)
        blackAction.triggered.connect(self.black)

        redAction = QAction(QIcon("./icons/red.png"), "Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColorMenu.addAction(redAction)
        redAction.triggered.connect(self.red)

        greenAction = QAction(QIcon("./icons/green.png"), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColorMenu.addAction(greenAction)
        greenAction.triggered.connect(self.green)

        yellowAction = QAction(QIcon("./icons/yellow.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColorMenu.addAction(yellowAction);
        yellowAction.triggered.connect(self.yellow)

        # Help Menu
        helpAction = QAction(QIcon("./icons/help.jpg"), "Help", self)
        helpAction.setShortcut("Ctrl+H")
        helpMenu.addAction(helpAction)  # connect the action to the function below
        helpAction.triggered.connect(self.help)

        # About Menu
        aboutAction = QAction(QIcon("./icons/about.png"), "About", self)
        aboutAction.setShortcut("Ctrl+A")
        aboutMenu.addAction(aboutAction)  # connect the action to the function below
        aboutAction.triggered.connect(self.about)

        # Side Dock
        self.dockInfo = QDockWidget()
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dockInfo)

        # widget inside the Dock
        self.playerInfo = QWidget()
        self.vbdock = QVBoxLayout()
        self.playerInfo.setLayout(self.vbdock)
        self.playerInfo.setMaximumSize(100, self.height())
        self.playerInfo.setMaximumSize(135, self.width())

        # add gameplay info and controls to custom widget
        self.startLabel = QLabel("Press Start")
        self.vbdock.addWidget(self.startLabel)
        self.vbdock.addSpacing(10)

        # label for player turn
        self.playerTurn = QLabel("Player Turn: " + str(self.currentTurn))
        self.vbdock.addWidget(self.playerTurn)
        self.vbdock.addSpacing(10)

        # score label
        self.vbdock.addWidget(QLabel("Scores:"))

        # label for player 1 and 2 scores
        self.P1ScoreLabel = QLabel("Player 1: " + str(self.p1score))
        self.P2ScoreLabel = QLabel("Player 2: " + str(self.p2score))

        # adding label to dock
        self.vbdock.addWidget(self.P1ScoreLabel)
        self.vbdock.addWidget(self.P2ScoreLabel)

        self.vbdock.addStretch(1)

        # select mode label
        self.modeLabel = QLabel("Select mode:")
        self.selectMode = QComboBox()
        self.selectMode.addItem("easy")
        self.selectMode.addItem("hard")

        # button for start
        self.btnStart = QPushButton("Start ")

        # button for correct
        self.btnGuessed = QPushButton("Correct")

        # adding start button to dock
        self.vbdock.addWidget(self.btnStart)
        self.vbdock.addSpacing(5)

        # adding guessed button to dock
        self.vbdock.addWidget(self.btnGuessed)
        self.vbdock.addSpacing(5)

        # adding select mode label and combobox to dock
        self.vbdock.addWidget(self.modeLabel)
        self.vbdock.addWidget(self.selectMode)
        self.vbdock.addSpacing(10)

        # Start button event
        self.btnStart.clicked.connect(self.start)

        # guessedCorrectly button event
        self.btnGuessed.clicked.connect(lambda: self.guessedCorrectly())

        # select mode easy or hard
        self.selectMode.currentIndexChanged.connect(self.chooseMode)

        # Setting colour of dock to gray
        self.playerInfo.setAutoFillBackground(True)
        p = self.playerInfo.palette()
        p.setColor(self.playerInfo.backgroundRole(), Qt.GlobalColor.gray)
        self.playerInfo.setPalette(p)

        # set widget for dock
        self.dockInfo.setWidget(self.playerInfo)

        # getting list of words
        self.getList("easy")
        self.currentWord = self.getWord()

    # event handlers
    def mousePressEvent(self,
                        event):  # when the mouse is pressed, documentation:
        # https://doc.qt.io/qt-6/qwidget.html#mousePressEvent
        if event.button() == Qt.MouseButton.LeftButton:  # if the pressed button is the left button
            self.drawing = True  # enter drawing mode
            self.lastPoint = event.pos()  # save the location of the mouse press as the lastPoint
            print(self.lastPoint)  # print the lastPoint for debugging purposes

    def mouseMoveEvent(self,
                       event):  # when the mouse is moved, documentation: documentation:
        # https://doc.qt.io/qt-6/qwidget.html#mouseMoveEvent
        if self.drawing:
            painter = QPainter(self.image)  # object which allows drawing to take place on an image
            # allows the selection of brush colour, brish size, line type, cap type, join type. Images available here
            # http://doc.qt.io/qt-6/qpen.html
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap,
                                Qt.PenJoinStyle.RoundJoin))
            painter.drawLine(self.lastPoint,
                             event.pos())  # draw a line from the point of the original press to the point to where
            # the mouse was dragged to
            self.lastPoint = event.pos()  # set the last point to refer to the point we have just moved to,
            # this helps when drawing the next line segment
            self.update()  # call the update method of the widget which calls the paintEvent of this class

    def mouseReleaseEvent(self,
                          event):  # when the mouse is released, documentation:
        # https://doc.qt.io/qt-6/qwidget.html#mouseReleaseEvent
        if event.button() == Qt.MouseButton.LeftButton:  # if the released button is the left button, documentation:
            # https://doc.qt.io/qt-6/qt.html#MouseButton-enum ,
            self.drawing = False  # exit drawing mode

    # paint events
    def paintEvent(self, event):
        # you should only create and use the QPainter object in this method, it should be a local variable
        canvasPainter = QPainter(
            self)  # create a new QPainter object, documentation: https://doc.qt.io/qt-6/qpainter.html
        canvasPainter.drawPixmap(QPoint(),
                                 self.image)  # draw the image , documentation:
        # https://doc.qt.io/qt-6/qpainter.html#drawImage-1

    # resize event - this function is called
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    # open function
    def open(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)

        if fname[0]:
            f = open(fname[0], 'r')

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if the file path is empty
            return  # do nothing and return
        self.image.save(filePath)  # save file image to the file path

    def clear(self):
        self.image.fill(
            Qt.GlobalColor.white)  # fill the image with white, documentation: https://doc.qt.io/qt-6/qimage.html#fill-2
        self.update()  # call the update method of the widget which calls the paintEvent of this class

    def threepx(self):  # the brush size is set to 3
        self.brushSize = 3

    def fivepx(self):
        self.brushSize = 5

    def sevenpx(self):
        self.brushSize = 7

    def ninepx(self):
        self.brushSize = 9

    def black(self):  # the brush color is set to black
        self.brushColor = Qt.GlobalColor.black

    def red(self):
        self.brushColor = Qt.GlobalColor.red

    def green(self):
        self.brushColor = Qt.GlobalColor.green

    def yellow(self):
        self.brushColor = Qt.GlobalColor.yellow

    # help function that explain the gam to the players
    def help(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Help")
        msg.setText("THIS GAME IS PLAYED BY TWO PLAYERS.")
        msg.setText("Press START to begin\n\nPress CORRECT if word was guessed correctly\n\nclick on SKIP TURN if "
                    "player could not draw word "
                    "\n\nSelect mode to choose between easy or hard word\n\nP.S: Hard mode get extra points ")

        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.show()

    # about game function
    def about(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("About")
        msg.setText("ABOUT PICTIONARY")
        msg.setText("Pictionary v1.0\n\n@2022 ApexPlayground. All rights reserved")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.show()

    # easy mode
    def easyMode(self):
        self.getList("easy")
        self.currentWord = self.getWord()

    # hard mode
    def hardMode(self):
        self.getList("hard")
        self.currentWord = self.getWord()

    # choose mode, easy or hard word
    def chooseMode(self):
        if self.selectMode.currentText() == "easy":
            self.easyMode()
        else:
            self.hardMode()

    # start function
    def start(self):
        # checks if game has started
        if self.gameStarted:
            print("Turn Skipped")
            # switches turn from 1 to 2 when turn is skipped
            if self.currentTurn == 1:
                self.currentTurn = 2

                # Updating the current turn label
                self.playerTurn.setText("Player Turn: " + str(self.currentTurn))
                self.playerTurn.update()
            else:
                self.currentTurn = 1

                # Updating the current turn label
                self.playerTurn.setText("Player Turn: " + str(self.currentTurn))
                self.playerTurn.update()

            # getting word
            self.chooseMode()

            # message box with player word and instructions
            msg = QMessageBox(self)
            msg.setWindowTitle("Pictionary")
            msg.setText("Turn skipped!\n\n Player " + str(self.currentTurn) + " word:")
            msg.setInformativeText("Don't let others see, Press show details!")
            msg.setDetailedText(self.currentWord)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.show()
            self.clear()
            self.update()

        else:
            self.gameStarted = True
            # changes start button to Skip Turn
            self.btnStart.setText("Skip Turn")

            # getting the words
            self.chooseMode()

            # Message box with word and instructions
            msg = QMessageBox(self)
            msg.setWindowTitle("Pictionary")
            msg.setText("Player " + str(self.currentTurn) + " See your word")
            msg.setInformativeText("Don't let others see, Press Show Details")
            msg.setDetailedText(self.currentWord)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.show()
            self.clear()
            self.update()

    # Adding scores if guessed correctly
    def guessedCorrectly(self):
        self.clear()
        if self.gameStarted:
            print("Guessed correctly")
            if self.currentTurn == 1:

                # Add to score
                # extra scores are added if mode is hard
                if self.selectMode.currentText() == "easy":
                    self.p1score += 2
                    self.p2score += 1
                else:
                    self.p1score += 3
                    self.p2score += 2

                # update the score label
                self.P1ScoreLabel.setText("Player 1: " + str(self.p1score))
                self.P2ScoreLabel.setText("Player 2: " + str(self.p2score))
                self.P1ScoreLabel.update()
                self.P2ScoreLabel.update()

                # switch turn to player 2
                self.currentTurn = 2

                # update the turn label
                self.playerTurn.setText("Player Turn: " + str(self.currentTurn))
                self.playerTurn.update()

                # get the words
                self.chooseMode()

                # message box with word and instructions
                msg = QMessageBox(self)
                msg.setWindowTitle("Pictionary")
                msg.setText("Player " + str(self.currentTurn) + " See your word")
                msg.setInformativeText("Don't let others see, Press Show Details")
                msg.setDetailedText(self.currentWord)
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.show()
                self.clear()
                self.update()

            else:
                # Add to score
                # extra scores are added if mode is hard
                if self.selectMode.currentText() == "easy":
                    self.p1score += 1
                    self.p2score += 2
                else:
                    self.p1score += 2
                    self.p2score += 3

                # update the label
                self.P1ScoreLabel.setText("Player 1: " + str(self.p1score))
                self.P2ScoreLabel.setText("Player 2: " + str(self.p2score))
                self.P1ScoreLabel.update()
                self.P2ScoreLabel.update()

                # switch turn to player 1
                self.currentTurn = 1

                # update the turn label
                self.playerTurn.setText("Player Turn: " + str(self.currentTurn))
                self.playerTurn.update()

                # get the words
                self.chooseMode()

                # message box with word and instructions
                msg = QMessageBox(self)
                msg.setWindowTitle("Pictionary")
                msg.setText("Player " + str(self.currentTurn) + " See your word")
                msg.setInformativeText("Don't let others see, Press Show Details")
                msg.setDetailedText(self.currentWord)
                msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg.show()
                self.clear()
                self.update()

    # Get a random word from the list read from file
    def getWord(self):
        randomWord = random.choice(self.wordList)
        print(randomWord)
        return randomWord

    # read word list from file
    def getList(self, mode):
        with open(mode + 'mode.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # print(row)
                self.wordList = row
                line_count += 1
            # print(f'Processed {line_count} lines.')

    # open a file
    def open(self):
        '''
        This is an additional function which is not part of the tutorial. It will allow you to:
         - open a file dialog box,
         - filter the list of files according to file extension
         - set the QImage of your application (self.image) to a scaled version of the file)
         - update the widget
        '''
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "PNG(*.png);;JPG(*.jpg *.jpeg);;All Files (*.*)")
        if filePath == "":  # if not file is selected exit
            return
        with open(filePath, 'rb') as f:  # open the file in binary mode for reading
            content = f.read()  # read the file
        self.image.loadFromData(content)  # load the data into the file
        width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height)  # scale the image from file and put it in your QImage
        self.update()  # call the update method of the widget which calls the paintEvent of this class


# this code will be executed if it is the main module but not if the module is imported
#  https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # style for the application
    app.setStyleSheet(
        """
                

                QComboBox{
                    border: 1px solid ;
                    padding: 3px;
                   font-family:Lucida Sans;
                     font-size: 15px;
                    border-radius: 8px;
                    background: #f8f8ff ;
                }
                
                QPushButton{
                    border: 1px solid ;
                    padding: 3px;
                    background: #f8f8ff ;
                    font-family:Lucida Sans;
                     font-size: 15px;
                    border-radius: 8px;
                }
            

                QLabel{
                    font-family:Lucida Sans;
                    font-size: 15px;
                    font-weight: Medium;
                }

               QWidget{
               
                    
               }



            """
    )
    window = PictionaryGame()
    window.show()
    app.exec()  # start the event loop running
