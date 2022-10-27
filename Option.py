from typing import *

from base import Listener

class Option(Listener):
    description = ""
    requirements = {}
    
    def __init__(self, encounter, description = None, requirements = None):
        self.encounter = encounter
        self.des = self.description = description or self.description
        self.req = self.requirements = requirements or self.requirements
    
    def select(self) -> List[Tuple[str, str, str, int]]:
        """
        card play effects \n
        return: [("objName", "statName", "op", num)]
        """
        print(f"{repr(self)} selected")
        return []