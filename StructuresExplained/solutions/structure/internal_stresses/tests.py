from anastruct import SystemElements
from sympy import sympify

from StructuresExplained.solutions.structure.internal_stresses.assembler import Assembler, Setting


def test_struct1():
    ss = SystemElements()
    ss.add_element([[-2, 2], [-1, 0]])
    ss.add_element([[-2, 3], [-2, 2]])
    ss.add_element([[-1, 4], [-2, 3]])
    # ss.add_element([[-1, 4], [0, 5]])
    # ss.add_element([[0, 5], [1, 5]])
    # ss.add_element([[1, 5], [2, 5]])
    # ss.add_element([[2, 5], [3, 5]])
    # ss.add_element([[3, 5], [5, 2]])
    ss.add_element([[-3, 4], [-2, 3]])
    ss.add_element([[-4, 4], [-3, 4]])
    ss.add_element([[-3, 5], [-3, 4]])
    ss.add_element([[-2, 0], [-1, 0]])
    ss.add_element([[-2, 1], [-2, 0]])
    ss.add_element([[-2, -1], [-2, 0]])
    ss.add_element([[-3, 0], [-2, 0]])
    ss.add_element([[-4, 1], [-3, 0]])
    ss.add_element([[-5, 2], [-4, 1]])
    ss.add_element([[-4, -1], [-3, 0]])
    ss.add_element([[-5, -2], [-4, -1]])
    ss.add_element([[-1, 0], [0, 0]])
    ss.add_element([[0, 0], [1, 0]])
    ss.add_element([[2, 0], [3, 0]])
    ss.add_element([[1, 0], [2, 0]])
    ss.add_element([[2, 0], [3, 1]])
    ss.point_load(10, 5)
    ss.moment_load(1, 15)
    # ss.add_element([[3, 1], [4, 1]])
    # ss.add_element([[3, 1], [3, 2]])
    # ss.add_element([[4, 1], [5, 2]])
    # ss.add_element([[4, 1], [6, 2]])
    ss.add_element([[1, 0], [-1, 1]])
    ss.show_structure()
    ass = Assembler(ss)
    ass.assemble_structure(main_path=(15, 20))
    # ass.assemble_structure(main_path=(7, 13))
    # ass.plot_solve_order(ass.plot_order, show=True, save_figure=False, plotting_start_node=15)
    [[print(f"section {index + 1}-{sub_index + 1}: {sympify(sub_string, evaluate=False)}") for sub_index, sub_string in
      enumerate(string)] for index, string in enumerate(ass.sections_strings)]


def test_struct2():
    ss = SystemElements()
    ss.add_element([[0, 0], [1, 0]])
    ss.add_element([[1, 0], [1, 1]])
    ss.add_element([[1, 0], [2, 0]])
    ss.add_element([[2, 0], [3, 0]])
    ss.add_element([[3, 0], [4, 1]])
    ss.add_element([[4, 1], [5, 1]])
    ss.point_load(2, Fy=10)
    ss.point_load(3, Fy=-20)
    ss.point_load(4, Fy=-30)
    ss.point_load(5, Fx=-40)
    ss.moment_load(2, Ty=-9)
    ss.moment_load(1, 7)
    ss.moment_load(3, 3)
    ss.q_load(element_id=3, q=(-10, -20))
    ss.add_support_roll(4)
    ss.add_support_hinged(5)
    # ss.show_structure()
    ss.solve()
    ss.show_reaction_force(show=False)
    ass = Assembler(ss)
    ass.assemble_structure(main_path=Setting.longest)
    [print(element.id, values) for element, values in ass.internal_stresses_dict.items()]


if __name__ == "__main__":
    test_struct2()
