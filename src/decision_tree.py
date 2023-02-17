from math import log2

from src.utils import *
from collections import Counter


def calculate_unique_values(data: list[list[str]]) -> list[int]:
    """ Returns the number of unique values for each attribute """
    unique_values = []
    for column in zip(*data):
        unique_values.append(len(set(column)))
    return unique_values


def calculate_unique_values2(data: list[list[str]]) -> list[int]:
    """ Returns the number of unique attribute """
    return [len(set(column)) for column in zip(*data)]


def calculate_different_occurrences(data: list[list[str]]) -> list[dict[str, int]]:
    """ Returns number of different occurrences for each attribute """
    different_occurrences = []
    for column in zip(*data):
        different_occurrences.append(dict(Counter(column)))
    return different_occurrences


def calculate_different_occurrences2(data: list[list[str]]) -> list[dict[str, int]]:
    """ Returns number of different occurrences of attributes """
    return [dict(Counter(column)) for column in zip(*data)]


def calculate_probabilities(occurrences: list[dict[str, int]]):
    """ Returns the probability for each attribute  """
    probabilities = []
    for column in occurrences:
        probability = []
        for attribute in column.values():
            probability.append(attribute / sum(column.values()))
        probabilities.append(probability)

    return probabilities


def calculate_probabilities2(occurrences: list[dict[str, int]]):
    """ Returns the probability for each attribute  """
    return [[attribute / sum(column.values()) for attribute in column.values()] for column in occurrences]


def calculate_entropy(probability: list[list[float]]) -> float:
    """ Returns the entropy  """
    return -sum([p * log2(p) for p in probability[-1] if p != 0])


def calculate_information(data: list[list[str]], unique_values: list[int], occurrences) -> list[float]:
    """ Returns information """
    information = []
    for index in range(len(unique_values) - 1):
        class_information = 0
        for attribute in occurrences[index].keys():
            class_values = [row for row in data if row[index] == attribute]
            class_probabilities = calculate_probabilities2(calculate_different_occurrences2(class_values))
            class_information += len(class_values) / len(data) * calculate_entropy(class_probabilities)
        information.append(class_information)
    return information


def calculate_information2(data: list[list[str]], unique_values: list[int], occurrences) -> list[float]:
    """ Returns information """
    information = []
    for index in range(len(unique_values) - 1):
        class_information = 0
        for attribute in occurrences[index].keys():
            class_information = calculate_class_information(data, class_information, attribute, index)
        information.append(class_information)
    return information


def calculate_class_information(data: list[list[str]], class_information, attribute, index) -> list[float]:
    """ Returns class information """
    class_values = [row for row in data if row[index] == attribute]
    class_probabilities = calculate_probabilities2(calculate_different_occurrences2(class_values))
    class_information += len(class_values) / len(data) * calculate_entropy(class_probabilities)
    return class_information


def decision_tree():
    data = read_file('data/gielda.txt')
    # data = read_file('data/test2.txt')
    # data = read_file('data/breast-cancer.data')
    # print(f'data = {data}')
    unique_values = calculate_unique_values2(data)
    # print(f'cc2 = {cc2}')
    different_occurrences = calculate_different_occurrences2(data)
    # print(f'listcomp = {oc2}')
    # p1 = calculate_probabilities(oc2)
    # print(f'p1 = {p1}')
    p2 = calculate_probabilities2(different_occurrences)
    print(f'p2 = {p2}')
    entropy = calculate_entropy(p2)
    print(f'entropy = {entropy}')
    # info2 = calculate_information(data, unique_values, different_occurrences)
    # print(f'info2 = {info2}')
    info3 = calculate_information2(data, unique_values, different_occurrences)
    print(f'info3 = {info3}')

    return 0
