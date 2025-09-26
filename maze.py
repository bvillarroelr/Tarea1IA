import numpy as np
import random
# n 25, 50
class Maze():
    def __init__(self, n):
        self.n = n
        self.matrix = np.full((n,n), "  ")
        pass
    
    def laberinto_estatico(self):
        self.matrix[0, :] = " ▣"  # Borde superior
        self.matrix[19, :] = " ▣"  # Borde inferior
        self.matrix[:, 0] = " ▣"  # Borde izquierdo
        self.matrix[:, 19] = " ▣"  # Borde derecho
        
        # Paredes interiores según el diseño del laberinto
        
        # Sección superior izquierda
        self.matrix[1:4, 1] = " ▣"  # Pared vertical izquierda
        self.matrix[3, 1:8] = " ▣"  # Pared horizontal
        self.matrix[4:6, 7] = " ▣"  # Pared vertical
        self.matrix[1, 1:6] = " ▣"  # Pared horizontal superior
        self.matrix[2:4, 5] = " ▣"  # Pared vertical
        
        # Sección superior derecha
        self.matrix[1, 11:19] = " ▣"  # Pared horizontal superior derecha
        self.matrix[2:4, 11] = " ▣"  # Pared vertical
        self.matrix[3, 11:16] = " ▣"  # Pared horizontal
        self.matrix[4:6, 15] = " ▣"  # Pared vertical
        
        # Sección central
        self.matrix[7, 1:9] = " ▣"  # Pared horizontal central izquierda
        self.matrix[8:11, 8] = " ▣"  # Pared vertical central
        self.matrix[11, 8:12] = " ▣"  # Pared horizontal central
        self.matrix[8:12, 11] = " ▣"  # Pared vertical central
        self.matrix[7, 15:19] = " ▣"  # Pared horizontal central derecha
        
        # Sección inferior izquierda
        self.matrix[15, 1:8] = " ▣"  # Pared horizontal inferior izquierda
        self.matrix[13:16, 7] = " ▣"  # Pared vertical
        self.matrix[16:19, 5] = " ▣"  # Pared vertical
        self.matrix[17, 5:10] = " ▣"  # Pared horizontal
        
        # Sección inferior derecha
        self.matrix[15, 11:19] = " ▣"  # Pared horizontal inferior derecha
        self.matrix[13:16, 11] = " ▣"  # Pared vertical
        self.matrix[16:19, 15] = " ▣"  # Pared vertical
        self.matrix[17, 12:16] = " ▣"  # Pared horizontal

        # Abrir algunos espacios
        self.matrix[1, 1:6] = "  "  
        self.matrix[1, 11:19] = "  "
        self.matrix[16, 5] = "  "
        self.matrix[18, 15] = "  "

        self.matrix[1, 1] = " X"  # Mala salida
        self.matrix[10, 16] = " X"  # Mala salida
        self.matrix[17, 3] = " O"  # Buena salida

    def mover_laberinto(self):     
        for i in range(20):
            for j in range(20):
                # Mantener bordes como paredes
                if i==0 or i==19 or j==0 or j==19:
                    self.matrix[i,j]=" ▣" 
                    continue
                elif (self.matrix[i,j]==" X" or self.matrix[i,j]==" O"):
                    continue
                elif(self.matrix[i,j]==" ▣"):  
                    random_num=random.randint(1,10)
                    if random_num<=3:
                        self.matrix[i,j]="  "
                        continue
                elif(self.matrix[i,j]=="  "):
                     random_num=random.randint(1,10)
                     if random_num<=3:
                         self.matrix[i,j]=" ▣" 
                         continue
    
    def printMaze(self):
        for fila in self.matrix:
            print("".join(fila))

lab=Maze(20)
lab.laberinto_estatico()
lab.printMaze()
print("\n")
lab.mover_laberinto()
lab.printMaze()