# General imports
from asyncore import file_dispatcher
import pandas as pd
import numpy as np
# Brainflow
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowError
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, WindowFunctions, DetrendOperations

# Abstract class / parent class
class InputSource:
    def __init__(self):
        self.params = BrainFlowInputParams()
        self.params.ip_port = 0
        self.params.serial_port = ''
        self.params.mac_address = ''
        self.params.other_info = ''
        self.params.serial_number = ''
        self.params.ip_address = ''
        self.params.ip_protocol = 0
        self.params.timeout = 0
        self.params.file = ''
        # users board
        self.board = None

    """
    Initializes the users CYTON BOARD
    """
    def init_board(self, board_id):
        self.board = BoardShim(board_id, self.params)

    """
    Starts streaming from the users board
    """
    def start_session(self):
        if self.board is None:
            self.init_board()
        self.board.prepare_session()
        self.board.start_stream(45000, '')

    """
    Stop streaming from the users board
    """
    def stop_session(self):
        self.board.stop_stream()

# HeadSet input source (recording and streaming capability)
class HeadSet(InputSource):
    def __init__(self, serial_port: str, filename = None):
        InputSource.__init__(self)
        self.params.serial_port = serial_port
        self.filename = filename
        self.board_id = 0
        self.init_board(self.board_id)

# File input source (streaming capability)
class File(InputSource):
    def __init__(self, filename):
        InputSource.__init__(self)
        self.filename = filename
        self.board_id = -3
        self.params.other_info = "0"

"""
Records timeseries data from board and stores it in the given filename

params: the users current board where they are gathering data,
        a filename where the data will be stored
output: nothing is explicitly returned
"""
def record(board, filename):
    data = board.get_board_data()  
    # board.stop_stream()
    # board.release_session()

    df = pd.DataFrame(np.transpose(data))
    print('Data From the Board')
    print(df.head(10))

    DataFilter.write_file(data, filename, 'w')  # use 'a' for append mode
