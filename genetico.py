import random
import agent
# algoritmo genético: proceso de evolución artificial
# cada cromosoma representa una secuencia de movimientos del agente
# Atributos:
# cromosoma: representación de una posible solución al problema (secuencia de acciones en este caso)
# población inicial: posibleles soluciones iniciales que el agente podria intentar
# fitness: qué tan buena es una solución (cromosoma) para resolver el problema
# selección: elegir los mejores cromosomas para reproducirse y crear la próxima generación
# cruce: combinar partes de dos cromosomas para crear nuevos cromosomas (hijos)
# mutación: introducir cambios aleatorios en algunos cromosomas para mantener la diversidad genética (cambios de acciones en este caso)
# evolución: repetir el proceso de selección, cruce y mutación durante varias generaciones para mejorar la población

# finalmente, el mejor cromosoma obtenido es la ruta candidata más prometedora para resolver el laberinto

# Códigos del laberinto establecidos en maze.py pero nombrados para mayor legibilidad

FREE = 0
AGENT = 1
WALL = 2
FAKE_GOAL = 3
TRUE_GOAL = 4

# Movimientos (N,S,E,O)
MOVES = ["N", "S", "E", "O"]
DELTA = {
    "N": (-1,  0),
    "S": ( 1,  0),
    "E": ( 0,  1),
    "O": ( 0, -1),
}

