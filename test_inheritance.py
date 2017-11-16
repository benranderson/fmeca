class SuperFMECAType():
    
    def __init__(self, ident):
        self.ident = ident
    
    def export_data(self):
        data = {}
        for a in self.__dict__:
            if type(self.__dict__[a]) == type([]):
                data[a] = { k: v for k, v in 
                    [(b.ident, b.export_data()) for b in self.__dict__[a]]}
            else:
                data[a] = self.__dict__[a]
        return data
        
        
class Component(SuperFMECAType):
    
    def __init__(self, ident):
        super(type(self), self).__init__(ident)
        self.facilities = [Subcomponent('subcomponent_a'),
                           Subcomponent('subcomponent_b'),
                           Subcomponent('subcomponent_c')]
        
class Subcomponent(SuperFMECAType):
    
    def __init__(self, ident):
        super(type(self), self).__init__(ident)

if __name__ == '__main__':
    c = Component('component_1')
    print(c.export_data())