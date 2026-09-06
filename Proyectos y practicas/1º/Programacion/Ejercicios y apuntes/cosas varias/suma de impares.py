
decision=int(input("si quieres decir el numero ultimo numero a sumar pon 0 si quieres los n primeros numeros pon 1"))
if decision==0:
    ult_impar=int(input("hasta que impar quieres sumar"))
    n=(ult_impar+1)/2
else:
       n=int(input("")) 
       
       
suma=int(n**2)

print(suma)