class AlgoritmoGenetico:
    def __init__(self, tamaño_poblacion, longitud_cromosoma, seed=None):
        self.tamaño_poblacion = tamaño_poblacion
        self.longitud_cromosoma = longitud_cromosoma
        self.rng = random.Random(seed) #si no se pasa seed, python usa el reloj del sistema, siempre aleatorio.
        self.poblacion = []  # lista de cromosomas (cada uno es lista de "N","S","E","O")

    # 1) Generar población inicial (rutas aleatorias)
    def inicializar_poblacion(self):
        self.poblacion = []
        for _ in range(self.tamaño_poblacion):
            crom = [self.rng.choice(MOVES) for _ in range(self.longitud_cromosoma)]
            self.poblacion.append(crom)

    # 2) Buscar la meta verdadera (celda == 4)
    def true_goal(self, maze):
        n = len(maze.logical_matrix)
        for i in range(n):
            for j in range(n):
                if maze.logical_matrix[i][j] == TRUE_GOAL:
                    return (i, j)
        raise ValueError("No se encontró meta verdadera (celda == 4).")

    # 3) Aplicar una ruta respetando bordes y paredes, tomando como
    #    estado inicial la posición que tenga el Agent (x,y).
    #    Nota: NO modifica el maze ni el agent; solo simula.
    def aplicar_ruta(self, start, cromosoma, maze):
        r, c = start  # (x,y) segun tu Agent:contentReference[oaicite:2]{index=2}
        n = len(maze.logical_matrix)
        choques = 0
        pasos = 0
        for mv in cromosoma:
            dr, dc = DELTA[mv]
            nr, nc = r + dr, c + dc
            # límites
            if nr < 0 or nr >= n or nc < 0 or nc >= n:
                choques += 1
                continue
            # pared
            if maze.logical_matrix[nr][nc] == WALL:
                choques += 1
                continue
            # avanzar
            r, c = nr, nc
            pasos += 1
            # llegó a la meta verdadera
            if maze.logical_matrix[r][c] == TRUE_GOAL:
                break
        return (r, c, choques, pasos)

    # 4) Fitness sencillo:
    #    + recompensa alta por llegar a (4)
    #    - penaliza distancia final si no llega
    #    - penaliza choques y un poco los pasos
    def fitness_basico(self, maze, start, cromosoma, goal):
        r, c, choques, pasos = self.aplicar_ruta(start, cromosoma, maze)
        
        if (r, c) == goal:
            return 1000.0 - 0.1 * pasos
        
        dist = abs(r - goal[0]) + abs(c - goal[1])
        score = -1.0 * dist
        score -= 2.0 * choques
        score -= 0.05 * pasos
        return score

    # 5) Elegir el mejor cromosoma de la población según este fitness
    def mejor_actual(self, maze, agent):
        goal = self.true_goal(maze)
        mejor = None
        mejor_fit = float("-inf")
        for crom in self.poblacion:
            fit = self.fitness_basico(maze, agent, crom, goal)
            if fit > mejor_fit:
                mejor, mejor_fit = crom, fit
        return mejor, mejor_fit

    # 6) Selección por torneo
    def seleccion_torneo(self, maze, start, tamaño_torneo=3):
        goal = self.true_goal(maze)
        mejor_crom = None
        mejor_fit = float("-inf")
        
        # Elegir aleatoriamente cromosomas para el torneo
        candidatos = self.rng.sample(self.poblacion, tamaño_torneo)
        
        for crom in candidatos:
            fit = self.fitness_basico(maze, start, crom, goal)
            if fit > mejor_fit:
                mejor_fit = fit
                mejor_crom = crom
        
        return mejor_crom.copy()

    # 7) Cruce de un punto
    def cruce_un_punto(self, padre1, padre2):
        if self.rng.random() > 0.8:  # 80% probabilidad de cruce
            return padre1.copy(), padre2.copy()
        
        punto = self.rng.randint(1, self.longitud_cromosoma - 1)
        hijo1 = padre1[:punto] + padre2[punto:]
        hijo2 = padre2[:punto] + padre1[punto:]
        return hijo1, hijo2

    # 8) Mutación
    def mutar(self, cromosoma, prob_mutacion=0.1):
        mutado = cromosoma.copy()
        for i in range(len(mutado)):
            if self.rng.random() < prob_mutacion:
                mutado[i] = self.rng.choice(MOVES)
        return mutado

    # 9) Algoritmo principal con integración de agent
    def evolucionar(self, maze, agente, generaciones=50):
        """
        Ejecuta el algoritmo genético usando la clase agent
        """
        print("=== INICIANDO ALGORITMO GENÉTICO ===")
        start = agente.position_getter()  # Usar posición actual del agente
        print(f"Posición inicial del agente: {start}")
        
        # Inicializar población
        self.inicializar_poblacion()
        print(f"Población inicializada: {self.tamaño_poblacion} cromosomas")
        
        mejor_solucion = None
        mejor_fitness_global = float("-inf")
        
        for gen in range(generaciones):
            print(f"\n--- Generación {gen + 1} ---")
            
            # Evaluar población actual
            fitness_scores = []
            goal = self.true_goal(maze)
            
            for crom in self.poblacion:
                fit = self.fitness_basico(maze, start, crom, goal)
                fitness_scores.append(fit)
            
            # Estadísticas de la generación
            mejor_fit_gen = max(fitness_scores)
            promedio_fit = sum(fitness_scores) / len(fitness_scores)
            
            # Actualizar mejor solución global
            if mejor_fit_gen > mejor_fitness_global:
                mejor_fitness_global = mejor_fit_gen
                mejor_idx = fitness_scores.index(mejor_fit_gen)
                mejor_solucion = self.poblacion[mejor_idx].copy()
            
            print(f"Mejor fitness: {mejor_fit_gen:.2f}")
            print(f"Fitness promedio: {promedio_fit:.2f}")
            
            # Verificar si encontró la solución
            if mejor_fit_gen >= 1000:
                print("¡SOLUCIÓN ENCONTRADA!")
                # Actualizar posición del agente al final del mejor camino
                r, c, _, _ = self.aplicar_ruta(start, mejor_solucion, maze)
                agente.position_setter(r, c)
                return mejor_solucion, gen + 1
            
            # Crear nueva población
            nueva_poblacion = []
            
            # Elitismo: mantener el mejor cromosoma
            mejor_idx = fitness_scores.index(mejor_fit_gen)
            nueva_poblacion.append(self.poblacion[mejor_idx].copy())
            
            # Generar resto de la población
            while len(nueva_poblacion) < self.tamaño_poblacion:
                # Selección
                padre1 = self.seleccion_torneo(maze, start)
                padre2 = self.seleccion_torneo(maze, start)
                
                # Cruce
                hijo1, hijo2 = self.cruce_un_punto(padre1, padre2)
                
                # Mutación
                hijo1 = self.mutar(hijo1)
                hijo2 = self.mutar(hijo2)
                
                nueva_poblacion.extend([hijo1, hijo2])
            
            # Actualizar población (mantener tamaño exacto)
            self.poblacion = nueva_poblacion[:self.tamaño_poblacion]
            
            # Adaptación dinámica cada 10 generaciones
            if gen > 0 and gen % 10 == 0:
                print(">>> Aplicando cambios dinámicos al laberinto...")
                maze.mover_laberinto()
        
        print(f"\nGeneraciones completadas. Mejor fitness alcanzado: {mejor_fitness_global:.2f}")
        
        # Si no encontró la meta, mover el agente al mejor resultado
        if mejor_solucion:
            r, c, _, _ = self.aplicar_ruta(start, mejor_solucion, maze)
            agente.position_setter(r, c)
            print(f"Agente movido a la mejor posición encontrada: ({r}, {c})")
        
        return mejor_solucion, generaciones

    # 10) Función para mostrar la ruta del agente
    def mostrar_ruta(self, cromosoma, maze, agente):
        """
        Muestra paso a paso cómo se mueve el agente siguiendo el cromosoma
        """
        start = agente.position_getter()
        print(f"Ruta desde {start}:")
        
        r, c = start
        n = len(maze.logical_matrix)
        
        for i, mv in enumerate(cromosoma):
            dr, dc = DELTA[mv]
            nr, nc = r + dr, c + dc
            
            # Verificar movimiento válido
            if nr < 0 or nr >= n or nc < 0 or nc >= n:
                print(f"Paso {i+1}: {mv} -> FUERA DE LÍMITES, se queda en ({r}, {c})")
                continue
            
            if maze.logical_matrix[nr][nc] == WALL:
                print(f"Paso {i+1}: {mv} -> PARED, se queda en ({r}, {c})")
                continue
            
            # Movimiento exitoso
            r, c = nr, nc
            cell_type = maze.logical_matrix[r][c]
            
            if cell_type == TRUE_GOAL:
                print(f"Paso {i+1}: {mv} -> ({r}, {c}) ¡META ALCANZADA!")
                break
            elif cell_type == FAKE_GOAL:
                print(f"Paso {i+1}: {mv} -> ({r}, {c}) - Salida falsa")
            else:
                print(f"Paso {i+1}: {mv} -> ({r}, {c})")
        
        # Actualizar posición del agente
        agente.position_setter(r, c)
        return (r, c)

    # 11) Función de prueba
    def probar_algoritmo(self, maze):
        """
        Función de prueba que crea un agente y ejecuta el algoritmo
        """
        # Crear agente en posición inicial
        agente = agent.Agent()
        pos_inicial = maze.agent_start_position()
        agente.position_setter(pos_inicial[0], pos_inicial[1])
        
        print("=== PRUEBA DEL ALGORITMO GENÉTICO ===")
        maze.printMaze()
        
        # Ejecutar algoritmo
        solucion, generaciones = self.evolucionar(maze, agente, generaciones=30)
        
        if solucion:
            print(f"\n=== RESULTADO ===")
            print(f"Solución encontrada en {generaciones} generaciones")
            print(f"Posición final del agente: {agente.position_getter()}")
            
            # Mostrar primeros movimientos de la solución
            print("Primeros 15 movimientos de la mejor solución:")
            print(" -> ".join(solucion[:15]))
            
            # Mostrar ruta completa (opcional)
            respuesta = input("\n¿Mostrar ruta completa paso a paso? (s/n): ")
            if respuesta.lower() == 's':
                # Resetear agente a posición inicial para mostrar ruta
                agente.position_setter(pos_inicial[0], pos_inicial[1])
                self.mostrar_ruta(solucion, maze, agente)
        
        return solucion