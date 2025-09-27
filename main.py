import lrta
import maze

lab=maze.Maze(20)
lab.laberinto_estatico()
agent=lrta.Lrta()
agent.set_maze_and_goal(lab, (17,3))  # Meta fija en (17,3)
pors=lab.agent_start_position() # Posición inicial del agente
lab.update_visual_matrix()
lab.printMaze()
