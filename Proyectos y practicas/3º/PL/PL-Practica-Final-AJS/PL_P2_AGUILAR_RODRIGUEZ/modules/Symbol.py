import pprint 

pp = pprint.PrettyPrinter(indent=4, depth=None)
class PrimitiveTypes:
    compatible_types = {"int", "float", "character", "NUMBER_VALUE"}
    # high index means more restrictive
    restrictiveness = ["NUMBER_VALUE","float", "character", "int",  "boolean"]
    
    @classmethod
    def is_compatible(cls, type1: str, type2: str) -> bool:
        if type1 == type2:
            return True
        if type1 is None or type2 is None:
            return True
        return type1 in cls.compatible_types and type2 in cls.compatible_types
    
    @classmethod
    def get_less_restrictive(cls, type1: str, type2: str) -> str:
        return cls.restrictiveness[max(cls.restrictiveness.index(type1), cls.restrictiveness.index(type2))]


class Symbol:
    def __init__(self, name: str, type: str, value: any = None) -> None:
        self.name = name
        self.type = type
        self.value = value


    def update(self, new_symbol) -> None:
        self.name = new_symbol.name
        self.type = new_symbol.type
        self.value = new_symbol.value
        
    
    def __repr__(self) -> str:
        value_str = self.value if self.value is not None else "Unkown"
        return f"Symbol(name={self.name!r}, type={self.type!r}, value={value_str!r})"
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Symbol):
            return False
        return self.name == value.name and PrimitiveTypes.is_compatible(self.type, value.type)
    
    def __ne__(self, value: object) -> bool:
        return not self == value
    
    def __hash__(self) -> int:
        return hash((self.name, self.type))
    
    def __copy__(self):
        return Symbol(self.name, self.type)
    
    

class Function(Symbol):
    # parameters is a list of dicts with the following keys: name, type
    def __init__(self, name: str, type: str, parameters: list) -> None:
        super().__init__(name, type)
        self.parameters = parameters
        self.scope = dict()
        # for each parameter, add it to the scope
        if parameters is not None:
            for parameter in parameters:
                self.scope[parameter.name] = parameter
    
    def __repr__(self) -> str:
        formated_parameters = ""
        for parameter in self.parameters:
            formated_parameters += f"\t{parameter.name}:{parameter.type},\n"
            
        
        return f"Function(name={self.name!r}, type={self.type!r}, parameters={formated_parameters})"


    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Function):
            return False
        return super().__eq__(value) and self.parameters == value.parameters


class Type(Symbol):
    def __init__(self, name: str, atributes:list) -> None:
        super().__init__(name, name)
        self.atributes = atributes

    def is_compatible(self, obj) -> bool:
        if not isinstance(obj, Type) and not isinstance(obj, Object):
            return False
        for atribute in self.atributes:
            if isinstance(atribute, Type) or isinstance(atribute, Object): # atribute is a type
                # search the atribute in obj.atributes with same name
                for atribute2 in obj.atributes:
                    if atribute.name == atribute2.name:
                        if not atribute.is_compatible(atribute2):
                            return False
                        break
            else: # atribute is a primitive type
                # compare atr to atr unitl find the same name and type
                found = False
                for atribute2 in obj.atributes:
                    if atribute.name == atribute2.name and PrimitiveTypes.is_compatible(atribute.type, atribute2.type):
                        found = True
                        break
                if not found:
                    return False
        return True
            
    def get(self, name: str):
        for atribute in self.atributes:
            if atribute.name == name:
                return atribute
        return None
        
        
    def update(self, new_symbol) -> None:
        super().update(new_symbol)
        self.atributes = new_symbol.atributes
    
    def __repr__(self) -> str:
        # get a dict of name:type for each atribute

        formatted_attributes = pp.pformat({a.name: a.type for a in self.atributes})
        return f"Type(name={self.name!r}, attributes={formatted_attributes}\n)"

    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Type) and not isinstance(value, Object):
            return False
        return self.atributes == value.atributes


class Object(Symbol):
    def __init__(self, name: str, type, atributes) -> None:
        super().__init__(name, type, None)
        self.atributes = atributes
        # atributes es una lista de simbolos
        
    def is_compatible(self, obj) -> bool:
        if not isinstance(obj, Type) and not isinstance(obj, Object):
            return False
        for atribute in self.atributes:
            if isinstance(atribute, Type) or isinstance(atribute, Object): # atribute is a type
                # search the atribute in obj.atributes with same name
                for atribute2 in obj.atributes:
                    if atribute.name == atribute2.name:
                        if not atribute.is_compatible(atribute2):
                            return False
                        break
            else: # atribute is a primitive type
                # compare atr to atr unitl find the same name and type
                found = False
                for atribute2 in obj.atributes:
                    if atribute.name == atribute2.name and PrimitiveTypes.is_compatible(atribute.type, atribute2.type):
                        found = True
                        break
                if not found:
                    return False
        return True
    
    def update(self, new_symbol) -> None:
        super().update(new_symbol)
        self.atributes = new_symbol.atributes
        
    
    def get(self, name: str):
        for atribute in self.atributes:
            if atribute.name == name:
                return atribute
        return None

    
    def __repr__(self) -> str:
        # Use the pp instance to format with depth control
        formatted_attributes = pp.pformat(self.atributes)
        return f"Object(name={self.name!r}, type={self.type!r}, attributes={formatted_attributes})"


    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Object) and not isinstance(value, Type):
            return False
        return self.atributes == value.atributes



        