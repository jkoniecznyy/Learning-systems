from math import log2
from collections import Counter

MARGIN = '\t'


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


def calculate_class_information(data: list[list[str]], attribute: str, index: int) -> float:
    """
    Returns the class information for a given attribute
    input:
        data = [['old', 'yes', 'swr', 'down'], ...]
        attribute = old
        index = 0
    output:
        0.0
    """
    class_values = [row for row in data if row[index] == attribute]
    occurrences = get_occurrences(class_values)
    class_probabilities = get_probabilities(occurrences)
    entropy = get_entropy(class_probabilities[-1])
    return len(class_values) / len(data) * entropy


def get_information(data: list[list[str]], occurrences: list[dict[str, int]]) -> list[float]:
    """
    Returns the information for every attribute
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
            class_information += calculate_class_information(data, attribute, index)
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
    split_information = []
    for index in range(len(probabilities) - 1):
        split_information.append(get_entropy(probabilities[index]))
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


def organize_data_by_attribute(data: list[list[str]], occurrences: list[dict[str, int]],
                               parent_attribute: int) -> list[list[list[str]]]:
    """
    Organizes the data into a list of lists, where each list contains the data for a specific attribute
    input:
        data = [['old', 'yes', 'swr', 'down'], ['old', 'no', 'swr', 'down'], ['mid', 'yes', 'swr', 'down']]
        occurrences = [{'old': 2, 'mid': 1}, {'yes': 2, 'no': 1}, {'swr': 3}, {'down': 3}]
        parent_attribute = 0 (old/mid)
    output:
        new_data = [[['old', 'yes', 'swr', 'down'], ['old', 'no', 'swr', 'down']], [['mid', 'yes', 'swr', 'down']]]
    """
    organized_data = []
    for attribute in occurrences[parent_attribute]:
        organized_data.append(
            [d for d in data if d[parent_attribute] == attribute]
        )
    return organized_data


def print_node(occurrences, parent_attribute: int, child_attribute: int, level: int) -> None:
    """ Prints the node of the decision tree """
    if parent_attribute < 0:
        print(f'{MARGIN * level} '
              f'Atrybut: {child_attribute + 1}')
    else:
        print(f'{MARGIN * level} '
              f'{list(occurrences[parent_attribute].keys())[0]} '
              f'-> Atrybut: {child_attribute + 1}')


def print_leaf(data: list[list[str]], occurrences:  list[dict[str, int]],
               parent_attribute: int, level: int) -> None:
    """ Prints the leaf of the decision tree """
    print(
        f'{MARGIN * level} '
        f'{list(occurrences[parent_attribute].keys())[0]} -> D: '
        f'{list(occurrences[len(data[0]) - 1].keys())[0]}'
    )


def build_decision_tree(data: list[list[str]], parent_attribute: int = -1, level: int = 0) -> None:
    """
    Builds the decision tree
    """
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
    child_attribute = gain_ratio.index(max(gain_ratio))

    if max(gain_ratio) > 0:
        print_node(occurrences, parent_attribute, child_attribute, level)
        level += 1
        parent_attribute = child_attribute
        organized_data = organize_data_by_attribute(data, occurrences, parent_attribute)

        for data_part in organized_data:
            build_decision_tree(data_part, parent_attribute, level)
    else:
        print_leaf(data, occurrences, parent_attribute, level)
