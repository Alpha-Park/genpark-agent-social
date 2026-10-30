# -*- coding: utf-8 -*-
from client import GenParkAgentSocial

social = GenParkAgentSocial()

# 1. R0 Viral Reproduction Rate
r0 = social.estimate_basic_reproduction_number_r0(average_contact_rate_per_agent=14.0, transmission_probability_per_interaction=0.12, average_active_duration_days=3.0)
print(f"Epidemic Dynamics: R0={r0['basic_reproduction_number_r0']} ({r0['viral_regime']})")

# 2. Granovetter Threshold Cascade
nodes = [
    {"id": "agent_0", "adoption_threshold": 0.0}, # Seed
    {"id": "agent_1", "adoption_threshold": 0.3},
    {"id": "agent_2", "adoption_threshold": 0.4},
    {"id": "agent_3", "adoption_threshold": 0.5},
    {"id": "agent_4", "adoption_threshold": 0.8}
]
edges = [
    {"source": "agent_0", "target": "agent_1", "influence_weight": 0.35},
    {"source": "agent_1", "target": "agent_2", "influence_weight": 0.45},
    {"source": "agent_2", "target": "agent_3", "influence_weight": 0.55},
    {"source": "agent_3", "target": "agent_4", "influence_weight": 0.60}
]

cascade = social.simulate_granovetter_linear_threshold_cascade(nodes, edges, seed_node_ids=["agent_0"])
print()
print(f"Viral Cascade: Final Adoption={cascade['final_adoption_percentage']}% ({cascade['final_active_nodes_count']}/{cascade['total_nodes']} nodes in {cascade['rounds_to_equilibrium']} rounds)")
for h in cascade['cascade_history']:
    print(f"  Round {h['round']}: +{h['newly_activated_count']} nodes (Cumulative: {h['cumulative_active_count']}, {h['adoption_rate_pct']}%)")

# 3. Greedy Influential Seed Selection
seeds = social.select_influential_seed_nodes_greedy(nodes, edges, target_seed_k=2)
print()
print(f"Greedy Seed Nodes: {seeds['selected_seed_nodes']}")
