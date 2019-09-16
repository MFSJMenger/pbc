""" Protected Base Classes (PBCs) 

inspired from Abstract Base Classes (ABCs) classes according to PEP 3119,
PBCs represent an way to protect classmethods from being overwritten.

Only way is still: 
cls.__dict__['func'] = ...

every other method does not work!

This redefines the 'setattr' function, so do not use it if you use many 
setattr calls!

"""
from functools import wraps


__all__ = ['protectmethod', 'PBC']


class ProtectedFunction(Exception):
    
    def __init__(self, func):

        text = f"Cannot overwrite member-function '{func}' as it is protected!"
        
        Exception.__init__(self, text)


def _pbc_protect_setter(funcobj):

    @wraps(funcobj)    
    def _setter(self, name, value):
        protected = getattr(self, '_pbc__protected_functions__', None) 
        if protected is not None:
            if name in protected:
                raise ProtectedFunction(name)
        return funcobj(name, value)
    return _setter


class PBCMeta(type):
    """Metaclass for defining Protected Base Classes (PBCs).
    Use this metaclass to create an PBC.  An PBC can be subclassed
    directly, and then acts as a mix-in class. 
    """

    def __new__(self, name, bases, ns, *args, **kwargs):

        ns['_pbc__protected_functions__'] = []

        for base in bases:
            protected = getattr(base, '_pbc__protected_functions__', None) 
            if protected is not None:
                ns['_pbc__protected_functions__'] += protected
        
        if '__setattr__' in ns:
            ns['__setattr__'] = _pbc_protect_setter(ns['__setattr__'])
        else:
            @_pbc_protect_setter
            def setattribute(self, name, value):
                setattr(self, name, value)
            ns['__setattr__'] = setattribute

        for name, obj in ns.items():
            if name in ns['_pbc__protected_functions__']:
                raise ProtectedFunction(name)

            if callable(obj):
                if getattr(obj, '_pbc__isprotected__', False) is True:
                    ns['_pbc__protected_functions__'].append(name)

        return type.__new__(self, name, bases, ns, *args, **kwargs)

class PBC(metaclass=PBCMeta):
    """Helper class that provides a standard way to create an PBC using
    inheritance.
    """
    __slots__ = ()


def protectmethod(func):
    """A decorator indicating protected methods.
    Requires that the metaclass is PBCMeta or derived from it. A
    class that has a metaclass derived from PBCMeta cannot be
    overwritten by any class that inherits from the class.
    The protected methods can be called using any of the normal
    'super' call mechanisms.
    Usage:
        class C(metaclass=PBCMeta):
            @protectmethod
            def my_proteced_method(self, ...):
                ...
    """
    func._pbc__isprotected__ = True
    return func
