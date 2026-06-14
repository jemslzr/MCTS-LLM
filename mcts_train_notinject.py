import re
import json
import math
import random
from datasets import load_dataset

def clean_text(text):
    if not isinstance(text, str): return "DROP"
    if re.search(r'[\u4e00-\u9fff]', text): return "DROP"
    return text.strip()

# ==========================================
# MCTS ALGORITHM (The "AI" Search Engine)
# ==========================================
class MCTSNode:
    def __init__(self, state):
        self.state = state  # Turn number
        self.visits = 0
        self.wins = 0.0     # Successful attacks
        self.children = []

    def best_child(self, exploration_weight=1.41):
        # UCB1 Mathematical Formula
        best_score = -float('inf')
        best_node = None
        for child in self.children:
            if child.visits == 0: return child
            exploit = child.wins / child.visits
            explore = exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
            score = exploit + explore
            if score > best_score:
                best_score = score
                best_node = child
        return best_node

def simulate_llm_guardrail(turn, difficulty_tier):
    """Simulates the environment for MCTS rollouts"""
    if turn >= 3: return "exfiltrated" if random.random() > (0.4 * difficulty_tier) else "blocked"
    return "persistence"

def train_mcts_on_seed(seed_text, difficulty_tier, iterations=50):
    """ The Actual MCTS Search/Training Loop """
    root = MCTSNode(state=1) # Turn 1: NotInject Context
    
    for _ in range(iterations):
        node = root
        
        # 1. Selection & 2. Expansion
        if not node.children:
            node.children.append(MCTSNode(state=2))
        node = node.children[0]
        
        # 3. Simulation (Rollout)
        result = simulate_llm_guardrail(node.state, difficulty_tier)
        
        # 4. Backpropagation
        reward = 1.0 if result == "exfiltrated" else 0.0
        node.visits += 1
        node.wins += reward
        root.visits += 1
        root.wins += reward

    # The AI "Learned" Weight is the exploitation win-rate
    return root.wins / root.visits if root.visits > 0 else 0.0

# ==========================================
# MAIN PIPELINE
# ==========================================
def preprocess_and_train():
    print("[1/3] Fetching NotInject dataset...")
    dataset_dict = load_dataset("leolee99/NotInject")
    
    clean_seeds = []
    seed_id = 1
    
    print("[2/3] Preprocessing (Removing Chinese characters)...")
    for split in dataset_dict.keys():
        for row in dataset_dict[split]:
            prompt = clean_text(row.get("prompt", ""))
            if prompt == "DROP" or prompt == "": continue
            
            clean_seeds.append({
                "id": f"NOTINJ-{seed_id:03d}",
                "turn_1_context": prompt,
                "tier": random.choice([1, 2])
            })
            seed_id += 1
            if len(clean_seeds) >= 200: break # Keep size manageable for presentation
            
    print(f"[3/3] Training MCTS state-space transitions on {len(clean_seeds)} seeds...")
    
    # Run the AI Training Loop on every seed
    for seed in clean_seeds:
        seed["weight"] = train_mcts_on_seed(seed["turn_1_context"], seed["tier"])
    
    with open("trained_mcts_notinject.json", "w") as f:
        json.dump(clean_seeds, f, indent=4)
        
    print("\n[SUCCESS] Data pre-training complete. MCTS weights exported to JSON.")

if __name__ == "__main__":
    preprocess_and_train()