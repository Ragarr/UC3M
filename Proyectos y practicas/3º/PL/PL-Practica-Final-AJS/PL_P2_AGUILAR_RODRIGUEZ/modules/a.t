Type() =
{
    name = "a",
    atributes = [
        Symbol(name = "attr1", type = "int"),
        Symbol(name = "attr2", type = "char"),
        Type(name = "Persona", atributes = [
            Symbol(name = "nombre", type = "char"),
            Symbol(name = "edad", type = "int")
        ])
    ]
}