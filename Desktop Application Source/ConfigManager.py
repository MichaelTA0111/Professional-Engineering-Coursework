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

        key_error_raised = False

        try:
            self.db_file_path = config['DEFAULT']['db_file_path']
            raise KeyError
        except (KeyError, TypeError, ValueError):
            key_error_raised = True

        try:
            self.ip_address = config['DEFAULT']['ip_address']
        except (KeyError, TypeError, ValueError):
            key_error_raised = True

        if key_error_raised:
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
            raise TypeError

        if db_file_path.count('.db') != 1:
            raise ValueError

        if not db_file_path.endswith('.db'):
            raise ValueError

        invalid_characters = ['<', '>', ':', '"', '/', '|', '?', '*']
        if [character for character in invalid_characters if (character in db_file_path)]:
            raise ValueError

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
            raise TypeError

        if ip_address.count('.') != 3:
            raise ValueError

        if ip_address.startswith('.'):
            raise ValueError

        if ip_address.endswith('.'):
            raise ValueError

        invalid_characters = ['..', '...']
        if [character for character in invalid_characters if (character in ip_address)]:
            raise ValueError

        for character in ip_address:
            if not character.isdigit() and character != '.':
                raise ValueError

        self.__ip_address = ip_address
        self.__update_configuration_file()


if __name__ == '__main__':
    print('Please run a different source file.')
