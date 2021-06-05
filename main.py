import playsound
from login import *
from system import *
from PyQt6 import QtCore, QtGui, QtWidgets
import re

class MainUi(object):
    system = System()
    system.load_database()
    # system.save_to_database()
    _translate = QtCore.QCoreApplication.translate

    def setup_ui(self, widget, Login):
        self.login_widget = Login
        widget.setWindowTitle("Focus")
        widget.setObjectName("Focus")
        widget.setWindowIcon(QtGui.QIcon("focus.png"))
        widget.setFixedSize(1109, 778)
        widget.setGeometry(200, 30, 1109, 778)
        widget.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid blue;}')
        # self.fontList = QtWidgets.QFontComboBox(widget)
        # self.fontList.textActivated.connect(self.change_font)

        self.font = QtGui.QFont("Kristen ITC")
        self.font.setPointSize(11)
        # Focus.setStyleSheet("background-image: url(background.jpg);")
        # image
        # self.bgd = QtWidgets.QTextBrowser(widget)
        # self.bgd.setGeometry(QtCore.QRect(0, 0, 1109, 778))
        # self.bgd.setObjectName("console")
        # self.bgd.setFont(self.font)
        self.centralwidget = QtWidgets.QWidget(widget)
        self.centralwidget.setObjectName("centralwidget")
        # create label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1109, 778))

        self.label.setObjectName("label")
        # widget.setCentralWidget(self.centralwidget)

        # set qmovie as label

        self.movie = QtGui.QMovie("view.gif")
        self.movie.setScaledSize(QtCore.QSize(1109, 778))
        self.label.setStyleSheet("""QLabel{opacity:0.1}""")
        self.label.setMovie(self.movie)
        self.movie.start()


        self.label2 = QtWidgets.QTextBrowser(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(0, 0, 1109, 778))
        self.label2.setStyleSheet("""QTextBrowser{background-color:rgba(255, 255, 255, 0.6);}""")
        # console
        self.console = QtWidgets.QTextBrowser(widget)
        self.console.setGeometry(QtCore.QRect(250, 730, 620, 40))
        self.console.setObjectName("console")


        # credits
        self.credits = QtWidgets.QTextBrowser(widget)
        self.credits.setGeometry(QtCore.QRect(260, 510, 190, 40))
        self.credits.setObjectName("credits")
        self.font.setPointSize(14)
        self.font.setFamily("Somebody")
        self.credits.setFont(self.font)


        self.update_credits()
        self.font.setPointSize(11)
        self.font.setFamily("Kristen ITC")

        # timer to check new day
        timer = QtCore.QTimer(widget)
        timer.timeout.connect(self.new_day)
        timer.start(1000)

        # timer for logout
        timer2 = QtCore.QTimer(widget)
        timer2.timeout.connect(self.login_widget.log_out)
        timer2.start(10000)

        self.tasks_combo = QtWidgets.QComboBox(widget)
        self.tasks_combo.setFont(self.font)
        self.tasks_combo.setGeometry(QtCore.QRect(780, 121, 191, 31))
        self.tasks_combo.setObjectName("comboBox")
        self.tasks_combo.addItem("Select a Task")
        self.tasks_combo.addItems(self.system.get_items_list_price())

        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(790, 80, 181, 31))
        self.label.setFont(self.font)
        self.label.setObjectName("label")

        ################## buttons ############################
        self.buy_button = QtWidgets.QPushButton(widget)
        self.buy_button.setFont(self.font)
        self.buy_button.setGeometry(QtCore.QRect(980, 230, 93, 31))
        self.buy_button.setObjectName("pushButton_2")
        self.buy_button.clicked.connect(self.buy_reward)
        self.buy_button.setStyleSheet("""
            QPushButton{background-color:#b00b69 ;border-radius:1px;border:1px solid #9e095e ;display:inline-block;
            cursor:pointer;color:#ffffff;self.font-size:17px;padding:0px 0px;text-decoration:none;
            text-shadow:0px 1px 0px #2f6627;}
            QPushButton:hover{background-color:#9e095e ;}
            QPushButton:active{	position:relative;top:1px;}
            QPushButton:disabled{background-color: #d98cb3; color: #602040}""")
        self.buy_button.setFont(self.font)


        self.register_button = QtWidgets.QPushButton(widget)
        self.register_button.setGeometry(QtCore.QRect(980, 120, 93, 31))
        self.register_button.setObjectName("pushButton")
        self.register_button.pressed.connect(self.register_task)
        self.register_button.setStyleSheet("""
            QPushButton{background-color: #9e095e;border-radius:1px;border:1px solid #9e095e ;display:inline-block;
            cursor:pointer;color:#ffffff;self.font-size:17px;padding:0px 0px;text-decoration:none;
            text-shadow:0px 1px 0px #2f6627;}
            QPushButton:hover{background-color:#b00b69 ;}
            QPushButton:active{	position:relative;top:1px;}
            QPushButton:disabled{background-color: #d98cb3; color: #602040}""")
        self.register_button.setFont(self.font)


        self.lock_tasks_button = QtWidgets.QPushButton(widget)
        self.lock_tasks_button.setGeometry(QtCore.QRect(180, 330, 93, 28))
        self.lock_tasks_button.setObjectName("pushButton")
        self.lock_tasks_button.clicked.connect(self.lock_tasks)
        self.lock_tasks_button.setStyleSheet("""
            QPushButton{background-color:#b00b69 ;border-radius:1px;border:1px solid #9e095e ;display:inline-block;
            cursor:pointer;color:#ffffff;self.font-size:17px;padding:0px 0px;text-decoration:none;
            text-shadow:0px 1px 0px #2f6627;}
            QPushButton:hover{background-color:#9e095e ;}
            QPushButton:active{	position:relative;top:1px;}
            QPushButton:disabled{background-color: #d98cb3; color: #602040}""")
        self.lock_tasks_button.setFont(self.font)

        if self.system.locked:
            self.lock_tasks_button.setDisabled(True)
            self.register_button.setDisabled(True)

        self.tasks_in_progress = QtWidgets.QLabel(widget)
        self.tasks_in_progress.setFont(self.font)
        self.tasks_in_progress.setGeometry(QtCore.QRect(140, 50, 181, 31))
        self.tasks_in_progress.setObjectName("label_2")

        self.todays_status = QtWidgets.QLabel(widget)
        self.todays_status.setFont(self.font)
        self.todays_status.setGeometry(QtCore.QRect(280, 410, 181, 31))

        self.todays_status.setFont(self.font)
        self.todays_status.setObjectName("label_3")
        self.progressBar = QtWidgets.QProgressBar(widget)
        self.progressBar.setFont(self.font)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(250, 450, 251, 23))

        self.progressBar.setFont(self.font)
        self.update_bar()
        self.progressBar.setObjectName("progressBar")

        self.label_4 = QtWidgets.QLabel(widget)
        self.label_4.setFont(self.font)
        self.label_4.setGeometry(QtCore.QRect(410, 50, 191, 31))
        self.label_4.setObjectName("label_4")

        self.completed_tasks = QtWidgets.QListWidget(widget)
        self.completed_tasks.setFont(self.font)
        self.completed_tasks.setGeometry(QtCore.QRect(380, 90, 256, 231))
        self.completed_tasks.setObjectName("listView_2")
        self.completed_tasks.addItems(self.system.completed_tasks)

        self.verticalLayoutWidget = QtWidgets.QWidget(widget)
        self.verticalLayoutWidget.setFont(self.font)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(110, 90, 241, 231))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        # tasks in progress
        self.in_progress_tasks = []
        for i in self.system.in_progress_tasks:
            temp = QtWidgets.QCheckBox(self.verticalLayoutWidget)
            temp.setFont(self.font)
            temp.setObjectName("checkBox")
            self.verticalLayout.addWidget(temp)
            temp.setText(self._translate("Focus", i))
            temp.clicked.connect(self.update)
            self.in_progress_tasks.append(temp)

        self.refresh = QtWidgets.QPushButton(widget)
        self.refresh.setFont(self.font)
        self.refresh.setGeometry(QtCore.QRect(250, 600, 200, 50))
        self.refresh.setObjectName("pushButton")
        self.refresh.clicked.connect(self.new_day)
        self.refresh.setDisabled(True)

        self.label_5 = QtWidgets.QLabel(widget)
        self.label_5.setGeometry(QtCore.QRect(770, 430, 181, 31))
        self.label_5.setFont(self.font)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(widget)
        self.verticalLayoutWidget_2.setFont(self.font)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(740, 470, 241, 231))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.bought_items_list = []
        for i in self.system.bought_rewards:
            t = QtWidgets.QCheckBox(self.verticalLayoutWidget_2)
            t.setFont(self.font)
            t.setObjectName("checkBox_3")
            self.verticalLayout_2.addWidget(t)
            t.setText(self._translate("Focus", i))
            t.clicked.connect(self.update)
            self.bought_items_list.append(t)

        self.store_label = QtWidgets.QLabel(widget)
        self.store_label.setFont(self.font)
        self.store_label.setGeometry(QtCore.QRect(840, 190, 181, 31))
        self.store_label.setFont(self.font)
        self.store_label.setObjectName("label_6")

        self.store_combo = QtWidgets.QComboBox(widget)
        self.store_combo.setFont(self.font)
        self.store_combo.addItem("Select a Reward")
        self.store_combo.addItems(self.system.get_rewards_list_price())
        self.store_combo.setGeometry(QtCore.QRect(780, 230, 191, 31))
        self.store_combo.setObjectName("comboBox_2")

        self.bought_items = QtWidgets.QLabel(widget)
        self.bought_items.setFont(self.font)
        self.bought_items.setGeometry(QtCore.QRect(780, 430, 161, 31))
        self.bought_items.setFont(self.font)
        self.bought_items.setObjectName("label_7")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)
        # self.fontList.raise_()

    def change_font(self):
        self.font.setFamily(self.fontList.currentText())
        self.label_4.setFont(self.font)
        print("gfdf")
    def retranslateUi(self, Focus):
        self.widget = Focus
        _translate = QtCore.QCoreApplication.translate
        Focus.setWindowTitle(_translate("Focus", "Focus"))
        self.label.setText(_translate("Focus", "Register a Task"))

        self.register_button.setText(_translate("Focus", "Register"))
        self.refresh.setText(_translate("Focus", "Early evaluate!"))
        self.tasks_in_progress.setText(_translate("Focus", "Task in Progress"))
        self.todays_status.setText(_translate("Focus", "Today\'s Status"))
        self.progressBar.setFormat(_translate("Focus", "%p%"))
        self.label_4.setText(_translate("Focus", "Completed Tasks"))
        self.store_label.setText(_translate("Focus", "Store"))
        self.buy_button.setText(_translate("Focus", "Buy"))
        self.lock_tasks_button.setText(_translate("Focus", "Lock Tasks"))
        self.bought_items.setText(_translate("Focus", "Bought Items"))

    def update(self):
        self.credits.setText(str(self.system.credit))
        for i in self.in_progress_tasks:
            if i.isChecked():
                if self.system.locked:
                    self.system.in_progress_tasks.remove(i.text())
                    self.completed_tasks.addItem(i.text())
                    self.system.completed_tasks.append(i.text())
                    self.in_progress_tasks.remove(i)
                    self.verticalLayout.removeWidget(i)
                    i.deleteLater()
                else:
                    self.system.in_progress_tasks.remove(i.text())
                    self.in_progress_tasks.remove(i)
                    i.deleteLater()


        for i in self.bought_items_list:
            if i.isChecked():
                self.system.bought_rewards.remove(i.text())
                self.bought_items_list.remove(i)
                self.verticalLayout_2.removeWidget(i)
                i.deleteLater()
        self.update_bar()
        self.system.save_to_database()

    def new_day(self):
        if self.system.is_new_day():
            if not self.system.evaluated:
                self.evaluate()
            self.print("New Day!")
            self.register_button.setDisabled(False)
            self.lock_tasks_button.setDisabled(False)
            self.system.evaluated = False
            self.system.finished = False

    def evaluate(self):
        self.system.finished = False
        self.update()
        self.print("Day Evaluated!")
        self.system.new_day()
        self.completed_tasks.clear()
        for i in self.in_progress_tasks:
            i.deleteLater()
        self.in_progress_tasks.clear()
        self.update_credits()
        self.system.finished = False
        self.system.evaluated = True

    def update_credits(self):
        self.credits.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.credits.setText(str(self.system.credit))
        self.credits.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

    def buy_reward(self):
        if self.store_combo.currentText()[0] == "(":
            reward = re.sub(r'\([^()]*\)  ', '', self.store_combo.currentText())
            if self.system.can_buy(reward):
                self.system.buy(reward)
                self.print(f"Reward ({reward}) purchased successfully")

                temp = QtWidgets.QCheckBox(self.verticalLayoutWidget)
                temp.setObjectName("checkBox")
                self.verticalLayout_2.addWidget(temp)
                temp.setText(self._translate("Focus", reward))
                temp.setFont(self.font)
                temp.clicked.connect(self.update)
                self.bought_items_list.append(temp)
                self.update()
            else:
                self.print(f"Couldn't purchase {reward}, insufficient credits!", True)


    def register_task(self):
        if self.tasks_combo.currentText()[0] == "(":
            playsound.playsound("click.wav")
            task = re.sub(r'\([^()]*\)  ', '', self.tasks_combo.currentText())
            self.system.register_task(task)

            temp = QtWidgets.QCheckBox(self.verticalLayoutWidget)
            temp.setFont(self.font)
            temp.setObjectName("checkBox")
            self.verticalLayout.addWidget(temp)
            temp.setText(self._translate("Focus", task))

            temp.clicked.connect(self.update)

            self.in_progress_tasks.append(temp)
            self.print(f"Task {task} registered successfully")
            self.update()

    def print(self, message, alert=False):
        if alert:
            self.console.setTextColor(QtGui.QColor(255, 0, 0))
        else:
            self.console.setTextColor(QtGui.QColor(0, 0, 0))
        self.console.setText(message)

    def lock_tasks(self):
        if self.system.initialized:
            playsound.playsound("click.wav")
            self.system.locked = True
            self.register_button.setDisabled(True)
            self.lock_tasks_button.setDisabled(True)
            self.print("Focus!", True)
            self.update()
        else:
            self.print("Choose more Tasks!", True)

    def update_bar(self):
        t = self.system.get_completed_credits() * 100 / self.system.min_points
        self.progressBar.setProperty("value", t) if t <= 100 else self.progressBar.setProperty("value", 100)
        if t >= 100:
            self.system.finished = True


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_widget = QtWidgets.QWidget()
    main_ui = MainUi()
    login_widget = QtWidgets.QDialog()
    login_ui = LoginUi()
    main_ui.setup_ui(main_widget, login_ui)
    login_ui.setupUi(login_widget, main_ui, app)
    login_widget.show()
    sys.exit(app.exec())

