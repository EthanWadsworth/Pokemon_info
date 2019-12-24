import csv


class CSV:

    def __init__(self, dataframe, name):
        """
        :param dataframe: 2D list of strings to be appended to the csv file
        :param name: name of the csv file or the path to the file
        """
        self.dataframe = dataframe
        self.name = name

    def csv_write(self):
        """
        Appends rows to the csv file specified using the entered dataframe
        :return: no return type
        """
        with open(self.name, 'a') as file:
            writer = csv.writer(file)
            for row in self.dataframe:
                writer.writerow(row)

    def create_file(self, header_list):
        """
        Creates a new csv file with the desired header in the specified directory
        :param header_list: A list of strings used to create the header rows of the new csv file
        :return: no return type
        """
        with open(self.name, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(header_list)

