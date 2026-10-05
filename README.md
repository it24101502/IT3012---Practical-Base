## 📸 Screenshots

### Part 1: The Logic Engine Architecture

#### Step 1.1: Building the Knowledge Base (KB)
* **Description**: Storing unique facts in a `set` and Horn clause rules as tuples `([premises], conclusion)`.

| Code & Output | Implementation Verification |
| :---: | :---: |
| ![Step 1.1 (1)](images/Step%201.1%20%281%29.png) | ![Step 1.1 (2)](images/Step%201.1%20%282%29.png) |

---

### Part 2: Implementing Forward Chaining

#### Step 2.1: Inference Engine Algorithm
* **Description**: Translating the Data-Driven Forward Chaining algorithm with Modus Ponens verification into code.

| Algorithm Implementation | Execution Proof |
| :---: | :---: |
| ![Step 2.1 (1)](images/Step%202.1%20%281%29.png) | ![Step 2.1 (2)](images/Step%202.1%20%282%29.png) |

---

### Part 3: Hooking Logic into the Grid Game

#### Step 3.1: Defining Game Constraints
* **Description**: Translating domain safety constraints into Horn clauses in `SearchAgent.__init__()`.
  * $Rule\ 1: \text{TargetVisible} \land \text{HasDust} \implies \text{SafeToEngage}$
  * $Rule\ 2: \text{SafeToEngage} \land \text{BloodseekerMissing} \implies \text{Retreat}$

![Step 3.1](images/Step%203.1.png)

---

#### Step 3.2: Validating Feasibility in A*
* **Description**: Updating `astar_search()` to evaluate successor tiles via `forward_chain()` and skipping any tile where `'Retreat'` is derived.

| A* Modification | Step-by-Step Logic Pruning | Execution Check |
| :---: | :---: | :---: |
| ![Step 3.2 (1)](images/Step%203.2%20%281%29.png) | ![Step 3.2 (2)](images/Step%203.2%20%282%29.png) | ![Step 3.2 (3)](images/Step%203.2%20%283%29.png) |

---

#### Step 3.3: Visual Grid Simulation Run
* **Description**: Running `visual_grid_game.py` with sample tile facts. Coordinate `(1, 0)` generates `'Retreat'` and is dynamically avoided by the agent throughout execution.

| Initial State & Setup | Step Execution | Mid-Game Routing | Near Completion | Final Score Screen |
| :---: | :---: | :---: | :---: | :---: |
| ![Step 3.3 (1)](images/Step%203.3%20%281%29.png) | ![Step 3.3 (2)](images/Step%203.3%20%282%29.png) | ![Step 3.3 (3)](images/Step%203.3%20%283%29.png) | ![Step 3.3 (4)](images/Step%203.3%20%284%29.png) | ![Step 3.3 (5)](images/Step%203.3%20%285%29.png) |

---

### Part 4: Automated Verification Test Suite

#### Step 4.1: Logic Engine Unit Tests
* **Description**: Running automated assertion tests in `test_logic.py` to verify mathematical correctness.

![Step 4.1](images/Step%204.1.png)

---

## 🚀 How to Run

1. **Run Automated Test Suite**:
   ```bash
   python test_logic.py

2. **Run Visual Grid Game Simulation**:
   ```bash
   python visual_grid_game.py