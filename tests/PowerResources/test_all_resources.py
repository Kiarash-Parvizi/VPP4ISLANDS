from .test_DG import test_DG
from .test_ES import test_ES
from .test_PV import test_PV
from .test_WF import test_WF

from .test_FL import test_FL
from .test_FixedLoad import test_FixedLoad
from .test_LoadCollection import test_LoadCollection
from .test_structure import test_structure

def test_all_resources():
    print(f"....TEST test_all_resources is started...")
    test_DG()
    test_ES()
    test_PV()
    test_WF()
    test_FL()
    test_FixedLoad()
    test_LoadCollection()
    test_structure()


if __name__ == "__main__":
    test_all_resources()