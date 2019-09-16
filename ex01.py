from pbc import PBC, protectmethod


class ProtectedExample(PBC):

    @protectmethod
    def __init__(self, value): 
        self.value = value


class Inherit(ProtectedExample):

    def __init__(self, txt):
        print(txt)
