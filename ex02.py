from pbc import PBC, protectmethod


class ProtectedExample(PBC):

    @protectmethod
    def setvalue(self, value): 
        self.value = value


class Inherit(ProtectedExample):
    pass

# fix so that this does not work!
Inherit.setvalue = 10


a = Inherit()
