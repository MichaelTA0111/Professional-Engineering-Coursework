from configparser import ConfigParser


class ConfigManager:
    """
    Manager for the config file
    """
    def __init__(self, config_filename="config.ini"):
        """
        Constructor for the ConfigManager.
        :param config_filename: The name of the config file
        """
        self.__config_filename = config_filename

        try:
            file = open(self.__config_filename)
        except FileNotFoundError:
            file = open(self.__config_filename, 'x')

        file.close()

        config = ConfigParser()
        config.read(self.__config_filename)

        self.__db_file_path = "data.db"
        self.__ip_address = ""

        error_raised = False

        try:
            self.db_file_path = config['DEFAULT']['db_file_path']
            raise KeyError
        except (KeyError, TypeError, ValueError):
            error_raised = True

        try:
            self.ip_address = config['DEFAULT']['ip_address']
        except (KeyError, TypeError, ValueError):
            error_raised = True

        if error_raised:
            self.__update_configuration_file()

    def __update_configuration_file(self):
        """
        Write config data to the config file
        """
        config = ConfigParser()
        config['DEFAULT']['db_file_path'] = self.__db_file_path
        config['DEFAULT']['ip_address'] = self.__ip_address

        configfile = open(self.__config_filename, 'w')
        config.write(configfile)
        configfile.close()

    @property
    def db_file_path(self):
        """
        Getter for db_file_path
        :return: The file path the database as a string
        """
        return self.__db_file_path

    @db_file_path.setter
    def db_file_path(self, db_file_path: str):
        """
        Setter for the db_file_path
        :param db_file_path: The file path the database as a string
        """
        if not isinstance(db_file_path, str):
            raise TypeError('db_file_path must be a string')

        if not db_file_path.endswith('.db'):
            raise ValueError("db_file_path must end with substring '.db'")

        if db_file_path.count('.db') != 1:
            raise ValueError("db_file_path must can only contain substring '.db' once")

        invalid_characters = ['<', '>', ':', '"', '/', '|', '?', '*']
        if [character for character in invalid_characters if (character in db_file_path)]:
            raise ValueError('db_file_path cannot contain any of the following invalid characters: <, >, :, ", /, |, '
                             '?, *')

        self.__db_file_path = db_file_path
        self.__update_configuration_file()

    @property
    def ip_address(self):
        """
        Getter for the ip_address
        :return: The ip address of the microcontroller ss a string (None if no IP has been set yet)
        """
        if self.__ip_address:
            return self.__ip_address
        else:
            return None

    @ip_address.setter
    def ip_address(self, ip_address: str):
        """
        Setter for the ip_address
        :param ip_address: The ip address of the microcontroller as a string
        """
        if not isinstance(ip_address, str):
            raise TypeError('ip_address must be a string')

        if ip_address.count('.') != 3:
            raise ValueError('ip_address must have 3 decimal points')

        if ip_address.startswith('.'):
            raise ValueError('ip_address cannot start with a decimal point')

        if ip_address.endswith('.'):
            raise ValueError('ip_address cannot end with a decimal point')

        if '..' in ip_address:
            raise ValueError('ip_address cannot contain two or more decimal places next to each other')

        for character in ip_address:
            if not character.isdigit() and character != '.':
                raise ValueError('ip_address must only contain numbers and decimal points')

        self.__ip_address = ip_address
        self.__update_configuration_file()


if __name__ == '__main__':
    print('Please run a different source file.')
