class Lrta():
    def __init__(self):
        self.H = {}  # heurística aprendida
        self.result = {}  # transiciones observadas
        self.s_prev = None  # estado previo
        self.a_prev = None  # acción previa
        self.maze = None  # referencia al laberinto
        self.goal = None  # meta fija

    def set_maze_and_goal(self, maze, goal):
        self.maze = maze
        self.goal = goal

    def heuristic(self, state, goal):
        # Coordenadas de la posicion actual y la meta
        return abs(state[0] - goal[0]) + abs(state[1] - goal[1])

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
            if maze.matrix[ni, nj] != 2:  # Si no es pared
                valid.append((a, (ni, nj)))
        return valid

    def lrta_cost(self, s, a, s_next, goal):
        if s_next is None:
            return self.heuristic(s, goal)
        return 1 + self.H.get(s_next, self.heuristic(s_next, goal))

    def lrta_agent(self, s_prime, goal, maze):
        # Parametros son el estado actual, la meta y el laberinto
        # Si estamos en el objetivo, parar
        if s_prime == goal:
            return None
        
        # Inicializar heurística con la ubicación actual
        if s_prime not in self.H:
            self.H[s_prime] = self.heuristic(s_prime, goal)
        
        # Actualizar el estado anterior
        if self.s_prev is not None:
            self.result[(self.s_prev, self.a_prev)] = s_prime
            succs = self.actions(self.s_prev, maze)
            self.H[self.s_prev] = min(
                self.lrta_cost(self.s_prev, act, self.result.get((self.s_prev, act)), goal)
                for act, _ in succs
            )
        
        # Elegir la acción que minimiza el costo
        succs = self.actions(s_prime, maze)
        a, s_next = min(
            succs,
            key=lambda x: self.lrta_cost(s_prime, x[0], self.result.get((s_prime, x[0]), x[1]), goal)
        )
        
        self.s_prev, self.a_prev = s_prime, a
        return a, s_next