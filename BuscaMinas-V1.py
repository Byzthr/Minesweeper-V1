# -*- coding: utf-8 -*-

import numpy as np
# import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
# import time
import sys

# Funciones del juego----------------------------------------------------------


def Gamei(sizey, sizex, Nb, x0, y0):
    M  = np.zeros((sizey,sizex), dtype=int)
    Mn = np.zeros((sizey, sizex),dtype=int)
    Mt = np.zeros((sizey,sizex), dtype = bool)
    Mm = np.zeros((sizey,sizex), dtype = bool)
    Ms = 9*np.ones((sizey, sizex), dtype = int)

    # Generación de M
    coordbx = np.random.randint(0, sizex-1, Nb)
    coordby = np.random.randint(0, sizey-1, Nb)
    for cor in zip(coordby,coordbx):
        M[cor] = 10

    if x0==0 and y0==0:
        M[y0:y0+1,x0:x0+1] = 0

    elif x0==0:
        M[y0-1:y0+2,x0:x0+2] = 0

    elif y0==0:
        M[y0:y0+1,x0-1:x0+1] = 0

    elif x0>0 and y0>0:
        M[y0-1:y0+2,x0-1:x0+2] = 0

    else:
        print("Algo raro en Gamei()")

    # Generación de Mn
    for i in range(sizey):
        for j in range(sizex):
            if i==0 and j==0:
                n = len(np.where(M[i:i+2,j:j+2] == 10)[0])

            elif i==0:
                n = len(np.where(M[i:i+2,j-1:j+2] == 10)[0])

            elif j==0:
                n = len(np.where(M[i-1:i+2,j:j+2] == 10)[0])

            else:
                n = len(np.where(M[i-1:i+2,j-1:j+2] == 10)[0])
            Mn[i,j] = int(n)

    coordspost = np.where(M==10)
    for cor in zip(coordspost[0],coordspost[1]):
        Mn[cor] = M[cor]

    # print(M)
    # print(Mn)
    # print(Ms)
    return M, Mn, Mt, Mm, Ms


def Fallo(M, Mt, Mm, Ms, x, y):
    print("Peldiste mi rey")
    # coords = np.where(M == 10)
    # for i,j in zip(coords[0],coords[1]):
    #     Ms[i,j] = Mn[i,j]
    # coordsfm = np.where((Mn==True) & (M!=10))
    # for i,j in zip(coordsfm[0],coordsfm[1]):
    #     Ms[i,j] = Mn[i,j]
    Ms[:,:] = Mn[:,:]

    return Ms


def Agua(Mn, Mt, Ms,x, y):
    Mt[y,x] = True
    if Mn[y,x]==0:
        if x==0 and y==0:
            Mt[y:y+1,x:x+1] = True

        elif x==0:
            Mt[y-1:y+2,x:x+2] = True

        elif y==0:
            Mt[y:y+1,x-1:x+1] = True

        elif x>0 and y>0:
            Mt[y-1:y+2,x-1:x+2] = True

        else:
            print("Algo raro en Agua()")

        #Mostrar áreas blancas
        for it in range(size):
            for i in range(sizey):
                for j in range(sizex):
                    if Mn[i,j] == 0:
                        if i==0 and j==0:
                            n = len(np.where((Mt[i:i+2,j:j+2] == True) & (Mn[i:i+2,j:j+2] == 0))[0])

                        elif i==0:
                            n = len(np.where((Mt[i:i+2,j-1:j+2] == True) & (Mn[i:i+2,j-1:j+2] == 0))[0])

                        elif j==0:
                            n = len(np.where((Mt[i-1:i+2,j:j+2] == True) & (Mn[i-1:i+2,j:j+2] == 0))[0])

                        else:
                            n = len(np.where((Mt[i-1:i+2,j-1:j+2] == True) & (Mn[i-1:i+2,j-1:j+2] == 0))[0])
                        
                        if n!=0:
                            Mt[i,j] = True
                            if i==0 and j==0:
                                Mt[i:i+2,j:j+1] = True
                            elif j==0:
                                Mt[i-1:i+2,j:j+2] = True
                            elif i==0:
                                Mt[i:i+2,j-1:j+2] = True
                            elif i>0 and j>0:
                                Mt[i-1:i+2,j-1:j+2] = True
                            else:
                                print("Algo raro en Agua()")
    #Actualización de Ms
    coordst = np.where(Mt == True)
    for i,j in zip(coordst[0],coordst[1]):
        Ms[i,j] = Mn[i,j]
    return Mt, Ms


