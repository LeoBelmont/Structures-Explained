from anastruct import SystemElements

from StructuresExplained.solutions.structure.manager.manager import Manager


def test_struct():
    ss = SystemElements()
    ss.add_element([[0, 0], [1, 0]])
    ss.add_element([[1, 0], [1, 1]])
    ss.add_element([[1, 0], [2, 0]])
    ss.add_element([[2, 0], [3, 0]])
    ss.add_element([[3, 0], [4, 1]])
    ss.add_element([[4, 1], [5, 1]])
    ss.point_load(2, Fy=10)
    ss.point_load(3, Fy=-20, Fx=5)
    ss.point_load(4, Fy=-30)
    ss.point_load(5, Fx=-40)
    ss.moment_load(2, Ty=-9)
    ss.moment_load(1, 7)
    ss.moment_load(3, 3)
    ss.q_load(element_id=3, q=(-10, -20))
    ss.q_load(element_id=5, q=(-10, -20))
    ss.add_support_roll(4)
    ss.add_support_hinged(5)
    # ss.add_support_fixed(3)

    mn = Manager(ss)
    mn.generate_pdf(pdf_path=r"C:\testfolder")


if __name__ == "__main__":
    test_struct()
