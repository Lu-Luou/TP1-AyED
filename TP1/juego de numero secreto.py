import random
numero_secreto=random.randint(1,100)
intentos=6
ganador=0
jugador=input("Indique nombre del jugador")
while(intentos>0 and ganador==0):
     print("Usted tiene",intentos,"intentos")
     valido=False
     while(valido==False):
         numero=input("Ingrese un número entre 1 y 100")
         try:
             numero = int(numero)
             if(numero >=1 and numero <=100):
                 valido = True

             else:
                 print("Ingrese un número válido entre 1 y 100")
            
         except:
             print("Debe ingresar un número")
     if(numero==numero_secreto):
         ganador=1

     else:

         if(numero>numero_secreto):
             print("El número secreto es menor")
             intentos=intentos-1

         else:
             print("El número secreto es mayor")
             intentos=intentos-1
     if(ganador==1):
         print(jugador,"¡¡Enhorabuena,ganaste!!")

     else:
         if(intentos==0):
             print("Oh no,perdiste el juego")
             print("El número secreto era", numero_secreto)