def Marca(M, Mt, Mm, Ms, sizey, sizex, rmarks, marks):

    reinput = input("Tag bomb \nA: ")

    if reinput=="" or reinput=="m" or reinput=="M":
        return Mm, Ms, rmarks, marks, True

    while True:
        try:
            y = int(reinput)
            if y<0 or y>sizey-1:
                print("Fuera de límites \n")

            x = int(input("B: "))
            if x<0 or x>sizex-1:
                print("Fuera de límites \n")

            break

        except:
            print("Introduce un número o 'enter' o 'm' para salir del modo marca")

    if Mm[y,x]==False and Mt[y,x]==False:
        Mm[y,x] = True
        Ms[y,x] = 10
        marks += 1
        if M[y,x]==10:
            rmarks += 1

    elif Mm[y,x]==True and Mt[y,x]==False:
        Mm[y,x] = False
        Ms[y,x] = 9
        marks -= 1
        if M[y,x]==10:
            rmarks -= 1

    else:
        print("Ya le diste a ese \n")

    return Mm, Ms, rmarks, marks, reinput

# Mapa de color customizado----------------------------------------------------

blanc = (1,1,1,0)
bomb1 = (150/255,251/255,1,1)
bomb2 = (131/255, 106/255, 255/255,1)
bomb3 = (108/255, 255/255, 170/255,1)
bomb4 = (154/255, 255/255, 108/255,1)
bomb5 = (238/255, 255/255, 106/255,1)
bomb6 = (255/255, 202/255, 106/255,1)
bomb7 = (1,0,0,1)
bomb8 = (.5,0,0,1)
ocult = (.85,.85,.85,1)
bombs = (0,0,0,1)

colorlist=[blanc, bomb1, bomb2, bomb3, bomb4, bomb5, bomb6, bomb7, bomb8, ocult, bombs]
cmap = clrs.LinearSegmentedColormap.from_list('Customizado', colorlist, 11)


# Ejecución del juego----------------------------------------------------------

print("Bienvenido al BuscaMinas casero de Byzthr V0.1. \nSi no conoces las reglas del juego búscalas en Google. \nEntra al menú de pausa pulsando intro")

dificultad=0

print("Nivel de dificultad")
while True:
    try:
        dificultad = int(input("[1-5]: "))
        if dificultad<1 or dificultad>5:
            print("Entre 1 y 5")
        else:
            break
    except:
        print("Introduce un número entre 1 y 5")

size = dificultad*6
sizex = int(np.sqrt(dificultad)*7)
sizey = int(np.sqrt(dificultad)*5)
figsizex = dificultad+6
figsizey = dificultad+2
Nb = int(sizex*sizey*15/100)

      
#Motor gráfico----------------------------------------------------------------

Ms0 = 9 * np.ones((sizey, sizex))
antialiaisin = .3

fig = plt.figure(figsize = (figsizex,figsizey))
plt.ion()
mapa = plt.imshow(Ms0, cmap= cmap, vmin = 0, vmax = 11)

plt.title("Moves = 0")
plt.xlabel("B")
plt.ylabel("A")

ax = plt.gca()
ax.set_xticks(np.arange(0, sizex, 1))
ax.set_yticks(np.arange(0, sizey, 1))
ax.set_xticklabels(np.arange(0, sizex, 1))
ax.set_yticklabels(np.arange(0, sizey, 1))
ax.set_xticks(np.arange(.5, sizex, 1), minor = True)
ax.set_yticks(np.arange(.5, sizey, 1), minor = True)
plt.grid(which = 'minor', linewidth = 1.5)

cbar = plt.colorbar()
cbar.set_ticks(np.arange(.5,11.5,1))
cbar.set_ticklabels(["0", "1", "2", "3", "4", "5", "6", "7", "8", "?", "Bombs"])
plt.show()
plt.pause(antialiaisin)

