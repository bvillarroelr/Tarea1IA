import random 
import agent

class Lrta():
    def __init__(self):
        self.H = {}  # heurística aprendida
        self.result = {}  # transiciones observadas
        self.s_prev = None  # estado previo
        self.a_prev = None  # acción previa
        self.maze = None  # referencia al laberinto
        self.goal = None  # meta fija
        self.agente = agent.Agent()  # Instancia del agente
        self.visit_count = {} # Conteo de visitas a estados

   # def set_maze_and_goal(self, maze, goal): # Esto no lo estoy ocupando
    #    self.maze = maze
     #   self.goal = goal

    def goals(self, maze):
        goals = []
        for i in range(maze.n):
            for j in range(maze.n):
                if maze.logical_matrix[i, j] >= 3:  # Si es una buena salida
                    goals.append((i, j))
        return goals

    def heuristic(self, state, goal):
        # Coordenadas de la posicion actual y la meta
        return abs(state[0] - goal[0]) + abs(state[1] - goal[1])
    
    def find_closest_goal(self, agent_position, maze):
        goals = self.goals(maze)
        
        if not goals:
            return None  # No hay metas disponibles
        
        # Calcular distancias a todas las metas
        distances = []
        for goal in goals:
            distance = self.heuristic(agent_position, goal)
            distances.append((distance, goal))
        
        # Ordenar por distancia y devolver la más cercana
        distances.sort(key=lambda x: x[0])
        closest_distance, closest_goal = distances[0]
        
        print(f"Agente en {agent_position}, meta más cercana: {closest_goal} (distancia: {closest_distance})")
        return closest_goal

    def actions(self, state, maze):
        #Acciones posibles (N,S,E,O) si no son paredes.
        moves = {
            "N": (-1, 0),
            "S": (1, 0),
            "E": (0, 1),
            "O": (0, -1)
        }
        valid = []
        for a, (di, dj) in moves.items():
            ni, nj = state[0] + di, state[1] + dj
            if maze.logical_matrix[ni, nj] != 2:  # Si no es pared
                valid.append((a, (ni, nj)))
        return valid

    def lrta_cost(self, s, a, s_next, goal):
        if s_next is None:
            return self.heuristic(s, goal)
        return 1 + self.H.get(s_next, self.heuristic(s_next, goal))

    def lrta_agent(self, s_prime, maze):
        # Encontrar la meta más cercana dinámica
        goal = self.find_closest_goal(s_prime, maze)

        # Si ya llegó a la meta
        if s_prime == goal:
            return None

        # Inicializar heurística para estado nuevo
        if s_prime not in self.H:
            self.H[s_prime] = self.heuristic(s_prime, goal)

        # Actualizar heurística del estado previo 
        if self.s_prev is not None:
            self.result[(self.s_prev, self.a_prev)] = s_prime
            succs = self.actions(self.s_prev, maze)
            self.H[self.s_prev] = min(
                self.lrta_cost(self.s_prev, act, self.result.get((self.s_prev, act)), goal)
                for act, _ in succs
            )

        # Generar sucesores desde el estado actual
        succs = self.actions(s_prime, maze)
        costs = []

        for a, s_next in succs:
            # Costo LRTA normal
            base_cost = self.lrta_cost(s_prime, a, self.result.get((s_prime, a), s_next), goal)

            # Penalización por visitas repetidas
            visit_penalty = self.visit_count.get(s_next, 0) * 0.5

            # Penalizar regresar al estado previo inmediato
            if self.s_prev is not None and s_next == self.s_prev:
                visit_penalty += 0.8

            total_cost = base_cost + visit_penalty
            costs.append((a, s_next, total_cost))

        if not costs:
            print(f" El agente quedó encerrado en {s_prime}.")
            return None

        # Desempate aleatorio + ordenar por costo
        random.shuffle(costs)
        costs.sort(key=lambda x: x[2])

        # Elegir mejor acción (ya penalizada)
        best_action, best_state, best_cost = costs[0]

        # Actualizar tracking del agente
        self.s_prev, self.a_prev = s_prime, best_action

        # Registrar visita
        self.visit_count[best_state] = self.visit_count.get(best_state, 0) + 1

        # Mover agente en entorno
        self.agente.position_setter(best_state[0], best_state[1])

        return best_action, best_state
