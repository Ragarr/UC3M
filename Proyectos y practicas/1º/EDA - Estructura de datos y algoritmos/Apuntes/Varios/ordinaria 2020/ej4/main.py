def are_adjacent(w:str,c1:str,c2:str):
    if w and len(w)==2 and w[0]==c1 and w[1]==c2:
        return True
    elif not w or len(w)<=2:
        return False
    else:
        return are_adjacent(w[:len(w)//2],c1,c2) or  are_adjacent(w[len(w)//2:],c1,c2) or\
               are_adjacent(w[:len(w)//2:-1],c2,c1) or  are_adjacent(w[len(w)//2::-1],c2,c1)
