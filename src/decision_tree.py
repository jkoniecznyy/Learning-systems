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
    print('calculate_entropy', data)
    return -(sum([p * log2(p) for p in data if p != 0]))


def get_entropy(data: list[list[float]]) -> float:
    """
    Returns the entropy value for the last attribute from data
    for example: 0.5
    """
    print('data', data)
    print('data[-1]', data[-1])
    print('get_entropy', data)
    return calculate_entropy(data[-1])


def calculate_information2(data: list[list[str]], values: list[int], occurrences) -> list[float]:
    """ Returns information """
    values = get_values(data)
    occurrences = get_occurrences(data)
    information = []
    for index in range(len(values) - 1):
        class_information = 0
        for attribute in occurrences[index].keys():
            class_information = calculate_class_information(data, class_information, attribute, index)
        information.append(class_information)
    return information


def calculate_class_information(data: list[list[str]], class_information, attribute, index) -> list[float]:
    """ Returns class information """
    print('calculate_class_information', data, class_information, attribute, index)
    class_values = [row for row in data if row[index] == attribute]

    occurrences = get_occurrences(class_values)
    class_probabilities = get_probabilities(occurrences)
    entropy = get_entropy(class_probabilities)

    class_information += len(class_values) / len(data) * entropy
    return class_information


def calculate_gain(entropy: float, info: list[float]) -> list[float]:
    """
    Compute the information gain for all attribute classes
    """
    return [(entropy - attribute) for attribute in info]


def calculate_split_info(attribute_index: int, probabilities: list[list[float]]) -> float:
    """
    Compute the split information, i.e. calculate the entropy for each attribute
    """
    return calculate_entropy(probabilities[attribute_index])


def calculate_gain_ratio(gain: list[float], split_info: list[float]) -> list[float]:
    """
    Balance the disproportions
    """
    return [
        (gain[attribute] / split_info[attribute]) if split_info[attribute] > 0 else 0
        for attribute in range(len(gain))
    ]


def find_best_attribute(gain_ratio: list[float]) -> int:
    """
    Selection of the attribute according to which the division will be made in the decision tree.
    The function returns the index of the attribute class.
    """
    return gain_ratio.index(max(gain_ratio))


def decision_tree(data, prev=-1):
    values = get_values(data)
    print(f'values = {values}')
    occurrences = get_occurrences(data)
    print(f'occurrences = {occurrences}')
    # p1 = get_probabilities(occurrences)
    # print(f'p1 = {p1}')
    probabilities = get_probabilities(occurrences)
    print(f'probabilities = {probabilities}')
    entropy = calculate_entropy(probabilities[-1])
    print(f'entropy = {entropy}')
    information = calculate_information2(data, values, occurrences)
    print(f'information = {information}')
    # gain = calculate_gain(entropy, info)
    # print(f'gain = {gain}')

    # split_info = [
    #     calculate_split_info(index, p2) for index in range(len(values) - 1)
    # ]
    # gain_ratio = calculate_gain_ratio(gain, split_info)
    #
    # max_gain_ratio = max(gain_ratio)
    # best_attribute = find_best_attribute(gain_ratio)
    # margin = "\t"
    # if max_gain_ratio > 0:  # warunek stopu
    #     if prev != -1:
    #         print("1")
    #         print(
    #             f"{margin}"
    #             f"{print_attribute_value(occurrences, prev)} --> Atrybut: {best_attribute + 1} "
    #         )
    #     else:
    #         print("2")
    #         print(
    #             f"Atrybut: {best_attribute + 1}"
    #         )
    #
    #     prev = best_attribute
    #     margin += "\t"
    #     new_data = [
    #         [x for x in data if x[best_attribute] == key]
    #         for key in occurrences[best_attribute]
    #     ]
    #
    #     for subset in new_data:
    #         decision_tree(subset, prev, )
    # else:
    #     print("3")
    #     print(
    #         f"{margin}{print_attribute_value(occurrences, prev)} --> Decyzja: "
    #         f"{print_decision(occurrences, data)}"
    #     )

    return 0
