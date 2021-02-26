import sqlite3
from sqlite3 import Error
from TimeConverter import TimeConverter as Tc
from Plotter import Plotter

dtu = Tc.date_to_unix
utd = Tc.unix_to_date


class DatabaseManager:
    """
    A class to manage an sqlite database.
    Some code used from https://www.sqlitetutorial.net/
    """
    def __init__(self, file_name):
        """
        Constructor for the database manager class
        :param file_name: The file path of the database to be queried
        """
        self.__file_name = file_name
        self.__conn = self.__create_connection()
        self.__valid = self.__conn is not None

    def __create_connection(self):
        """
        Helper method to create a connection to a new or already existing database.
        :return: Connection object of the database or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.__file_name)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_table(self, create_table_sql):
        """
        Create a table using the create_table_sql statement
        :param create_table_sql: A CREATE TABLE statement
        """
        try:
            c = self.__conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def is_valid(self):
        """
        Checks whether the database manager is valid
        :return:
        """
        return self.__valid

    def close(self):
        """
        Close the connection to the database.
        """
        if self.__conn:
            self.__conn.close()

    def query(self, time_range, columns):
        """
        Method to query the database for certain measurements in a certain time range
        :param time_range: The start and end time_range to be queried as unix timestamps
        :param columns: The column headers from the SQL database which are to be queried
        :return: The data obtained from the query
        """
        try:
            c = self.__conn.cursor()
            c.execute(f'SELECT {columns} FROM data_table WHERE timestamp BETWEEN ? AND ?',
                      (time_range[0], time_range[1]))
            data = c.fetchall()
            return data
        except Error as e:
            print(e)
            return

    def insert(self, data):
        """
        Method to insert data into database
        :param data: The data to be inserted into the database as an array of JSON objects
        """
        try:
            c = self.__conn.cursor()
            for i in range(len(data)):
                c.execute('''INSERT INTO data_table(timestamp, temperature, carbon_monoxide, nitric_oxide,
                             nitrogen_dioxide, sulphur_dioxide) VALUES(?,?,?,?,?,?)''',
                          (data[i]['timeAlive'],
                           data[i]['temperature'],
                           data[i]['carbonMonoxide'],
                           data[i]['nitricOxide'],
                           data[i]['nitrogenDioxide'],
                           data[i]['sulphurDioxide']))
            self.__conn.commit()
        except Error as e:
            print(e)


def determine_heading_labels(headings):
    """
    Function to determine the labels to be used in the legend of the graph
    :param headings: The column headings which are being queried
    :return: An array of the labels as strings
    """
    heading_labels = headings.split(', ')  # Split the headings into individual strings in an array
    labels = []
    for string in heading_labels:
        i = 0
        make_upper = [0]  # An array to store the letters which are to be capitalised
        label = ''
        for char in string:
            if char == '_':
                label += ' '  # Convert all underscores to spaces
                make_upper.append(i + 1)  # Capitalise each new word
            elif i in make_upper:
                label += char.upper()  # Add a capital letter
            else:
                label += char  # Add a character
            i += 1
        labels.append(label)
    return labels


def format_data(raw_data, headings):
    """
    Function to format raw data read from the database
    :param raw_data: The raw data read from the database
    :param headings: The headings which were queried
    :return: The time and corresponding measurements after required formatting
    """
    formatted_time = []
    for element in raw_data:
        formatted_time.append(utd(element[0]))

    formatted_measurements = []
    for i in range(len(headings.split(', '))):
        formatted_measurements.append([])
        for element in raw_data:
            formatted_measurements[i].append(element[i + 1])

    return formatted_time, formatted_measurements


def db_read(time_range, headings, db_file_path=r"data.db", plot_graph=True, graph_file_path=None):
    """
    Function to read the database
    :param time_range: The start and end times to be queried as unix timestamps
    :param headings: The column headings which are being queried
    :param db_file_path: The file path of the database to be queried
    :param plot_graph: Boolean to determine if the results should be plotted
    :param graph_file_path: The file path to save the graph to
    :return: The raw data and the formatted time with corresponding measurements
    """
    db = DatabaseManager(db_file_path)  # Open a database
    sql_create_projects_table = '''CREATE TABLE IF NOT EXISTS data_table (timestamp integer PRIMARY KEY,
                                                                          temperature real,
                                                                          carbon_monoxide real,
                                                                          nitric_oxide real,
                                                                          nitrogen_dioxide real,
                                                                          sulphur_dioxide real);'''
    db.create_table(sql_create_projects_table)

    query_headings = 'timestamp, ' + headings
    raw_data = db.query(time_range, query_headings)  # Query the database for the given columns and timestamps
    formatted_time, formatted_measurements = format_data(raw_data, headings)  # Format the raw data

    if plot_graph:
        labels = determine_heading_labels(headings)  # Determine the labels to be used
        Plotter(formatted_time, formatted_measurements, labels, graph_file_path).plot()  # Plot the desired graph

    db.close()  # Close the database

    return raw_data, formatted_time, formatted_measurements


def db_write(data, db_file_path=r"data.db"):
    """
    Function to write to the database
    :param data: The data to be written to the database
    :param db_file_path: The file path of the database to be written to
    """
    try:
        if data is not None:
            db = DatabaseManager(db_file_path)  # Open a database
            sql_create_projects_table = '''CREATE TABLE IF NOT EXISTS data_table (timestamp integer PRIMARY KEY,
                                                                                  temperature real,
                                                                                  carbon_monoxide real,
                                                                                  nitric_oxide real,
                                                                                  nitrogen_dioxide real,
                                                                                  sulphur_dioxide real);'''
            db.create_table(sql_create_projects_table)

            db.insert(data)  # Insert data into the database

            db.close()  # Close the database
        else:
            print('No data to be written!')
    except:
        print('Error writing to database')


if __name__ == '__main__':
    print('Please run a different source file.')