#Primer movimiento------------------------------------------------------------

print("Movimiento 1---------------------")
initio = False
jugando = False
movs = 0
errors  = 0
maxerrors = 15
while initio!=True:
    X = input("A: ")
    if X == "":
        X = "Pausa"
        while X != "":
            X = input("Menú \nVolver al juego: enter \nSalir: q \n")
            if X == "q" or X == "Q":
                sys.exit("Has decidido terminar el juego")
    else:
        while True:
            try:
                y0 = int(X)
                while y0 < 0 or y0 > sizey-1:
                    print("Fuera de límites")
                    y0 = int(input("A: "))
                x0 = int(input("B: "))
                while x0 < 0 or x0 > sizex-1:
                    print("Fuera de límites")
                    x0 = int(input("B: "))
                else:
                    errors = 0
                    break
            except:
                errors += 1
                if errors == maxerrors:
                    sys.exit("Too many incorrect inputs")
                print("Un número o 'enter' para el menú")
                X = input("A: ")

        M, Mn, Mt, Mm, Ms = Gamei(sizey, sizex, Nb, x0, y0)
        Mt, Ms = Agua(Mn, Mt, Ms, x0, y0)
        movs += 1
        plt.title("Moves = " + str(movs))
        plt.suptitle(str(Nb) + " bombs")
        mapa.set_data(Ms)
        plt.pause(3*antialiaisin)
        print("Movimiento 2---------------------")
        jugando = True
        initio = True

movs    = 1
tags   = 0
rtags = 0

while jugando == True:
    
    X = input("A: ")
    if X == "":
        X = "no"
        while X!="":
            X = input("Menú \nVolver al juego: enter \nMarcar bomba: M \nSalir: q \n")

            if X == "m" or X == "M":
                salir_modo_marca = False
                while salir_modo_marca != True:
                    Mm, Ms, rtags, tags, salir_modo_marca = Marca(M, Mt, Mm, Ms, sizey, sizex, rtags, tags)
                    mapa.set_data(Ms)
                    plt.suptitle(str(Nb-tags) + " bombs")
                    plt.pause(antialiaisin)

            elif X == "q" or  X=="Q":
                sys.exit("Has decidido terminar el juego")

            else:
                pass

    elif X == "m" or X == "M":
        salir_modo_marca = False
        while salir_modo_marca != True:
            Mm, Ms, rtags, tags, salir_modo_marca = Marca(M, Mt, Mm, Ms, sizey, sizex, rtags, tags)
            mapa.set_data(Ms)
            plt.suptitle(str(Nb-tags) + " bombs")
            plt.pause(antialiaisin)

    else:
        while True:
            try:
                y = int(X)
                while y<0 or y>sizey-1:
                    print("Fuera de límites \n")
                    y=int(input("A: "))

                x = int(input("B: "))
                while x<0 or x>sizex-1:
                    print("Fuera de límites \n")
                    x = int(input("B: "))

                else:
                    errors = 0
                    break

            except:
                print("Un número, A: 'm' para colocar una bomba o A: 'enter' para ver el menú\n")
                errors += 1
                if errors==10:
                    sys.exit("Too many incorrect inputs")

        if M[y,x] == 10 and Mm[y,x]==False:
            Ms = Fallo(M, Mt, Mm, Ms, x, y)
            movs += 1
            jugando = False 
            plt.title("GAME OVER \n Moves = " + str(movs))
            mapa.set_data(Ms)
            plt.pause(antialiaisin)
            print("\n")

        elif Mt[y,x]==False and Mm[y,x]==False:
            Mt, Ms = Agua(Mn, Mt, Ms, x, y)
            movs += 1
            "Moves = " + str(movs)
            mapa.set_data(Ms)
            plt.title("Moves = " + str(movs))
            plt.pause(antialiaisin)
            print("Movimiento", movs+1, "-----------------------")

            if sizey*sizex-Nb == len(np.where(Mt == True)[0]) or rtags==Nb:
                plt.title("VICTORY :D \n Moves = " + str(movs))
                jugando = False

        elif Mm[y,x]==True:
            print("No decías que eso era una bomba?")

        else:
            print("Ya le diste a ese \n")