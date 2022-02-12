# File functions
from graph import display_data
from hardware_interfacing import HeadSet, File
from classifying import spectral_analysis
from processing import apply_bandpass, get_fft
from label import import_json
# General imports
import json
import time
# Brainflow
from brainflow import BoardShim

def main():
    # initializes an input object
    input_source = HeadSet("/dev/cu.usbserial-DM0258JS", "testing")

    # starts visualization stream
    display_data(input_source, "fft")

    # testing real time classification
    time.sleep(4)

    sec = 3
    samp_rate = BoardShim.get_sampling_rate(input_source.board_id)

    while (True):
        # get the last sec * samp_rate samples of data
        data = input_source.board.get_current_board_data(sec * samp_rate)

        # applying bandpass to enhance frequency range we are looking at
        apply_bandpass(data, BoardShim.get_sampling_rate(input_source.board_id), range=(8, 32))

        # get FFT 
        fft = get_fft(data, BoardShim.get_sampling_rate(input_source.board_id))

        # prediction is based on the max power of the FFT for channel 8 (index 7)
        prediction = spectral_analysis(fft[7])

        # sleep to stop loop from happening too fast
        time.sleep(0.5)


if __name__ == "__main__":
    main()