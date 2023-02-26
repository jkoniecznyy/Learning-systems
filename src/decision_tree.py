from math import log2

from collections import Counter


def get_values(data: list[list[str]]) -> list[int]:
    """
    Returns how many values there are for each attribute
    input: [['old', 'yes', 'swr', 'down'], ...]
    output: [3, 2, 2, 2]
    """
    return [len(set(column)) for column in zip(*data)]


def get_occurrences(data: list[list[str]]) -> list[dict[str, int]]:
    """
    Returns how many times each value occurs
    input: [['old', 'yes', 'swr', 'down'], ...]
    output: [{'old': 3, 'mid': 4, 'new': 3}, {'yes': 4, 'no': 6}, ...]
    """
    return [dict(Counter(column)) for column in zip(*data)]


def get_probabilities(occurrences: list[dict[str, int]]) -> list[list[float]]:
    """
    Returns the probability for each value
    input: [{'old': 3, 'mid': 4, 'new': 3}, {'yes': 4, 'no': 6}, ...]
    output: [[0.3, 0.4, 0.3], [0.4, 0.6], ...]
    """
    all_probabilities = []
    for column in occurrences:
        probability = []
        for attribute in column.values():
            probability.append(attribute / sum(column.values()))
        all_probabilities.append(probability)
    return all_probabilities


def get_entropy(probabilities: list[float]) -> float:
    """
    Returns the entropy for a given list of probabilities
    input: [0.5, 0.5]
    output: 1.0
    """
    return -(sum([p * log2(p) for p in probabilities if p != 0]))


def calculate_class_information(data: list[list[str]], class_information: list[float],
                                attribute: str, index: int) -> list[float]:
    """ Calculates the information for a given attribute """
    print(f'attribute = {attribute}')
    print(f'index = {index}')
    # print(f'data = {data}')
    # print()
    class_values = [row for row in data if row[index] == attribute]
    occurrences = get_occurrences(class_values)
    class_probabilities = get_probabilities(occurrences)
    entropy = get_entropy(class_probabilities[-1])
    print("class_information = ", class_information)
    print("+= ", len(class_values) / len(data) * entropy)
    class_information += len(class_values) / len(data) * entropy
    print("class_information = ", class_information)
    return class_information


def get_information(data: list[list[str]], occurrences: list[dict[str, int]]) -> list[float]:
    """
    Returns information
    input:
        data = [['old', 'yes', 'swr', 'down'], ...]
        occurrences = [{'old': 3, 'mid': 4, 'new': 3}, ...]
    output:
        information = [0.4, 0.875..., 1.0]
    """
    information = []
    for index in range(len(occurrences) - 1):
        class_information = 0
        for attribute in occurrences[index].keys():
            class_information = calculate_class_information(data, class_information, attribute, index)
        information.append(class_information)
    return information


def get_split_information(probabilities: list[list[float]]) -> list[float]:
    """
    Returns the split information - entropy of each attribute (cuts off the decision attribute)
    input:
        probabilities = [[0.3, 0.4, 0.3], [0.4, 0.6], [0.6, 0.4], [0.5, 0.5]]
    output:
        split_information = [1.570..., 0.970..., 0.970...]
    """
    print('probabilities = ', probabilities)
    split_information = []
    for index in range(len(probabilities) - 1):
        split_information.append(get_entropy(probabilities[index]))
    print('split_information = ', split_information)
    return split_information


def get_gain(information: list[float], entropy: float) -> list[float]:
    """
    Returns the information gain
    input:
        information = [0.4, 0.875..., 1.0]
        entropy = 1.0
    output:
        gain = [0.6, 0.124..., 0.0]
    """
    return [(entropy - value) for value in information]


def get_gain_ratio(gain: list[float], split_info: list[float]) -> list[float]:
    """
    Returns the gain ratio
    input:
        gain = [0.6, 0.124..., 0.0]
        split_info = [1.570..., 0.970..., 0.970...]
    output:
        gain_ratio = [0.381..., 0.128..., 0.0]
    """
    gain_ratio = []
    for attribute in range(len(gain)):
        if split_info[attribute] > 0:
            gain_ratio.append(gain[attribute] / split_info[attribute])
        else:
            gain_ratio.append(0)
    return gain_ratio


def decision_tree(data, prev=-1):
    values = get_values(data)
    occurrences = get_occurrences(data)
    probabilities = get_probabilities(occurrences)

    entropy = get_entropy(probabilities[-1])
    information = get_information(data, occurrences)
    # print(f'information = {information}')
    gain = get_gain(information, entropy)
    # print(f'gain = {gain}')

    split_information = get_split_information(probabilities)
    # print(f'split_info = {split_information}')

    gain_ratio = get_gain_ratio(gain, split_information)
    # print(f'gain_ratio = {gain_ratio}')

    best_attribute = gain_ratio.index(max(gain_ratio))
