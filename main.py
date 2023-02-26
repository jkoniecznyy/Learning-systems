from src.decision_tree import decision_tree
from src.DecisionTree import Tree
from src.utils import *

if __name__ == '__main__':
    data = read_file('data/gielda.txt')
    # occurrences = read_file('occurrences/test2.txt')
    # occurrences = read_file('occurrences/breast-cancer.occurrences')
    # print(f'occurrences = {occurrences}')
    decision_tree(data)
    # tree = Tree(occurrences)
    # tree.build_tree()
