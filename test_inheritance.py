class SuperFMECAType():
    
    def __init__(self, ident):
        self.ident = ident
    
    def export_data(self):
        data = {}
        for a in self.__dict__:
            if type(self.__dict__[a]) == type({}):
                data[a] = {k: v for k, v in
                    [(b, self.__dict__[a][b].export_data()) for b in 
                          self.__dict__[a].keys()]}
            else:
                data[a] = self.__dict__[a]
        return data
    
    def import_data(self, data):
        for a in data:
            if type(data[a]) == type({}):
                c = _format_class_name(a)
                for l in data[a].keys():
                    o = eval(c)(l)
                    o.import_data(data[a][l])
                    getattr(self, a)[l] = o
            else:
                setattr(self, a, data[a])
    
    def _format_class_name(self, s):
        s = s.replace('_', ' ').title().replace(' ', '')
        if s[-3:] == 'ies':
            s = s[:-4] + 'y'
        else:
            s = s[:-1]
        return s
        
class Component(SuperFMECAType):
    
    def __init__(self, ident):
        super(type(self), self).__init__(ident)
        self.subcomponents = {}
        
class Subcomponent(SuperFMECAType):
    
    def __init__(self, ident):
        super(type(self), self).__init__(ident)

if __name__ == '__main__':
    
    d = {'ident': 'component_1',
         'subcomponents': {
                 'subcomponent_a': {'ident': 'subcomponent_a'},
                 'subcomponent_b': {'ident': 'subcomponent_b'},
                 'subcomponent_c': {'ident': 'subcomponent_c'}
                 }
         }
       
    c = Component('component_a')    
    print(c.ident)
    
    c.import_data(d)    
    print(c.ident)
    print(c.export_data())
    