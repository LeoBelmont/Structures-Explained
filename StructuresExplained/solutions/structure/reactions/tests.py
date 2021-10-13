from StructuresExplained.solutions.structure.reactions.assembler import Assembler

if __name__ == "__main__":
    from anastruct import SystemElements
    from sympy import sympify

    ss = SystemElements()
    ss.add_element([[0, 0], [1, 0]])
    ss.add_element([[1, 0], [1, 1]])
    ss.add_element([[1, 0], [2, 0]])
    ss.add_element([[2, 0], [3, 0]])
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
    ss.solve()
    ass = Assembler(ss)
    ass.assemble_structure()
    print(
        f"{sympify(ass.res.point_sum_y, evaluate=False)}\n{sympify(ass.res.point_sum_x, evaluate=False)}\n{ass.res.moments_sum}\n")
