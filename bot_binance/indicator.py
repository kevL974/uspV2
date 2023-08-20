from typing import List


def sma(values: List, window_size: int) -> List:
    """
    Calculate simple moving average values from a list of value according to window size given in parameter
    @param values: a list of element
    @param window_size: a number that defines the size of window
    @return: List of simple moving average
    """
    nb_values = len(values)
    moving_average = [None] * nb_values
    index_values = 0
    iem_values = 1
    while iem_values <= nb_values:

        if iem_values - window_size >= 0:
            average_i = sum(values[(iem_values - window_size):iem_values])/window_size
            moving_average[index_values] = average_i

        iem_values += 1
        index_values += 1

    return moving_average
