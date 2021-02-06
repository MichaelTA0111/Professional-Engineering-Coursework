from statistics import mean, median, multimode, quantiles, pstdev, pvariance


class StatisticsManager:
    """
    Class to calculate all required statistics from the data given
    """

    def __init__(self, data, time):
        """
        Constructor for the statistics manager class
        :param data: The formatted data as an array
        :param time: The formatted time as an array
        """
        self.__mean = mean(data)
        self.__median = median(data)
        self.__mode = multimode(data)
        self.__range = self.__calculate_range(data)
        self.__iqr = self.__calculate_iqr(data)
        self.__sd = pstdev(data)
        self.__variance = pvariance(data)
        self.__max = max(data)
        self.__max_time = self.__calculate_max_time(data, time)
        self.__min = min(data)
        self.__min_time = self.__calculate_min_time(data, time)

    def print_statistics(self):
        """
        Temporary method to print the statistics in a formatted way
        Will be replaced when the GUI is prepared
        """
        print('Mean: ' + "{:.2f}".format(self.__mean))
        print('Median: ' + "{:.2f}".format(self.__median))
        mode = ''
        for i in range(len(self.__mode)):
            if i != 0:
                mode += ', '
            mode += "{:.2f}".format(self.__mode[i])
        print('Mode: ' + mode)
        print('Range: ' + "{:.2f}".format(self.__range))
        print('Interquartile Range: ' + "{:.2f}".format(self.__iqr))
        print('Standard Deviation: ' + "{:.2f}".format(self.__sd))
        print('Variance: ' + "{:.2f}".format(self.__variance))
        print('Maximum: ' + "{:.2f}".format(self.__max))
        print('Time at Maximum: ' + str(self.__max_time))
        print('Minimum: ' + "{:.2f}".format(self.__min))
        print('Time at Minimum: ' + str(self.__min_time))

    def get_mean(self):
        """
        Getter for the mean
        :return: The mean
        """
        return self.__mean

    def get_median(self):
        """
        Getter for the median
        :return: The median
        """
        return self.__median

    def get_mode(self):
        """
        Getter for the mode
        :return: The mode
        """
        return self.__mode

    def get_range(self):
        """
        Getter for the range
        :return: The range
        """
        return self.__range

    def get_iqr(self):
        """
        Getter for the interquartile range
        :return: The interquartile range
        """
        return self.__iqr

    def get_sd(self):
        """
        Getter for the standard deviation
        :return: The standard deviation
        """
        return self.__sd

    def get_variance(self):
        """
        Getter for the variance
        :return: The variance
        """
        return self.__variance

    def get_max(self):
        """
        Getter for the maximum value
        :return: The maximum value
        """
        return self.__max

    def get_max_time(self):
        """
        Getter for the time at which the maximum value occurs
        :return: The time at which the maximum value occurs
        """
        return self.__max_time

    def get_min(self):
        """
        Getter for the minimum value
        :return: The minimum value
        """
        return self.__min

    def get_min_time(self):
        """
        Getter for the time at which the minimum value occurs
        :return: The time at which the minimum value occurs
        """
        return self.__min_time

    @staticmethod
    def __calculate_range(data):
        """
        Private static method to calculate the range of the data
        :param data: The data as an array
        :return: The range of the data
        """
        data_range = sorted(data)[-1] - sorted(data)[0]
        return data_range

    @staticmethod
    def __calculate_iqr(data):
        """
        Private static method to calculate the interquartile range
        :param data: The data as an array
        :return: The interquartile range of the data
        """
        inter_quartile_range = quantiles(data)[2] - quantiles(data)[0]
        return inter_quartile_range

    @staticmethod
    def __calculate_max_time(data, time):
        """
        Private static method to calculate the time at which the maximum value occurs
        :param data: The data as an array
        :return: The time at which the maximum value occurs
        """
        index = data.index(max(data))  # Determine the index for the maximum value of V_e
        max_time = time[index]  # Determine x_e_star from the index of V_e_max
        return max_time

    @staticmethod
    def __calculate_min_time(data, time):
        """
        Private static method to calculate the time at which the minimum value occurs
        :param data: The data as an array
        :return: The time at which the minimum value occurs
        """
        index = data.index(min(data))  # Determine the index for the maximum value of V_e
        max_time = time[index]  # Determine x_e_star from the index of V_e_max
        return max_time


if __name__ == '__main__':
    print('Please run a different source file.')
