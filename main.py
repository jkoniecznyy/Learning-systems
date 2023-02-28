import csv

from src.decision_tree import build_decision_tree


def read_file(path: str):
    with open(path) as input:
        return [row for row in csv.reader(input, delimiter=",")]


if __name__ == '__main__':
    # data = read_file('data/breast-cancer.data')
    # data = read_file('data/car.data')
    data = read_file('data/gielda.txt')
    # data = read_file('data/testowaTabDec.txt')

    build_decision_tree(data)
