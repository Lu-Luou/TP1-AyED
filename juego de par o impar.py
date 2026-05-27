import random
saldo=10000
racha=0
continua="S"
while(continua=="S"):
    print("Usted tiene",saldo,"créditos disponibles para jugar")
    apuesta=int(input("¿Cuantos créditos desea apostar en la siguiente jugada?"))
    if(apuesta>saldo or 0>=apuesta):
        while(apuesta>=saldo or 0>=apuesta):
            apuesta=int(input("Ingrese una apuesta menor o igual a su saldo,mayor a 0"))
    num1=random.randint(1,6)
    num2=random.randint(1,6)
    secreto=num1+num2
    eleccion=input("¿La suma es Par o Impar?")
    while(eleccion!= "Par" and eleccion!= "Impar"):
        eleccion=input("Ingrese una ópcion valida entre Par o Impar")
    if((eleccion=="Par" and secreto % 2 == 0)):
        print("Adivinaste!!!Tu apuesta de",apuesta,"créditos se ha duplicado!!! ")
        saldo=saldo+apuesta
        racha=racha+1
        print("Tu saldo actual es de",saldo,"créditos y tu racha es de",racha,)
    else:
         if((eleccion=="Impar" and secreto % 2 == 1)):
            print("Adivinaste!!!Tu apuesta de",apuesta,"creditos se ha duplicado!!! ")
            saldo=saldo+apuesta
            racha=racha+1
            print("Tu saldo actual es de",saldo,"créditos y tu racha es de ",racha,)
         else:
            print("No,fallaste")
            saldo=saldo-apuesta
            racha=0
            print("Tu saldo actual es de",saldo,"créditos")
    continua=input("¿Desea volver a jugar?Ingrese S para si o N para no")
    while(continua!="S" and continua!="N"):
        continua=input("Ingrese una opción valida")