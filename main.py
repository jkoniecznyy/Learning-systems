from src.decision_tree import decision_tree
from src.DecisionTree import Tree
from src.utils import *

if __name__ == '__main__':
    data = read_file('data/gielda.txt')
    # data = read_file('data/test2.txt')
    # data = read_file('data/breast-cancer.data')
    # print(f'data = {data}')
    decision_tree(data)
    # tree = Tree(data)
    # tree.build_tree()
