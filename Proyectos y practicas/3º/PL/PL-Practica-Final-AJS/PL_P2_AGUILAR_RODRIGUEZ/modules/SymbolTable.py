from .Symbol import *
import pprint 

pp = pprint.PrettyPrinter(indent=4, depth=2)


class SymbolTable:
    """Symbol table for the parser"""
    def __init__(self) -> None:
        self.__scopes_stack = list() # stack of scopes
        self.scopes = {"global": dict()} 
        self.scope = "global"

        
    
    def enter_scope(self, scope:str) -> None:
        
        # si el scope es una funcion, entonces se debe crear un nuevo scope con los parametros de la funcion
        # y se debe agregar el scope de la funcion a la pila
        
        prev_scope = self.scope
        symbol = self.get(scope)
        self.__scopes_stack.append(self.scope)
        self.scope = scope
        if scope not in self.scopes:
            self.scopes[scope] = dict()
        
        if isinstance(symbol, Function):
            self.scopes[scope] = self.scopes[prev_scope].copy()
            for param in symbol.parameters:
                self.add(param)
            # copiar el scope actual al scope de la funcion
        if scope == "ufc_scope":
            # copy the current scope to the ufc_scope
            self.scopes[scope] = self.scopes[prev_scope].copy()
        
            
        
    def exit_scope(self) -> None:
        self.scope = self.__scopes_stack.pop()
    
    def remove_scope(self, scope:str) -> None:
        if scope in self.scopes:
            del self.scopes[scope]
    
    def enter_fc_scope(self) -> None:
        self.remove_scope("ufc_scope")
        self.enter_scope("ufc_scope")
            
           
    def merge_fc_scope(self) -> None:
        # update the previous scope with the fc_scope
        self.exit_scope()
        for symbol in self.scopes["ufc_scope"]:
            self.scopes[self.scope][symbol] = self.scopes["ufc_scope"][symbol]
        self.remove_scope("ufc_scope")
    
    def discard_fc_scope(self) -> None:
        self.exit_scope()
        self.remove_scope("ufc_scope")
    
    def merge_fc_scope_as_unknwon(self) -> None:
        # update the previous scope with the fc_scope
        self.exit_scope()
        # cada simbolo que tenga tipo distinto se establece tipe = None, value = None
        for symbol in self.scopes["ufc_scope"]:
            if self.scopes[self.scope][symbol].type != self.scopes["ufc_scope"][symbol].type:
                self.scopes[self.scope][symbol].type = None
                self.scopes[self.scope][symbol].value = None
        # cada simbolo que conserve su tipo y cxambie su valor se establece value = None
        for symbol in self.scopes["ufc_scope"]:
            if self.scopes[self.scope][symbol].type == self.scopes["ufc_scope"][symbol].type:
                self.scopes[self.scope][symbol].value = None
        self.remove_scope("ufc_scope")
        
        
    def add(self, symbol: Symbol) -> None:
        """
        Adds a symbol to the symbol table.

        Args:
            symbol (Symbol): The symbol to be added.

        Raises:
            ValueError: If the symbol is not an instance of the Symbol class.

        Returns:
            None
        """
        if not isinstance(symbol, Symbol):
            raise ValueError("Invalid symbol")
        self.scopes[self.scope][symbol.name] = symbol
    
    def remove(self, name: str) -> None:
        """
        Removes a symbol from the symbol table.

        Args:
            name (str): The name of the symbol to remove.

        Returns:
            None
        """
        if name in self.scopes[self.scope]:
            del self.scopes[self.scope][name]
        
    def update(self, name: str|list, new_symbol: Symbol) -> None:
        """
        Updates the value of a symbol in the symbol table.

        Args:
            symbol (Symbol): The symbol to update.

        Returns:
            None
        """
        if isinstance(name, str):
            self.scopes[self.scope][name] = new_symbol
        elif isinstance(name, list):
            # recursive call
            item = self.get(name[0])
            if item is None:
                raise ValueError("Symbol not found")
            for ref in name[1:]:
                item = item.get(ref)
                if item is None:
                    raise ValueError("Symbol not found")
            item.update(new_symbol)
            
            
        
    
    def get(self, name) -> Symbol:
            """
            Retrieves the symbol with the given name from the symbol table.

            Args:
                name (str): The name of the symbol to retrieve.

            Returns:
                Symbol: The symbol with the given name, or None if it doesn't exist.
            """
            if isinstance(name, str):
                try:
                    return self.scopes[self.scope].get(name)
                except KeyError:
                    return None
            if isinstance(name, Symbol):
                return self.scopes[self.scope].get(name.name)
            if isinstance(name, list):
                # recursive call
                item = self.get(name[0])
                if item is None:
                    return None
                for ref in name[1:]:
                    if isinstance(item, Symbol):
                        new_item = self.scopes[self.scope].get(item.type)
                        if new_item is not None:
                            item = new_item
                    item = item.get(ref)
                    if item is None:
                        return None
                return item
                
            else:
                raise ValueError("Invalid name")
    
    def __repr__(self) -> str:
        msg = ""
        for scope in self.scopes:
            msg += f"SCOPE: {scope}\n"
            for symbol in self.scopes[scope]:
                msg += f"{repr(self.scopes[scope][symbol])}\n"
            msg += "\n"
        return msg
    
    def __iter__(self):
        return iter(self.scopes[self.scope].values())
    
    def __len__(self) -> int:
        return len(self.scopes[self.scope])
    
    def __contains__(self, name: str) -> bool:
        return name in self.scopes[self.scope]
    
    def __getitem__(self, name: str) -> Symbol:
        return self.scopes[self.scope][name]
    
    def __setitem__(self, name: str, symbol: Symbol) -> None:
        self.scopes[self.scope][name] = symbol
        
    def __delitem__(self, name: str) -> None:
        del self.scopes[self.scope][name]
    
    
    
    
if __name__ == "__main__":
    symbol_table = SymbolTable()
    symbol_table.add(Symbol("x", 10, "int"))
    symbol_table.add(Symbol("y", 123.2, "float"))
    symbol_table.add(Symbol("z", "Hello, World!", "string"))
    print(symbol_table)