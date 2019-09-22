# Trabajo practico 2 - Ejercicio 1
# a) Implement decision tree with Shannon entropy
# b) Add additional training example and reconstruct decision tree

from ml_tps.utils.decision_tree_utils import DecisionTree
import pandas as pd

DEFAULT_FILEPATH = "data/deporte.csv"
DEFAULT_OBJECTIVE = "Disfruta?"

def changesDaniel():
    import os
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin'


def main():
    '''
    ggg = Digraph(comment="Testing out")
    ggg.node('A')
    ggg.node('B')
    ggg.node('C')
    ggg.edge('A', 'B')
    ggg.edge('A', 'C', constraint='false')
    # ggg.render("./out/ASD.gv")
    ggg.view()
    '''
    objective = DEFAULT_OBJECTIVE
    drop_nro_example_column = True
    example_column_title = "Nro.Ejemplo"

    dataset = pd.read_csv(DEFAULT_FILEPATH)
    example = pd.Series([5, "Sol", "Calida", "Normal", "Debil", "Calida", "Estable", 0], index=dataset.columns)
    dataset_with_example = dataset.copy().append(example, ignore_index=True)

    if drop_nro_example_column:
        # Drop nro. example
        del dataset[example_column_title]
        del dataset_with_example[example_column_title]

    decision_tree = DecisionTree(dataset, objective)
    decision_tree.plot()

    # =========== EJ1 b) Add example ==========
    decision_tree_example_added = DecisionTree(dataset_with_example, objective)
    decision_tree_example_added.plot()

    a = 1

if __name__ == '__main__':
    changesDaniel()
    main()