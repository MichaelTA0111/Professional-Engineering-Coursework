from TimeConverter import TimeConverter as Tc


utds = Tc.unix_to_date_string


class Exporter:
    """
    Static class to export data as a csv
    """
    @staticmethod
    def export(headings, data, file_path, unix=False):
        """
        Static method to export the data as a csv
        :param headings: The headings that were queried in the database
        :param data: The data as an array
        :param file_path: The file path to store the csv
        :param unix: Boolean to save the time as a unix timestamp or a date and time
        """
        if unix:
            headings = 'timestamp,' + headings.replace(', ', ',')
        else:
            headings = 'date_and_time,' + headings.replace(', ', ',')
            for i in range(len(data)):
                data[i] = list(data[i])
                data[i][0] = utds(data[i][0])

        try:
            f = open(file_path, 'x')  # Create the csv file
            f.close()

            f = open(file_path, 'a')  # Write to the csv file
            f.write(headings)
            for i in range(len(data)):
                f.write('\n' + ','.join(map(str, data[i])))
            f.close()
        except FileExistsError:
            print('File already exists!')


if __name__ == '__main__':
    print('Please run a different source file.')
