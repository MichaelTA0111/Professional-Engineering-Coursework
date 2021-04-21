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
from StatisticsManager import StatisticsManager
from Exporter import Exporter
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

# this method is used to access the database at this stage
# at a later stage this may be used to display data from the db into GUI
# Perhaps a useful link: https://www.tutorialspoint.com/pyqt/pyqt_database_handling.htm


# connection = sqlite3.connect(r"data.db")
# cursor = connection.cursor()
# cursor.execute("SELECT * from data")
# results = cursor.fetchall()
# for r in results:
#     print(r)
# cursor.close()
# connection.close()


def graph_init(self, graph_data, ylabel, xlabel, title, tab):
    """
    Method to create the MatPlotLib graph and populate it with relevant data.
    :param self:
    :param graph_data: the time and temperature/humidity/pressure/VOC
    :param ylabel:
    :param xlabel:
    :param title:
    :param tab: which tab of the GUI to be included within
    :return:
    """
    graph = MplCanvas(self, width=5, height=4, dpi=100)
    graph.axes.plot(graph_data[1], graph_data[2][0])
    graph.axes.grid()
    # labels and title
    graph.axes.set_ylabel(ylabel)
    graph.axes.set_xlabel(xlabel)
    graph.axes.set_title(title)
    tab.layout.addWidget(graph)
    return graph


def tab_create(title, tabs):
    tab = QWidget()
    tabs.addTab(tab, title)
    tab.layout = QVBoxLayout()
    tab.setLayout(tab.layout)
    return tab


def stats_create(graph_data, tab):
    stats = StatisticsManager(graph_data[2][0], graph_data[1])
    stats_text = QLabel()
    mean = str('{0:.2f}'.format(stats.get_mean()))
    median = str('{0:.2f}'.format(stats.get_median()))
    mode = str(stats.get_mode())
    range = str('{0:.2f}'.format(stats.get_range()))
    iqr = str('{0:.2f}'.format(stats.get_iqr()))
    sd = str('{0:.2f}'.format(stats.get_sd()))
    variance = str('{0:.2f}'.format(stats.get_variance()))
    max = str('{0:.2f}'.format(stats.get_max()))
    max_time = str(stats.get_max_time())
    min = str('{0:.2f}'.format(stats.get_min()))
    min_time = str(stats.get_min_time())
    stats_text.setText("Mean: " + mean + "\nMedian: " + median + "\nMode: " + mode + "\nRange: " + range +
                       "\nInter-quartile Range: " + iqr + "\nStandard Deviation: " + sd + "\nVariance: " +
                       variance + "\nMaximum y value: " + max + "\nMaximum time value: " + max_time +
                       "\nMinimum y value: " + min + "\nMinimum time value: " + min_time)
    tab.layout.addWidget(stats_text)


