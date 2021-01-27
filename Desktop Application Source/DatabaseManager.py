import sqlite3
from sqlite3 import Error


class DatabaseManager:
    """
    A class to manage an sqlite database.
    Some code gotten from https://www.sqlitetutorial.net/
    """
    def __init__(self, file_name):
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
