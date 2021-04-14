from PyQt5.QtWidgets import *
import sys
import sqlite3
from DatabaseManager import determine_heading_labels
from DatabaseManager import db_read
from TimeConverter import TimeConverter as Tc
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5 import QtCore
matplotlib.use('Qt5Agg')

# import sql database
dtu = Tc.date_to_unix
utd = Tc.unix_to_date

# When accessing from the database, the program will require a 'time_range',
# this should be all as default but can be changed here.
# A feature will be implemented to change the time_range from the GUI.
times = [1618095260, 1618182381]
headings = ['temperature',
            'humidity',
            'pressure',
            'voc']


def button1_clicked():
    sys.exit()


# this method is used to access the database at this stage
# at a later stage this may be used to display data from the db into GUI
# Perhaps a useful link: https://www.tutorialspoint.com/pyqt/pyqt_database_handling.htm
def button2_clicked():
    connection = sqlite3.connect(r"data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * from data")
    results = cursor.fetchall()
    for r in results:
        print(r)
    cursor.close()
    connection.close()


class MplCanvas(FigureCanvasQTAgg):
    # class that creates a blank graph for data to be displayed in
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class App(QMainWindow):
    # Class to create the GUI.

    def __init__(self):
        super().__init__()
        self.title = 'Air Monitoring System'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 500
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):
    # This class creates the necessary widgets (buttons, graphs etc) to populate the GUI.

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tabs.resize(1000, 500)

        # Add tabs
        self.tabs.addTab(self.tab1, "Main Menu")
        self.tabs.addTab(self.tab2, "Temperature")
        self.tabs.addTab(self.tab3, "Humidity")
        self.tabs.addTab(self.tab4, "Pressure")
        self.tabs.addTab(self.tab5, "Volatile Organic Compounds (VOC)")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        # self.tab1.layout.setContentsMargins(0, 0, 0, 0)

        # Creates the 'Quit' button and re-sizes it
        self.pushButton1 = QPushButton("Quit")
        self.pushButton1.setFixedSize(QtCore.QSize(100, 20))

        self.pushButton2 = QPushButton("Database Access")
        self.pushButton2.setFixedSize(QtCore.QSize(100, 20))

        # Create and add text then add buttons
        self.descript = QLabel()
        self.wiki1 = QLabel()
        self.wiki2 = QLabel()
        self.wiki3 = QLabel()
        self.wiki4 = QLabel()
        self.descript.setText("<br>"
                              "This program is used to monitor the concentration of 4 gasses within the vicinity of the"
                              " application board. The gasses recorded are Carbon Monoxide, Nitric Oxide, Nitrogen"
                              " Dioxide<br>and Sulphur Dioxide, more information can be found about these gasses at the"
                              " links below:"
                              "<br><a href='https://en.wikipedia.org/wiki/Carbon_monoxide'>Carbon Monoxide Wiki</a>, "
                              "<br><a href='https://en.wikipedia.org/wiki/Nitric_oxide'>Nitric Oxide Wiki</a>, "
                              "<br><a href='https://en.wikipedia.org/wiki/Nitrogen_dioxide'>Nitrogen Dioxide Wiki</a>,"
                              "<br><a href='https://en.wikipedia.org/wiki/Sulphur_dioxide'>Sulphur Dioxide Wiki</a>.")
        self.tab1.layout.addWidget(self.descript)
        self.descript.setOpenExternalLinks(True)

        self.descript.setAlignment(QtCore.Qt.AlignTop)

        self.tab1.layout.addWidget(self.pushButton1, alignment=QtCore.Qt.AlignCenter)
        self.tab1.layout.addWidget(self.pushButton2, alignment=QtCore.Qt.AlignCenter)
        self.tab1.setLayout(self.tab1.layout)
        self.pushButton1.clicked.connect(button1_clicked)
        self.pushButton2.clicked.connect(button2_clicked)

        # Create second, third and fourth tabs and add graphs
        self.tab2.layout = QVBoxLayout(self)
        self.tab2.setLayout(self.tab2.layout)

        self.tab3.layout = QVBoxLayout(self)
        self.tab3.setLayout(self.tab3.layout)

        self.tab4.layout = QVBoxLayout(self)
        self.tab4.setLayout(self.tab4.layout)

        self.tab5.layout = QVBoxLayout(self)
        self.tab5.setLayout(self.tab5.layout)

        temp = MplCanvas(self, width=5, height=4, dpi=100)
        humid = MplCanvas(self, width=5, height=4, dpi=100)
        press = MplCanvas(self, width=5, height=4, dpi=100)
        voc = MplCanvas(self, width=5, height=4, dpi=100)

        """
        To add graphs the data must be retrieved from the db, to do this we use db_read from
        DatabaseManager.py, however the Plotter.py cannot be used because this plots in a new window
        (Address this in the meeting as well)
        """
        for i in range(4):
            print(i)
            graph_data = db_read(times, headings[i], plot_graph=False)

            print(graph_data[1])
            print(graph_data[2][0])

            labels = determine_heading_labels(headings[i])  # Determine the labels to be used
            if i == 0:
                temp.axes.plot(graph_data[1], graph_data[2][0])
                # labels and title
                temp.axes.set_ylabel("Temperature (\N{DEGREE SIGN}C)")
                temp.axes.set_xlabel("Date and Time [D H:M]")
                temp.axes.set_title("Air Temperature Recorded by the System.")
            elif i == 1:
                humid.axes.plot(graph_data[1], graph_data[2][0])
                # labels, key and title
                humid.axes.set_ylabel("Humidity (%)")
                humid.axes.set_xlabel("Date and Time [D H:M]")
                humid.axes.set_title("Air Humidity Recorded by the System.")
                # humid.axes.legend(labels)
            elif i == 2:
                press.axes.plot(graph_data[1], graph_data[2][0])
                # labels, key and title
                press.axes.set_ylabel("Pressure (Pa)")
                press.axes.set_xlabel("Date and Time [D H:M]")
                press.axes.set_title("Air Pressure Detected by the System.")
                # press.axes.legend(labels)
            else:
                voc.axes.plot(graph_data[1], graph_data[2][0])
                # labels, key and title
                voc.axes.set_ylabel("VOC ()")
                voc.axes.set_xlabel("Date and Time [D H:M]")
                voc.axes.set_title("Volatile Organic Compounds Detected by the System.")
                # voc.axes.legend(labels)

        self.tab2.layout.addWidget(temp)
        self.tab3.layout.addWidget(humid)
        self.tab4.layout.addWidget(press)
        self.tab5.layout.addWidget(voc)

        # Add the tabs to the GUI
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
