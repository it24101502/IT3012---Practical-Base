# agent.py
import random
from collections import deque
import heapq

class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        # If standing directly on food, or just wander / move towards coordinates
        pos = percept['agent_pos']
        # Simple heuristic or fallback random sweep
        return random.choice(self.actions_pool)

#Lab 03(Step 1.2) - Create class
class SearchAgent:
    #Lab 03(Step 1.3) - initiate   
    def __init__(self):
        self.plan = []
        self.active_algo = "UCS"
    
    #Lab 03(Step 1.3) -
    def sense_and_act(self, percept):
        current_pos = percept['agent_pos']
        all_food = percept['all_food']
        grid_size = percept['grid_size']
        walls = percept['walls']

        if not self.plan:
            target_food = self.find_closest_food(current_pos,all_food)
            
            if target_food is None:
                return "UP"
            
            if self.active_algo == "BFS":
                self.plan = self.bfs_search(current_pos,target_food,grid_size,walls)
            elif self.active_algo == "DFS":
                self.plan = self.dfs_search(current_pos,target_food,grid_size,walls)
            elif self.active_algo == "UCS":
                self.plan = self.ucs_search(current_pos,target_food,grid_size,walls)

        if self.plan:
            return self.plan.pop(0)

        return "UP"

    #Lab 03(Step 1.3) - Finds the nearest food pellet using Manhattan distance.
    def find_closest_food(self, start, all_food):
        if not all_food:
            return None

        return min(all_food,key=lambda food: abs(food[0] - start[0]) + abs(food[1] - start[1]))

    #Lab 03(Step 1.2) - get neigbours
    def get_neighbors(self, state, grid_size, walls):
        x, y = state

        possible_moves = {
            "UP": (x, y - 1),
            "DOWN": (x, y + 1),
            "LEFT": (x - 1, y),
            "RIGHT": (x + 1, y)
        }

        neighbors = []

        for action, (nx, ny) in possible_moves.items():
            if (0 <= nx < grid_size[0] and 0 <= ny < grid_size[1] and (nx, ny) not in walls):
                neighbors.append((action, (nx, ny)))

        return neighbors

    #Lab 03(Step 1.2) - Implement BFS
    def bfs_search(self, start, goal, grid_size, walls):
        frontier = deque([(start, [])])
        reached = {start}

        while frontier:
            state, path = frontier.popleft()
            if state == goal:
                return path

            for action, next_state in self.get_neighbors(state, grid_size, walls):
                if next_state not in reached:
                    reached.add(next_state)
                    frontier.append((next_state,path + [action]))

        return []

    #Lab 03(Step 1.2) - Implement DFS
    def dfs_search(self, start, goal, grid_size, walls):
        frontier = [(start, [])]
        reached = {start}

        while frontier:
            state, path = frontier.pop()
            if state == goal:
                return path

            for action, next_state in self.get_neighbors(state,grid_size,walls):
                if next_state not in reached:
                    reached.add(next_state)
                    frontier.append((next_state,path + [action]))

        return []

    #Lab 03(Step 1.2) - Implement UCS
    def ucs_search(self, start, goal, grid_size, walls):
        frontier = []
        heapq.heappush(frontier,(0, start, []))
        reached = set()

        while frontier:
            cost, state, path = heapq.heappop(frontier)
            if state in reached:
                continue

            reached.add(state)

            if state == goal:
                return path

            for action, next_state in self.get_neighbors(state,grid_size,walls):
                if next_state not in reached:
                    heapq.heappush(frontier,(cost + 1,next_state,path + [action]))

        return []

    