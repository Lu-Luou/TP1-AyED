import random
numero_mostrado = random.randint(1, 1000)
siguiente_numero = random.randint(1, 1000)
while(numero_mostrado == siguiente_numero):
    siguiente_numero = random.randint(1, 1000)
flag = 1
cuenta = 0
while(flag == 1): 
    print(numero_mostrado)
    numero_ingresado = input("Ingrese Mayor o Menor: ")
    while(numero_ingresado!="Mayor" and numero_ingresado!="Menor" and ...):
        print("Debe ingresar alguna opción valida")
        numero_ingresado = input("Ingrese Mayor o Menor: ")
    if(numero_ingresado == "Mayor" or numero_ingresado == "MAYOR" or numero_ingresado == "mayor"):
         if(siguiente_numero>numero_mostrado):
             cuenta = cuenta+1
             numero_mostrado = siguiente_numero
             siguiente_numero = random.randint(1,1000)
             while(siguiente_numero==numero_mostrado):
                 siguiente_numero=random.randint(1,1000)
         else:
             flag=0
    else:
         if(numero_ingresado == "Menor" or numero_ingresado=="MENOR" or numero_ingresado=="menor"):
             if(siguiente_numero<numero_mostrado):
                 cuenta = cuenta+1
                 numero_mostrado=siguiente_numero
                 siguiente_numero=random.randint(1,1000)
                 while(siguiente_numero==numero_mostrado):
                     siguiente_numero=random.randint(1,1000)
         else:
             flag=0
print("Oh no,perdiste")
print("Tuviste una racha de",cuenta)




