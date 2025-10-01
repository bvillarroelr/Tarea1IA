import random

# Códigos de celdas del maze
FREE = 0
AGENT = 1
WALL = 2
FAKE_GOAL = 3
TRUE_GOAL = 4

# Movimientos permitidos y sus deltas
MOVES = ["N", "S", "E", "O"]
DELTA = {
    "N": (-1,  0),
    "S": ( 1,  0),
    "E": ( 0,  1),
    "O": ( 0, -1),
}
# Para evitar “ping-pong” inmediato en la mutación
OPUESTO = {"N": "S", "S": "N", "E": "O", "O": "E"}


class AlgoritmoGenetico:
    """
    Algoritmo Genético para planificar EN LÍNEA (por paso):
      - En cada paso, desde la posición actual y un target (salida candidata),
        evoluciona rápidamente una población de trayectorias cortas y devuelve
        SOLO la PRIMERA acción del mejor cromosoma.

    Parámetros clave:
      - tamaño_poblacion: individuos por paso (pequeño para baja latencia)
      - longitud_cromosoma: horizonte de planificación (p. ej., 8–16)
      - prob_mutacion: probabilidad de mutación por gen (0.05–0.15)
      - prob_cruce: probabilidad de cruce 1 punto (≈0.8)
      - seed: semilla opcional para reproducibilidad
    """

    def __init__(self, tamaño_poblacion, longitud_cromosoma,
                 prob_mutacion=0.1, prob_cruce=0.8, seed=None):
        self.tamaño_poblacion = tamaño_poblacion
        self.longitud_cromosoma = longitud_cromosoma
        self.prob_mutacion = prob_mutacion
        self.prob_cruce = prob_cruce
        self.rng = random.Random(seed)

    def plan_one_action(self, lab, current_pos, target, generations_por_paso=12):
        """
        Devuelve UNA acción ('N','S','E','O') calculada por GA desde current_pos a target.
        Si no encuentra nada razonable, retorna None.
        """
        # Crear población inicial aleatoria
        population = []
        for i in range(self.tamaño_poblacion):
            crom = []
            for j in range(self.longitud_cromosoma):
                crom.append(self.rng.choice(MOVES))
            population.append(crom)

        # Evolucionar pocas generaciones 
        for g in range(generations_por_paso):
            scores = []
            for idx in range(len(population)):
                crom = population[idx]
                fit = self._fitness_to_target(lab, current_pos, crom, target)
                scores.append(fit)

            selected = self._seleccion_torneo(population, scores, k=3)
            population = self._crossover_y_mutacion(selected)

        # Elegir mejor cromosoma final y devolver su primer movimiento
        if len(population) == 0:
            return None

        best_idx = 0
        best_fit = self._fitness_to_target(lab, current_pos, population[0], target)
        for i in range(1, len(population)):
            fit = self._fitness_to_target(lab, current_pos, population[i], target)
            if fit > best_fit:
                best_fit = fit
                best_idx = i

        best_crom = population[best_idx]
        if len(best_crom) == 0:
            return None
        return best_crom[0]

    # Núcleo GA 
    def _seleccion_torneo(self, population, scores, k=3):
        """
        Selección por torneo. Devuelve una nueva lista del mismo tamaño que population,
        con copias de cromosomas seleccionados.
        """
        selected = []
        N = len(population)
        for _ in range(N):
            best_idx = None
            best_fit = None
            # torneo de tamaño k
            for __ in range(k):
                idx = self.rng.randrange(N)
                fit = scores[idx]
                if best_idx is None or fit > best_fit:
                    best_idx = idx
                    best_fit = fit
            selected.append(self._copiar_cromosoma(population[best_idx]))
        return selected

    def _crossover_y_mutacion(self, selected):
        """
        Empareja al azar y aplica cruce de 1 punto con prob_cruce, luego mutación por gen.
        """
        nueva_poblacion = []
        idxs = list(range(len(selected)))
        self.rng.shuffle(idxs)

        i = 0
        while i < len(idxs):
            p1 = selected[idxs[i]]
            if i + 1 < len(idxs):
                p2 = selected[idxs[i + 1]]
            else:
                p2 = selected[idxs[0]]  # si queda impares, empareja con el primero
            h1, h2 = self._cruce_un_punto(p1, p2)
            h1 = self._mutar(h1, self.prob_mutacion)
            h2 = self._mutar(h2, self.prob_mutacion)
            nueva_poblacion.append(h1)
            nueva_poblacion.append(h2)
            i += 2

        # Ajustar tamaño exacto
        if len(nueva_poblacion) > len(selected):
            nueva_poblacion = nueva_poblacion[:len(selected)]
        return nueva_poblacion

    def _cruce_un_punto(self, padre1, padre2):
        """
        Cruce 1 punto con probabilidad prob_cruce.
        """
        if self.rng.random() < self.prob_cruce:
            # punto en [1, L-1] para que ambos lados tengan al menos 1 gen
            punto = self.rng.randint(1, self.longitud_cromosoma - 1)
            hijo1 = padre1[:punto] + padre2[punto:]
            hijo2 = padre2[:punto] + padre1[punto:]
            return hijo1, hijo2
        # sin cruce: copias
        return self._copiar_cromosoma(padre1), self._copiar_cromosoma(padre2)

    def _mutar(self, crom, p):
        """
        Mutación por gen. Evita meter el opuesto inmediato para reducir “N,S,N,S…”.
        """
        mut = self._copiar_cromosoma(crom)
        for i in range(len(mut)):
            if self.rng.random() < p:
                opciones = MOVES[:]  # copia
                if i > 0:
                    op = OPUESTO.get(mut[i - 1])
                    if op in opciones:
                        opciones.remove(op)
                mut[i] = self.rng.choice(opciones)
        return mut

    def _copiar_cromosoma(self, c):
        # copia defensiva de lista de strings
        nuevo = []
        for g in c:
            nuevo.append(g)
        return nuevo

    # Función de aptitud hacia un target concreto (sin saber si es falsa o real)
    def _fitness_to_target(self, lab, start_pos, crom, target):
        """
        Evalúa una trayectoria hacia 'target' (una salida candidata):
          - Respeta paredes y bordes (pasos inválidos NO mueven y penalizan).
          - Shaping: premia acercarse, castiga alejarse.
          - Penaliza revisitas y rachas de bloqueos.
          - Premio moderado si pisa una salida falsa (3) — por “probarla”.
          - Premio grande si pisa la salida verdadera (4) — éxito.
        """
        r = start_pos[0]
        c = start_pos[1]
        n = lab.n

        choques = 0.0
        pasos = 0
        score = 0.0

        # distancia Manhattan inicial al target
        prev_dist = abs(r - target[0]) + abs(c - target[1])
        invalid_streak = 0
        visited = {(r, c)}

        # Simular la secuencia (sin modificar el laberinto real)
        for mv in crom:
            dr = DELTA[mv][0]
            dc = DELTA[mv][1]
            nr = r + dr
            nc = c + dc

            # Fuera de límites o pared entonces no avanza y penaliza
            if nr < 0 or nr >= n or nc < 0 or nc >= n or lab.logical_matrix[nr][nc] == WALL:
                choques += 1.0
                invalid_streak += 1
                score -= 0.5 * invalid_streak  # más castigo si se insiste en chocar
                continue
            else:
                invalid_streak = 0

            # Avanza
            r = nr
            c = nc
            pasos += 1

            # Shaping por distancia al target: acercarse bien, alejarse mal
            dist = abs(r - target[0]) + abs(c - target[1])
            if dist < prev_dist:
                score += 0.5
            else:
                score -= 0.5
            prev_dist = dist

            # Revisitas: pequeño castigo para evitar bucles locales
            if (r, c) in visited:
                choques += 0.5
                score -= 0.2
            else:
                visited.add((r, c))

            # Premios por tocar una salida
            cell = lab.logical_matrix[r][c]
            if cell == TRUE_GOAL:
                score += 10000.0
                break
            elif cell == FAKE_GOAL:
                score += 100.0
                break

        # Penalizaciones suaves al final
        score -= 1.0 * prev_dist   # distancia final al target
        score -= 2.0 * choques     # acumulado de choques/rachas
        score -= 0.05 * pasos      # preferencia por trayectorias más cortas

        return score
