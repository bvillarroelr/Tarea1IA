import numpy as np
import random
# n 25, 50
# logical_matrix: 0 espacio libre, 1 agente, 2 paredes, 3 mala salida, 4 buena salida
MAXWALLS = 20
MAXEMPTYS = 20

class Maze():
    def __init__(self, n):
        self.n = n
        self.logical_matrix = np.zeros((n,n))
        self.visual_matrix = np.full((n,n), "  ")
        self.agentProtectRadius = 4
        self.exitProtectRadius = 4
        self.agent = None
        pass
    
    # NOTA: esta función crea un laberinto fijo, y de momento solo lo usamos de prueba
    def laberinto_estatico(self):
        # Bordes del laberinto (valor 2)
        self.logical_matrix[0, :] = 2  # Borde superior
        self.logical_matrix[19, :] = 2  # Borde inferior
        self.logical_matrix[:, 0] = 2  # Borde izquierdo
        self.logical_matrix[:, 19] = 2  # Borde derecho
        
        # Paredes interiores según el diseño del laberinto (valor 2)
        
        # Sección superior izquierda
        self.logical_matrix[1:4, 1] = 2  # Pared vertical izquierda
        self.logical_matrix[3, 1:8] = 2  # Pared horizontal
        self.logical_matrix[4:6, 7] = 2  # Pared vertical
        self.logical_matrix[1, 1:6] = 2  # Pared horizontal superior
        self.logical_matrix[2:4, 5] = 2  # Pared vertical
        
        # Sección superior derecha
        self.logical_matrix[1, 11:19] = 2  # Pared horizontal superior derecha
        self.logical_matrix[2:4, 11] = 2  # Pared vertical
        self.logical_matrix[3, 11:16] = 2  # Pared horizontal
        self.logical_matrix[4:6, 15] = 2  # Pared vertical
        
        # Sección central
        self.logical_matrix[7, 1:9] = 2  # Pared horizontal central izquierda
        self.logical_matrix[8:11, 8] = 2  # Pared vertical central
        self.logical_matrix[11, 8:12] = 2  # Pared horizontal central
        self.logical_matrix[8:12, 11] = 2  # Pared vertical central
        self.logical_matrix[7, 15:19] = 2  # Pared horizontal central derecha
        
        # Sección inferior izquierda
        self.logical_matrix[15, 1:8] = 2  # Pared horizontal inferior izquierda
        self.logical_matrix[13:16, 7] = 2  # Pared vertical
        self.logical_matrix[16:19, 5] = 2  # Pared vertical
        self.logical_matrix[17, 5:10] = 2  # Pared horizontal
        
        # Sección inferior derecha
        self.logical_matrix[15, 11:19] = 2  # Pared horizontal inferior derecha
        self.logical_matrix[13:16, 11] = 2  # Pared vertical
        self.logical_matrix[16:19, 15] = 2  # Pared vertical
        self.logical_matrix[17, 12:16] = 2  # Pared horizontal

        # Abrir algunos espacios (valor 0 - espacio libre)
        self.logical_matrix[1, 1:6] = 0  
        self.logical_matrix[1, 11:19] = 0
        self.logical_matrix[16, 5] = 0
        self.logical_matrix[18, 15] = 0

        # Colocar salidas
        self.logical_matrix[1, 1] = 3  # Mala salida
        self.logical_matrix[10, 16] = 3  # Mala salida
        self.logical_matrix[17, 3] = 4  # Buena salida
        
        # Actualizar la matriz visual basada en la lógica
        self.update_visual_matrix()
    
    def update_visual_matrix(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.logical_matrix[i,j] == 0:  # Espacio libre
                    self.visual_matrix[i,j] = "  "
                elif self.logical_matrix[i,j] == 1:  # Agente
                    self.visual_matrix[i,j] = " A"
                elif self.logical_matrix[i,j] == 2:  # Pared
                    self.visual_matrix[i,j] = " ▣"
                elif self.logical_matrix[i,j] == 3:  # Mala salida
                    self.visual_matrix[i,j] = " X"
                elif self.logical_matrix[i,j] == 4:  # Buena salida
                    self.visual_matrix[i,j] = " O"

    def mover_laberinto(self):     
        walls = 0
        emptys = 0
        
        for i in range(self.n):
            for j in range(self.n):
                # Mantener bordes como paredes
                if i==0 or i==self.n-1 or j==0 or j==self.n-1:
                    self.logical_matrix[i,j] = 2  # Pared
                    continue

                # No modificar salidas ni agente
                elif (self.logical_matrix[i,j] == 3 or self.logical_matrix[i,j] == 4 or self.logical_matrix[i,j] == 1):
                    continue
                # Protecciones para no encerrar salidas ni al agente
                elif self.isProtected(i, j):
                    continue

                elif self.logical_matrix[i,j] == 2:  # Es pared
                    random_num = random.randint(0,10)
                    if random_num <= 1:
                        self.logical_matrix[i,j] = 0  # Cambiar a espacio libre
                        emptys += 1
                        if emptys >= MAXEMPTYS:
                            return
                        continue

                elif self.logical_matrix[i,j] == 0:  # Es espacio libre
                    random_num = random.randint(0,10)
                    if random_num <= 1:
                        self.logical_matrix[i,j] = 2  # Cambiar a pared
                        walls += 1
                        if walls >= MAXWALLS:
                            return
                        continue
        
        # Actualizar la matriz visual después de todos los cambios
        self.update_visual_matrix()
    
    def printMaze(self):
        for fila in self.visual_matrix:
            print("".join(fila))

    def isProtected(self, x, y):
        # Verificar protección del agente
        if self.agent and self.agent.x is not None and self.agent.y is not None:
            distancia_agente = self.manhattanDistance(x, y, self.agent.x, self.agent.y)
            if distancia_agente <= self.agentProtectRadius:
                return True
        
        # Verificar protección de salidas
        salidas = self.findExits()
        for salida_x, salida_y in salidas:
            distancia_salida = self.manhattanDistance(x, y, salida_x, salida_y)
            if distancia_salida <= self.exitProtectRadius:
                return True
        
        return False
        
    # para espacio en el que solo nos podemos mover en 4 direcciones conviene usar la distancia manhattan
    def manhattanDistance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)
        
    def findExits(self):
        exits = []
        for i in range(self.n):
            for j in range(self.n):
                if self.logical_matrix[i,j] == 3 or self.logical_matrix[i,j] == 4:
                    exits.append((i, j))
        return exits

    def printLogical(self):
        print(self.logical_matrix)

    def agent_start_position(self):
        x = random.randint(1, self.n-2)
        y = random.randint(1, self.n-2)
        while self.logical_matrix[x,y] != 0:  # Asegurarse de que es un espacio libre
            x = random.randint(1, self.n-2)
            y = random.randint(1, self.n-2)
        self.logical_matrix[x,y] = 1  # Colocar al agente en la posición inicial
        return (x,y)

""""
lab=Maze(20)
lab.laberinto_estatico()
lab.printMaze()
lab.printLogical()
print("\n")
lab.mover_laberinto()
lab.printMaze()
lab.printLogical()
"""