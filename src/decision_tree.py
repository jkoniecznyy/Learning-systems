from math import log2

from src.utils import *
from collections import Counter


def get_values(data: list[list[str]]) -> list[int]:
    """
    Returns how many values there are for each attribute
    for example: [3, 2, 2, 2]
    """
    return [len(set(column)) for column in zip(*data)]


def get_occurrences(data: list[list[str]]) -> list[dict[str, int]]:
    """
    Returns how many times each value occurs
    for example: [{'old': 3, 'mid': 4, 'new': 3}, {'yes': 4, 'no': 6}]
    """
    return [dict(Counter(column)) for column in zip(*data)]


def get_probabilities(data: list[dict[str, int]]) -> list[list[float]]:
    """
    Returns the probability for each value
    for example: [[0.3, 0.4, 0.3], [0.4, 0.6]]
    """
    all_probabilities = []
    for column in data:
        probability = []
        for attribute in column.values():
            probability.append(attribute / sum(column.values()))
        all_probabilities.append(probability)
    return all_probabilities


def calculate_entropy(data: list[float]) -> float:
    """
    Returns the entropy for a given list of probabilities
    for example: 0.5
    """
    # print('calculate_entropy', data)
    return -(sum([p * log2(p) for p in data if p != 0]))


def get_entropy(data: list[list[float]]) -> float:
    """
    Returns the entropy value for the last attribute from data
    for example: 0.5
    """
    # print('data', data)
    # print('data[-1]', data[-1])
    # print('get_entropy', data)
    return calculate_entropy(data[-1])


def get_information(data: list[list[str]], occurrences) -> list[float]:
    """ Returns information """
    information = []
    for index in range(len(occurrences) - 1):
        class_information = 0
        for attribute in occurrences[index].keys():
            class_information = calculate_class_information(data, class_information, attribute, index)
        information.append(class_information)
    return information


def get_split_information(probabilities: list[list[float]]) -> list[float]:
    """
    Compute the split information, i.e. calculate the entropy for each attribute
    """
    split_information = []
    for index in range(len(probabilities) - 1):
        split_information.append(calculate_entropy(probabilities[index]))
    return split_information


def calculate_class_information(data: list[list[str]], class_information, attribute, index) -> list[float]:
    """ Returns class information """
    # print('calculate_class_information', data, class_information, attribute, index)
    class_values = [row for row in data if row[index] == attribute]

    occurrences = get_occurrences(class_values)
    class_probabilities = get_probabilities(occurrences)
    entropy = get_entropy(class_probabilities)

    class_information += len(class_values) / len(data) * entropy
    return class_information


def get_gain(information, entropy) -> list[float]:
    """
    Compute the information gain for all attribute classes
    """
    return [(entropy - value) for value in information]


def get_gain_ratio(gain: list[float], split_info: list[float]) -> list[float]:
    """
    Balance the disproportions
    """
    gain_ratio = []
    for attribute in range(len(gain)):
        if split_info[attribute] > 0:
            gain_ratio.append(gain[attribute] / split_info[attribute])
        else:
            gain_ratio.append(0)

    return gain_ratio


def decision_tree(data, prev=-1):
    occurrences = get_occurrences(data)
    probabilities = get_probabilities(occurrences)

    entropy = calculate_entropy(probabilities[-1])
    information = get_information(data, occurrences)
    # print(f'information = {information}')
    gain = get_gain(information, entropy)
    # print(f'gain = {gain}')

    split_information = get_split_information(probabilities)
    # print(f'split_info = {split_information}')

    gain_ratio = get_gain_ratio(gain, split_information)
    # print(f'gain_ratio = {gain_ratio}')

    best_attribute = gain_ratio.index(max(gain_ratio))

