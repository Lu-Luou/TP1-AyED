import random
nombre = input("ingrese su nombre: ")
numero_mostrado = random.randint(1, 1000)
siguiente_numero = random.randint(1, 1000)
while(numero_mostrado == siguiente_numero):
    siguiente_numero = random.randint(1, 1000)
jugando = True
cuenta = 0
while(jugando): 
    print("el numero actual es:", numero_mostrado)
    numero_ingresado = input("Ingrese Mayor o Menor: ").lower()
    while numero_ingresado != "mayor" and numero_ingresado != "menor":
        print("Debe ingresar alguna opción valida")
        numero_ingresado = input("Ingrese Mayor o Menor: ").lower()
         
        if(numero_ingresado == "mayor"):
            if siguiente_numero > numero_mostrado:
             cuenta = cuenta+1
             numero_mostrado = siguiente_numero
             siguiente_numero = random.randint(1,1000)
             while(siguiente_numero==numero_mostrado):
                 siguiente_numero=random.randint(1,1000)
         else:
             jugando = False
    else:
             if(siguiente_numero<numero_mostrado):
                 cuenta = cuenta+1
                 numero_mostrado=siguiente_numero
                 siguiente_numero=random.randint(1,1000)
                 while(siguiente_numero==numero_mostrado):
                     siguiente_numero=random.randint(1,1000)
         else:
             jugando = False
print("Oh no,", nombre + ", perdiste")
print("Tuviste una racha de",cuenta)




