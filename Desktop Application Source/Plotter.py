import matplotlib.pyplot as plt


class Plotter:
    """
    Class for plotting graphs
    """
    def __init__(self, x_axis, y_axis, labels, file_path):
        """
        Constructor for the plotter object
        :param x_axis: The points to be plotted on the x-axis as an array
        :param y_axis: The points to be plotted on the y-axis as a 2D array
        :param labels: The labels of the plots to be made
        :param file_path: The file path where the image will be saved
        """
        self.__x_axis = x_axis
        self.__y_axis = y_axis
        self.__labels = labels
        self.__file_path = file_path

        self.__legend = False  # Boolean to determine if a legend will be displayed
        self.__legend_title = None  # Title of the legend
        self.__y_label = None  # Label of the y-axis
        self.__determine_plot_details()

    def plot(self):
        """
        Method to plot a graph of a given measurement against date & time
        """
        self.__plot_points()
        plt.xlabel('Date & Time')  # Label the x-axis
        plt.ylabel(self.__y_label)  # Label the y-axis
        plt.grid()  # Produces a grid on the graph
        if self.__file_path is not None:
            plt.savefig(self.__file_path)  # Save the graph
        plt.show()  # Displays the graph

    def __determine_plot_details(self):
        """
        Private helper method to determine details of the graph to be plotted
        """
        if 'Temperature' in self.__labels:
            self.__y_label = 'Temperature ($^\circ$C)'
        elif 'Humidity' in self.__labels:
            self.__y_label = 'Humidity (%)'
        else:
            self.__legend = True
            self.__legend_title = 'Gas:'
            self.__y_label = 'Concentration (µg/m³)'

    def __plot_points(self):
        """
        Private helper method to plot points on a graph
        """
        if self.__legend:
            for i in range(len(self.__y_axis)):  # Plot each line on the graph with labels
                plt.plot(self.__x_axis, self.__y_axis[i], label=self.__labels[i])
            plt.legend(title=self.__legend_title)  # Insert the legend with an optional title
        else:
            for i in range(len(self.__y_axis)):  # Plot each line on the graph without labels
                plt.plot(self.__x_axis, self.__y_axis[i])


if __name__ == '__main__':
    print('Please run a different source file.')
