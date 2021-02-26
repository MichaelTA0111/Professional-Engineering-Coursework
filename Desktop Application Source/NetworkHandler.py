import json


class NetworkHandler:
    """
    Class to handle the network connection
    """
    @staticmethod
    def parse_json(string):
        """
        Static method to create a list of objects from the JSON string
        :param string: The JSON string which will be received from the Mbed
        :return: A list of objects created from the JSON string
        """
        json_strings = NetworkHandler.split_strings(string)
        json_objects = []
        try:
            for i in range(len(json_strings)):
                json_objects.append(json.loads(json_strings[i]))
            if len(json_objects) > 0:
                return json_objects
            else:
                return None
        except:
            print('Error parsing the JSON string!')

    @staticmethod
    def split_strings(string):
        """
        Static method to split the JSON string into substrings which are compatible with the json library
        :param string: The JSON string which will be received from the Mbed
        :return: A list of JSON substrings
        """
        string_list = []
        while True:
            try:
                begin = string.index('{')
                end = string.index('}') + 1
                string_list.append(string[begin:end])
                string = string[end:]
            except ValueError:
                return string_list


if __name__ == '__main__':
    print('Please run a different source file.')