def text_create(tab, contents):
    text = QLabel()
    text.setText(contents)
    tab.layout.addWidget(text, alignment=QtCore.Qt.AlignTop)
    text.setOpenExternalLinks(True)
    return text


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
        layout = QVBoxLayout(self)

        # Initialize tab screen and creates all 5 tabs
        tabs = QTabWidget()
        tab1 = tab_create("Main Menu", tabs)
        tab2 = tab_create("Temperature", tabs)
        tab3 = tab_create("Humidity", tabs)
        tab4 = tab_create("Pressure", tabs)
        tab5 = tab_create("Volatile Organic Compounds (VOC)", tabs)
        tab6 = tab_create("Statistics", tabs)
        tabs.resize(1000, 500)

        # Creates the 'Quit' button and re-sizes it
        push_button1 = QPushButton("Quit")
        push_button1.setFixedSize(QtCore.QSize(150, 40))

        push_button2 = QPushButton("Update Time Range")
        push_button2.setFixedSize(QtCore.QSize(150, 40))

        push_button3 = QPushButton("Export Data to CSV")
        push_button3.setFixedSize(QtCore.QSize(150, 40))

        # Create and add text then add buttons
        descript_contents = ("<br>"
                             "This program is used to monitor the temperature, humidity, pressure and the volatile "
                             "organic compounds within the immediate vicinity of the monitoring system. For more "
                             "information on these features and their impact on the environment, click the links below:"
                             "<br><a href='https://en.wikipedia.org/wiki/Carbon_monoxide'>Carbon Monoxide Wiki</a>, "
                             "<br><a href='https://en.wikipedia.org/wiki/Nitric_oxide'>Nitric Oxide Wiki</a>, "
                             "<br><a href='https://en.wikipedia.org/wiki/Nitrogen_dioxide'>Nitrogen Dioxide Wiki</a>,"
                             "<br><a href='https://en.wikipedia.org/wiki/Sulphur_dioxide'>Sulphur Dioxide Wiki</a>.")
        descript = text_create(tab1, descript_contents)
        descript.setOpenExternalLinks(True)

        text_start_time = QLabel()
        text_start_time.setText("Enter the start time (in form DD/MM/YYYY HH:MM:SS): ")

        textbox1 = QLineEdit()
        textbox1.move(20, 20)
        textbox1.resize(280, 40)

        text_end_time = QLabel()
        text_end_time.setText("Enter the end time (in form DD/MM/YYYY HH:MM:SS): ")
        text_end_time.setContentsMargins(0, 0, 0, 0)

        textbox2 = QLineEdit(self)
        textbox2.move(20, 20)
        textbox2.resize(280, 40)

        tab1.layout.addWidget(text_start_time, alignment=QtCore.Qt.AlignHCenter)
        tab1.layout.addWidget(textbox1, alignment=QtCore.Qt.AlignHCenter)
        tab1.layout.addWidget(text_end_time, alignment=QtCore.Qt.AlignHCenter)
        tab1.layout.addWidget(textbox2, alignment=QtCore.Qt.AlignHCenter)
        tab1.layout.addWidget(push_button2, alignment=QtCore.Qt.AlignHCenter)

        export_text = QLabel()
        export_text.setText("Enter csv file name to export to (in form 'filename.csv'): ")
        export_text.setContentsMargins(0, 0, 0, 0)

        textbox3 = QLineEdit(self)
        # textbox3.move(20, 20)
        textbox3.resize(280, 40)

        tab1.layout.addWidget(export_text, alignment=QtCore.Qt.AlignHCenter)
        tab1.layout.addWidget(textbox3, alignment=QtCore.Qt.AlignHCenter)
        tab1.layout.addWidget(push_button3, alignment=QtCore.Qt.AlignHCenter)
        tab1.layout.addWidget(push_button1, alignment=QtCore.Qt.AlignHCenter)

        data = ["", "", "", ""]
        for i in range(4):
            data[i] = list(db_read(times, headings[i], plot_graph=False)[2])

        push_button1.clicked.connect(self.quit_button_clicked)
        push_button2.clicked.connect(lambda: self.time_button_clicked(textbox1.text(), textbox2.text(), temp, humid,
                                                                      press, voc, tab2))
        push_button3.clicked.connect(lambda: self.export_button_clicked(headings, data))

        temp_title = "Statistics for the temperature: "
        humid_title = "Statistics for the humidity: "
        press_title = "Statistics for the pressure: "
        voc_title = "Statistics for the VOC: "

        """
        To add graphs the data must be retrieved from the db, to do this we use db_read from
        DatabaseManager.py, however the Plotter.py cannot be used because this plots in a new window
        (Address this in the meeting as well)
        """
        for i in range(4):
            graph_data = db_read(times, headings[i], plot_graph=False)
            labels = determine_heading_labels(headings[i])  # Determine the labels to be used (if key was necessary)

            if i == 0:
                temp = graph_init(self, graph_data=graph_data, xlabel="Date and Time [M-D H]", tab=tab2,
                                  ylabel="Temperature (\N{DEGREE SIGN}C)",
                                  title="Air Temperature Recorded by the System.")
                text_create(tab6, temp_title)
                stats_create(graph_data, tab6)
            elif i == 1:
                humid = graph_init(self, graph_data=graph_data, xlabel="Date and Time [M-D H]", tab=tab3,
                                   ylabel="Humidity (%)", title="Air Humidity Recorded by the System.")
                # humid.axes.legend(labels)
                text_create(tab6, humid_title)
                stats_create(graph_data, tab6)
            elif i == 2:
                press = graph_init(self, graph_data=graph_data, xlabel="Date and Time [M-D H]", tab=tab4,
                                   ylabel="Pressure (Pa)", title="Air Pressure Detected by the System.")
                text_create(tab6, press_title)
                stats_create(graph_data, tab6)
            else:
                voc = graph_init(self, graph_data=graph_data, xlabel="Date and Time [M-D H]", tab=tab5,
                                 ylabel="VOC (k\u03A9)", title="Volatile Organic Compounds Detected by the System.")
                text_create(tab6, voc_title)
                stats_create(graph_data, tab6)

        layout.addWidget(tabs)
        self.setLayout(layout)

    # def on_click(self):
    #     print("\n")
    #     for currentQTableWidgetItem in self.tableWidget.selectedItems():
    #         print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    @staticmethod
    def quit_button_clicked():
        sys.exit()

    @staticmethod
    def time_button_clicked(textbox1_value, textbox2_value, temp, humid, press, voc, tab2):
        """
        This method should take the new time input, convert it to unix then display an updated graph with the
         corresponding data, it should also update the statistics to be relevant to the time range selected.
        :param textbox1_value:
        :param textbox2_value:
        :param temp:
        :param humid:
        :param press:
        :param voc:
        :param tab2:
        :return:
        """
        # test time: 10/04/2021 22:54:20, 10/04/2021 23:50:00
        # or: 1618095260, 1618101201
        print("test")
        # time_range = [(textbox1_value), (textbox2_value)]
        time_range = [1618095260, 1618101201]
        print(time_range)
        for i in range(4):
            print(i)
            graph_data = db_read(time_range, headings[i], plot_graph=False)
            print(graph_data)
            if i == 0:
                # code breaks here
                temp.axes.clear()
                temp.axes.plot(graph_data[1], graph_data[2][0])
                temp.axes.grid()
                # labels and title
                temp.axes.set_ylabel("Temperature (\N{DEGREE SIGN}C)")
                temp.axes.set_xlabel("Date and Time [M-D H]")
                temp.axes.set_title("Air Temperature Recorded by the System.")
                tab2.layout.addWidget(temp)
            elif i == 1:
                humid.axes.clear()
                humid.axes.plot(graph_data[1], graph_data[2][0])
                humid.axes.grid()
                humid.axes.set_ylabel("Humidity (%)")
                humid.axes.set_xlabel("Date and Time [M-D H]")
                humid.axes.set_title("Air Humidity Recorded by the System.")
            elif i == 2:
                press.axes.clear()
                press.axes.plot(graph_data[1], graph_data[2][0])
                press.axes.grid()
                press.axes.set_ylabel("Pressure (Pa)")
                press.axes.set_xlabel("Date and Time [M-D H]")
                press.axes.set_title("Air Pressure Detected by the System.")
            else:
                voc.axes.clear()
                voc.axes.plot(graph_data[1], graph_data[2][0])
                voc.axes.grid()
                voc.axes.set_ylabel("VOC (k\u03A9)")
                voc.axes.set_xlabel("Date and Time [M-D H]")
                voc.axes.set_title("Volatile Organic Compounds Detected by the System.")

    @staticmethod
    def export_button_clicked(headings, data):
        exporter = Exporter()
        for i in range(4):
            exporter.export(headings[i], data, "statistics.csv", unix=True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
