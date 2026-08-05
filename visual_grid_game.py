# visual_grid_game.py
import random
import tkinter as tk


class VisualGridHuntGame:
    """A flexible Pacman-style grid environment with support for configurable opponents and larger scales."""

    def __init__(self, width=10, height=10, num_food=10, num_opponents=2, custom_walls=None):
        self.width = width
        self.height = height
        self.agent_pos = [0, 0]  # Starting position (x, y)
        self.facing = "Up"  # Default facing direction

        if custom_walls is not None:
            self.walls = set(custom_walls)
        else:
            # Generate some default scattered walls for a larger grid
            self.walls = {(2, 2), (2, 3), (5, 5), (6, 5), (3, 7)}

        # Dynamically generate random food positions avoiding walls and agent start
        self.food_positions = set()
        while len(self.food_positions) < num_food:
            fx = random.randint(0, self.width - 1)
            fy = random.randint(0, self.height - 1)
            pos_tuple = (fx, fy)
            if pos_tuple != (0, 0) and pos_tuple not in self.walls:
                self.food_positions.add(pos_tuple)

        #Lab 01 - Generate toxic traps (hazards)
        self.toxic_traps = set()
        num_traps = max(3, self.width // 4)  # Example: scale traps with grid size
        while len(self.toxic_traps) < num_traps:
            tx = random.randint(0, self.width - 1)
            ty = random.randint(0, self.height - 1)
            trap_pos = (tx, ty)
            if trap_pos != (0, 0) and trap_pos not in self.walls and trap_pos not in self.food_positions:
                self.toxic_traps.add(trap_pos)

        # Generate adversarial opponents
        self.opponents = []
        while len(self.opponents) < num_opponents:
            ox = random.randint(0, self.width - 1)
            oy = random.randint(0, self.height - 1)
            op_pos = [ox, oy]
            if tuple(op_pos) != (0, 0) and tuple(op_pos) not in self.walls and tuple(op_pos) not in self.food_positions:
                self.opponents.append(op_pos)

        self.score = 0
        self.steps = 0
        self.collision = False

    #Lab 02(Step 1.1) - Modify to set the Trap (Partial Observability)
    def get_percept(self) -> dict:
        # Track facing direction (default "Up" if not set elsewhere)
        facing = getattr(self, "facing", "Up")

        x, y = self.agent_pos
        if facing == "Up":
            ahead = (x, min(self.height - 1, y + 1))
        elif facing == "Down":
            ahead = (x, max(0, y - 1))
        elif facing == "Left":
            ahead = (max(0, x - 1), y)
        elif facing == "Right":
            ahead = (min(self.width - 1, x + 1), y)
        else:
            ahead = (x, y)

        return {
            'wall_ahead': (ahead in self.walls) or (ahead == (x, y)),
            'food_here': (x, y) in self.food_positions,
            'toxin_here': (x, y) in self.toxic_traps,
            'opponent_here': any(op == [x, y] for op in self.opponents),
            'collision': self.collision,
            'score': self.score,
            'remaining_food': len(self.food_positions)
        }

    def execute_action(self, action: str):
        self.steps += 1

        # Lab 02(Step 1.2)--- Reflex-agent style actions: rotate facing, move in facing direction, or suck food ---
        if action == 'turn_left':
            order = ['Up', 'Left', 'Down', 'Right']  # counter-clockwise rotation
            idx = order.index(self.facing)
            self.facing = order[(idx + 1) % 4]
            return  # turning does not consume a movement step's collision/food/opponent logic

        if action == 'turn_right':
            order = ['Up', 'Right', 'Down', 'Left']  # clockwise rotation
            idx = order.index(self.facing)
            self.facing = order[(idx + 1) % 4]
            return  # turning does not consume a movement step's collision/food/opponent logic

        if action == 'suck':
            tuple_pos = tuple(self.agent_pos)
            if tuple_pos in self.food_positions:
                self.food_positions.remove(tuple_pos)
                self.score += 20
            self._advance_opponents()
            return

        if action == 'move_forward':
            action = self.facing  # translate facing into an Up/Down/Left/Right move
        
        new_pos = list(self.agent_pos)

        if action == 'Up':
            new_pos[1] = min(self.height - 1, new_pos[1] + 1)
        elif action == 'Down':
            new_pos[1] = max(0, new_pos[1] - 1)
        elif action == 'Left':
            new_pos[0] = max(0, new_pos[0] - 1)
        elif action == 'Right':
            new_pos[0] = min(self.width - 1, new_pos[0] + 1)

        if tuple(new_pos) in self.walls:
            self.score -= 5
        else:
            self.agent_pos = new_pos

        tuple_pos = tuple(self.agent_pos)
        if tuple_pos in self.food_positions:
            self.food_positions.remove(tuple_pos)
            self.score += 20

        # Lab 01 - Check if agent stepped on a toxic trap
        if tuple_pos in self.toxic_traps:
            self.score -= 15   # Lab 01 - Penalty for hitting a trap
            self.collision = True

        for op in self.opponents:
            move = random.choice(['Up', 'Down', 'Left', 'Right', 'Stay'])
            if move == 'Up' and op[1] < self.height - 1:
                op[1] += 1
            elif move == 'Down' and op[1] > 0:
                op[1] -= 1
            elif move == 'Left' and op[0] > 0:
                op[0] -= 1
            elif move == 'Right' and op[0] < self.width - 1:
                op[0] += 1

            if op == self.agent_pos:
                self.score -= 50
                self.collision = True

    def is_done(self) -> bool:
        return len(self.food_positions) == 0 or self.steps >= 60 or self.collision

#Lab 02(Step 1.2)
class SimpleReflexAgent:
    """A simple reflex agent get trapped in a corner or a U-shaped wall, infinitely repeating a cycle """

    def __init__(self, env: VisualGridHuntGame):
        self.env = env
        self.env.facing = "Up"  # Default facing direction

    def sense_and_act(self, percept: dict) -> str:
        # Strictly IF-THEN condition-action rules - no memory of past percepts is used.
        if percept['food_here']:
            return 'suck'
        elif percept['wall_ahead']:
            return 'turn_left'
        else:
            return 'move_forward'

#Lab 02(Step 1.3)
class ModelBasedAgent:
    """A simple agent should now remember where it has been, realize it is in a loop, and choose an alternate path to escape."""

    def __init__(self):
        self.visited_cells = set()
        self.position = (0, 0)   # believed starting position
        self.facing = "Up"       # believed starting heading
        self.last_action = None
        self.visited_cells.add(self.position)
        # Per-cell memory of which facings have already been found blocked here.
        # This is what lets the agent escape a true corner (two boundaries/walls
        # meeting), where "left vs right" alone isn't enough info.
        self.blocked_at = {}
 
    # --- helpers: relative directions, purely internal (no env access) ---
    _LEFT_ORDER = ['Up', 'Left', 'Down', 'Right']   # counter-clockwise
    _RIGHT_ORDER = ['Up', 'Right', 'Down', 'Left']  # clockwise
    _DELTAS = {'Up': (0, 1), 'Down': (0, -1), 'Left': (-1, 0), 'Right': (1, 0)}
 
    def _turned(self, order, facing):
        idx = order.index(facing)
        return order[(idx + 1) % 4]
 
    def _opposite(self, facing):
        return self._turned(self._LEFT_ORDER, self._turned(self._LEFT_ORDER, facing))
    
    def _cell_in_direction(self, pos, facing):
        dx, dy = self._DELTAS[facing]
        return (pos[0] + dx, pos[1] + dy)
 
    def sense_and_act(self, percept: dict) -> str:
        # 1) Update state (Transition & Sensor Model): record that we occupy
        #    our believed position, based on the percept + last action taken.
        self.visited_cells.add(self.position)
 
        wall_ahead = percept['wall_ahead']
        food_here = percept['food_here']
        
        if wall_ahead:
            # Remember: at THIS cell, facing THIS direction, we're blocked.
            self.blocked_at.setdefault(self.position, set()).add(self.facing)

        if food_here:
            self.last_action = 'suck'
            return 'suck'  # position/facing unchanged
 
        # 2) IF-THEN rules that QUERY the memory: score every direction we
        #    could face from here using what we remember, then act on the
        #    best one. This is still condition-action logic - just evaluated
        #    over all 4 headings instead of a single hard-coded left/right
        #    chain, which is what lets the agent escape a true corner
        #    (two blocked sides) instead of oscillating between them.
        blocked_here = self.blocked_at.get(self.position, set())
        left_facing = self._turned(self._LEFT_ORDER, self.facing)
        right_facing = self._turned(self._RIGHT_ORDER, self.facing)
        opposite_facing = self._opposite(self.facing)

        # Preference order when scores tie: keep going straight, then left,
        # then right, then a U-turn - cheapest rotation first.
        candidates = [self.facing, left_facing, right_facing, opposite_facing]

        def score(facing):
            if facing in blocked_here:
                return -1  # known wall from here - never choose it
            cell = self._cell_in_direction(self.position, facing)
            return 2 if cell not in self.visited_cells else 1  # prefer new ground

        best_facing = max(candidates, key=score)

        if score(best_facing) == -1:
            # Fully boxed in on every side we know of (rare) - turn to keep
            # sensing; something will eventually look different as walls
            # get remembered/refuted at neighboring cells.
            action = 'turn_left'
        elif best_facing == self.facing:
            action = 'move_forward'
        elif best_facing == left_facing:
            action = 'turn_left'
        elif best_facing == right_facing:
            action = 'turn_right'
        else:  # opposite_facing - takes two ticks; this starts the turn
            action = 'turn_left'
 
        # 3) Apply our own transition model so the belief state stays in sync
        #    with the action we're about to take (mirrors what the real
        #    environment will do in execute_action for the same action).
        if action == 'turn_left':
            self.facing = self._turned(self._LEFT_ORDER, self.facing)
        elif action == 'turn_right':
            self.facing = self._turned(self._RIGHT_ORDER, self.facing)
        elif action == 'move_forward':
            self.position = self._cell_in_direction(self.position, self.facing)
 
        self.last_action = action
        return action

class GridGameGUI:
    """Tkinter wrapper that dynamically scales cell sizes to keep larger grids on screen."""

    def __init__(self, root, width=10, height=10, num_food=12, num_opponents=2, walls=None):
        self.root = root
        self.root.title("IT3012 - Scalable Multi-Agent Grid Hunt")

        self.env = VisualGridHuntGame(width=width, height=height, num_food=num_food, num_opponents=num_opponents,
                                      custom_walls=walls)

        self.agent = ModelBasedAgent()  # Lab 02(Step 1.3) - swap SimpleReflexAgent(self.env) for ModelBasedAgent() to compare the two.
        
        # Dynamically calculate cell size so the total canvas fits nicely within a 600x600 window ceiling
        max_canvas_dim = 600
        self.cell_size = max(20, min(max_canvas_dim // self.env.width, max_canvas_dim // self.env.height))

        canvas_w = self.env.width * self.cell_size
        canvas_h = self.env.height * self.cell_size

        self.canvas = tk.Canvas(root, width=canvas_w, height=canvas_h, bg="white")
        self.canvas.pack()

        self.label = tk.Label(root, text="Score: 0 | Steps: 0", font=("Arial", 14))
        self.label.pack(pady=10)

        self.btn = tk.Button(root, text="Start Simulation", command=self.run_loop, font=("Arial", 12), bg="#000066",
                             fg="white")
        self.btn.pack(pady=5)

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")

        for x in range(self.env.width):
            for y in range(self.env.height):
                x1 = x * self.cell_size
                y1 = (self.env.height - 1 - y) * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = "#f1f5f9" if (x, y) not in self.env.walls else "#64748b"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#cbd5e1")

                # Only draw text if cell is large enough
                if self.cell_size >= 40 and (x, y) in self.env.walls:
                    self.canvas.create_text(x1 + self.cell_size / 2, y1 + self.cell_size / 2, text="W", fill="white",
                                            font=("Arial", 8, "bold"))

        for fx, fy in self.env.food_positions:
            offset = self.cell_size * 0.25
            x1 = fx * self.cell_size + offset
            y1 = (self.env.height - 1 - fy) * self.cell_size + offset
            self.canvas.create_oval(x1, y1, x1 + self.cell_size * 0.5, y1 + self.cell_size * 0.5, fill="#f59e0b",
                                    outline="#d97706")

        for ox, oy in self.env.opponents:
            offset = self.cell_size * 0.2
            x1 = ox * self.cell_size + offset
            y1 = (self.env.height - 1 - oy) * self.cell_size + offset
            self.canvas.create_rectangle(x1, y1, x1 + self.cell_size * 0.6, y1 + self.cell_size * 0.6, fill="#990000",
                                         outline="#7a0000")

        # Lab 01 - Render traps as purple polygons
        for tx, ty in self.env.toxic_traps:
            offset = self.cell_size * 0.25
            x1 = tx * self.cell_size + offset
            y1 = (self.env.height - 1 - ty) * self.cell_size + offset
            self.canvas.create_polygon(
                x1, y1,
                x1 + self.cell_size * 0.5, y1,
                x1 + self.cell_size * 0.25, y1 + self.cell_size * 0.5,
                fill="#9333ea", outline="#6b21a8"  # Purple tones
            )

        ax, ay = self.env.agent_pos
        offset = self.cell_size * 0.15
        x1 = ax * self.cell_size + offset
        y1 = (self.env.height - 1 - ay) * self.cell_size + offset
        self.canvas.create_oval(x1, y1, x1 + self.cell_size * 0.7, y1 + self.cell_size * 0.7, fill="#000066",
                                outline="#1e3a8a")

    def run_loop(self):
        self.btn.config(state="disabled")

        # Lab 02(Step1.2) - SimpleReflexAgent - the agent itself is stateless. We only use it here to detect and report the infinite-loop failure the exercise asks about.
        
        recent_actions = []
        cycle_len = 8  # how many recent (state, action) pairs to watch for a repeat
        
        def step():
            if not self.env.is_done():
                percept = self.env.get_percept()
                action = self.agent.sense_and_act(percept)
                self.env.execute_action(action)

                # Track (position, facing, action) to detect the agent repeating itself
                signature = (tuple(self.env.agent_pos), self.env.facing, action)
                recent_actions.append(signature)
                if len(recent_actions) > cycle_len:
                    recent_actions.pop(0)
                stuck = len(recent_actions) == cycle_len and len(set(recent_actions)) <= cycle_len // 2

                self.draw_grid()
                status = "  |  STUCK IN A LOOP (no memory of past states)" if stuck else ""
                self.label.config(
                    text=f"Score: {self.env.score} | Steps: {self.env.steps} | "
                         f"Facing: {self.env.facing} | Action: {action}{status}"
                )
                self.root.after(250, step)
            else:
                end_text = f"Collision! Game Over! Final Score: {self.env.score}" if self.env.collision else f"Finished! Final Score: {self.env.score}"
                self.label.config(text=end_text)
                self.btn.config(state="normal")

        step()

if __name__ == "__main__":
    root = tk.Tk()
    # Try a larger grid size like 12x12 with 15 food and 3 opponents!
    app = GridGameGUI(root, width=12, height=12, num_food=15, num_opponents=0)
    root.mainloop()