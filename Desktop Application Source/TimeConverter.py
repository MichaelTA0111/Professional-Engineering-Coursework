from datetime import datetime as dt
from time import mktime


class TimeConverter:
    """
    Static class to convert time between different formats
    """
    @staticmethod
    def date_to_unix(date_str):
        """
        Function to convert time from the format DD/MM/YYYY HH:MM:SS to a unix timestamp
        :param date_str: The date as a string
        :return: The date as a unix timestamp
        """

        date = [int(date_str[6] + date_str[7] + date_str[8] + date_str[9]),
                int(date_str[3] + date_str[4]),
                int(date_str[0] + date_str[1])]
        if len(date_str) >= 12:
            date.append(int(date_str[11] + date_str[12]))
        if len(date_str) >= 15:
            date.append(int(date_str[14] + date_str[15]))
        if len(date_str) == 18:
            date.append(int(date_str[17] + date_str[18]))
        while len(date) < 6:
            date.append(0)
        date = int(mktime(dt(date[0], date[1], date[2], date[3], date[4], date[5]).timetuple()))
        return date

    @staticmethod
    def unix_to_date(date_unix):
        """
        Function to convert time from a unix timestamp to the format DD/MM/YYYY HH:MM:SS
        :param date_unix: The date as a unix timestamp
        :return: The date as a datetime object
        """
        date = dt.utcfromtimestamp(date_unix).strftime('%d/%m/%Y %H:%M:%S')
        date = dt.strptime(date, '%d/%m/%Y %H:%M:%S')
        return date


if __name__ == '__main__':
    print('Please run a different source file.')
