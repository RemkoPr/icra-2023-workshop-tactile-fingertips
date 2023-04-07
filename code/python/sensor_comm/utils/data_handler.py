import itertools
import os
import csv
from loguru import logger
from datetime import *

from sensor_comm.utils.general import *


def create_unique_file_name(directory, preamble=None, extension='.csv'):
    # Build the file name so that each experiment (a.k.a. each run of the code) saves data to a different file

    file_name = str(date.today())
    if preamble:
        file_name = preamble + file_name
    file_number = 0
    for file_in_dir in os.listdir(directory):
        if file_in_dir.startswith(file_name):
            val = int(file_in_dir[file_in_dir.find("[") + 1:file_in_dir.find("]")])
            if val > file_number:
                file_number = val
    file_name = file_name + "[" + str(file_number + 1) + "]" + extension

    return file_name


class DataHandler:
    def __init__(self, devices, directory, buffer_size=10):
        self.directory = directory
        self.init_directory(self.directory)
        self.file_name = create_unique_file_name(directory)
        self.csv_header = None
        self.buffer = []
        self.max_buffer_size = buffer_size
        self.devices = devices
        self.current_data = None

    def init_directory(self, directory):
        """
        Checks if directory exists, if not, creates it
        :param directory: directory to check
        """
        if not os.path.exists(directory):
            ans = input("Make new directory (" + directory + ")? [Y/N] ")
            if ans.lower() == "y":
                os.makedirs(directory)
            elif ans.lower() == "n":
                raise NotADirectoryError("Data directory doesn't exist, creation cancelled by user.")
            else:
                raise ValueError("Invalid answer given, enter [Y] or [N].")

    def init_csv_file(self, directory, file_name):
        if self.csv_header:
            with open(os.path.join(directory, file_name), 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=';')
                csv_writer.writerow(self.csv_header)

    def data_convert(self, data):
        """
        Convert data to a sensible form for logging and storage in the class, e.g. convert bytearray to array of 16b ints.
        If such a conversion is not needed, simply return out of the function. This data format should also be a proper
        starting point for the visualiser.
        """
        raise NotImplementedError

    def persist(self, data, device):
        """
        Persists a single readout from a single device
        :param data: list, the data
        :param device: string, the MAC address of the device
        """
        self.buffer.append([device, datetime.now()] + data)

        if len(self.buffer) > self.max_buffer_size:
            self._persist_to_file()
            self.buffer = []

    def _persist_to_file(self):
        with open(os.path.join(self.directory, self.file_name), 'a+', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';')
            for row in self.buffer:
                csv_writer.writerow(row)
        logger.debug("Wrote to file")


class SmartTexDataHandler(DataHandler):
    def __init__(self, devices, directory="./data/smart_textile", buffer_size=10, grid_size=(7, 7)):
        super().__init__(devices, directory, buffer_size=buffer_size)
        grid_height = grid_size[0]
        grid_width = grid_size[1]
        self.csv_header = ['PCB addr', 'timestamp', 'LowBattery'] + \
                 [f'sensor_value_{digital_pin}_{analog_pin}'
                  for digital_pin, analog_pin in itertools.product(range(grid_width), range(grid_height))]
        self.init_csv_file(self.directory, self.file_name)

    def data_convert(self, data):
        return data


class Cap2SenseDataHandler(DataHandler):
    def __init__(self, devices, directory="./data/cap2sense", buffer_size=10, grid_size=(6, 6)):
        super().__init__(devices, directory, buffer_size=buffer_size)
        self.grid_height = grid_size[0]
        self.grid_width = grid_size[1]

        # TODO: make proper header
        self.csv_header = ['PCB addr', 'timestamp', 'LowBattery'] + \
                 [f'sensor_value_{digital_pin}_{analog_pin}'
                  for digital_pin, analog_pin in itertools.product(range(self.grid_width), range(self.grid_height))]
        self.init_csv_file(self.directory, self.file_name)

    def data_convert(self, data):
        data16 = data_bytes_to_uint16(data)
        return data16


class CapSenseDataHandler(DataHandler):
    def __init__(self, devices, directory="./data/capsense", buffer_size=10, grid_size=(6, 6)):
        super().__init__(devices, directory, buffer_size=buffer_size)
        self.grid_height = grid_size[0]
        self.grid_width = grid_size[1]

        # TODO: make proper header
        self.csv_header = ['PCB addr', 'timestamp', 'LowBattery'] + \
                          [f'sensor_value_{digital_pin}_{analog_pin}'
                           for digital_pin, analog_pin in
                           itertools.product(range(self.grid_width), range(self.grid_height))]
        self.init_csv_file(self.directory, self.file_name)

    def data_convert(self, data):
        data16 = data_bytes_to_uint16(data)
        '''data_converted = []

        connectivity_matrix = np.array([[0, 1, 1, 1, 1],
                                        [1, 0, 1, 1, 1],
                                        [1, 1, 0, 1, 1],
                                        [1, 1, 1, 0, 1],
                                        [1, 1, 1, 1, 0]])
        conversion_matrix = np.linalg.inv(connectivity_matrix)
        for i in range(self.grid_size[0]):
            start_idx = i * self.grid_size[1]
            end_idx = (i + 1) * self.grid_size[1]
            data_column = (np.array(data16[start_idx:end_idx]))
            conversion_result = np.dot(conversion_matrix, data_column)
            data_converted += list(conversion_result)
        return data_converted'''
        return data16


class CapTouchDataHandler(DataHandler):
    """
        Writes to a buffer and periodically flushes to file system.
    """

    def __init__(self, devices, cins, directory="./data/captouch", buffer_size=10, grid_size=(3, 2)):
        super().__init__(devices, directory, buffer_size=buffer_size)
        self.csv_header = ['PCB addr', 'timestamp', ]  # + self.cins
        self.init_csv_file(self.directory, self.file_name)
        self.cins = cins
        self.grid_height = grid_size[0]
        self.grid_width = grid_size[1]
        assert(len(cins) == self.grid_width * self.grid_height)

    def data_convert(self, data):
        return data_bytes_to_uint16(data)


class IRTouchDataHandler(DataHandler):
    def __init__(self, devices, directory="./data/irtouch", buffer_size=10, grid_size=(3, 2)):
        super().__init__(devices, directory, buffer_size=buffer_size)
        self.csv_header = ['MAC', 'timestamp']
        self.init_csv_file(self.directory, self.file_name)

    def data_convert(self, data):
        """
        Data is 8bit, received from bytearray, no conversion needed.
        """
        for i in range(len(data)):
            data[i] = 255 - data[i]
        return data

class PolyPiezoDataHandler(DataHandler):
    def __init__(self, devices, directory="./data/smart_textile", buffer_size=10, grid_size=(7, 7)):
        super().__init__(devices, directory, buffer_size=buffer_size)
        grid_height = grid_size[0]
        grid_width = grid_size[1]
        self.csv_header = ['PCB addr', 'timestamp'] + \
                 [f'sensor_value_{digital_pin}_{analog_pin}'
                  for digital_pin, analog_pin in itertools.product(range(grid_width), range(grid_height))]
        self.init_csv_file(self.directory, self.file_name)

    def data_convert(self, data):
        return data
