# -*- coding: utf-8 -*-
"""
GenPark Agent Social Client
Pure Python Standard Library (Zero External Dependencies)
Implements social network viral cascade propagation (Granovetter Linear Threshold Model),
epidemic basic reproduction number (R0) estimation, and greedy influence maximization seed selection.
"""

import math
from typing import Dict, Any, List, Optional, Set

class GenParkAgentSocial:
    """
    Autonomous multi-agent social network dynamics and viral cascade simulation engine.
    """

    def __init__(self):
        pass

    def simulate_granovetter_linear_threshold_cascade(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        seed_node_ids: List[str],
        max_rounds: int = 10
    ) -> Dict[str, Any]:
        """
        Simulates information cascade under Granovetter's Linear Threshold Model:
          A node v activates if sum( weight(u, v) for active neighbors u ) >= threshold(v).
        """
        thresholds = {n["id"]: float(n.get("adoption_threshold", 0.5)) for n in nodes}
        active_nodes: Set[str] = set(seed_node_ids)

        # Build in-neighbor weights: v -> [(u, weight)]
        in_neighbors = {n["id"]: [] for n in nodes}
        for e in edges:
            u = e["source"]
            v = e["target"]
            w = float(e.get("influence_weight", 0.2))
            if v in in_neighbors:
                in_neighbors[v].append((u, w))

        cascade_progression = [{
            "round": 0,
            "newly_activated_count": len(active_nodes),
            "cumulative_active_count": len(active_nodes),
            "adoption_rate_pct": round(len(active_nodes) / max(1, len(nodes)) * 100.0, 1)
        }]

        for r in range(1, max_rounds + 1):
            newly_activated = set()
            for v, threshold in thresholds.items():
                if v not in active_nodes:
                    # Calculate cumulative influence from active neighbors
                    total_influence = sum(w for u, w in in_neighbors[v] if u in active_nodes)
                    if total_influence >= threshold:
                        newly_activated.add(v)

            if not newly_activated:
                break

            active_nodes.update(newly_activated)
            cascade_progression.append({
                "round": r,
                "newly_activated_count": len(newly_activated),
                "cumulative_active_count": len(active_nodes),
                "adoption_rate_pct": round(len(active_nodes) / max(1, len(nodes)) * 100.0, 1)
            })

        total_nodes = len(nodes)
        final_adoption = len(active_nodes)
        cascade_complete = final_adoption == total_nodes

        return {
            "total_nodes": total_nodes,
            "seed_nodes_count": len(seed_node_ids),
            "final_active_nodes_count": final_adoption,
            "final_adoption_percentage": round(final_adoption / max(1, total_nodes) * 100.0, 1),
            "viral_tipping_point_achieved": final_adoption >= total_nodes * 0.5,
            "rounds_to_equilibrium": len(cascade_progression) - 1,
            "cascade_history": cascade_progression
        }

    def estimate_basic_reproduction_number_r0(
        self,
        average_contact_rate_per_agent: float = 12.0,
        transmission_probability_per_interaction: float = 0.15,
        average_active_duration_days: float = 2.5
    ) -> Dict[str, Any]:
        """
        Estimates epidemic basic reproduction number R0 in network interaction:
          R0 = beta * c * d
        Where beta is transmission probability, c is contact rate, d is infectious duration.
        """
        r0 = average_contact_rate_per_agent * transmission_probability_per_interaction * average_active_duration_days
        r0 = round(r0, 3)

        if r0 > 1.0:
            regime = "SUPER_EXPONENTIAL_VIRAL_SPREAD"
        elif r0 == 1.0:
            regime = "ENDEMIC_STABLE_PROPAGATION"
        else:
            regime = "SUB_CRITICAL_DECAY"

        return {
            "basic_reproduction_number_r0": r0,
            "viral_regime": regime,
            "epidemic_threshold_exceeded": r0 > 1.0,
            "effective_transmission_rate": round(average_contact_rate_per_agent * transmission_probability_per_interaction, 3)
        }

    def select_influential_seed_nodes_greedy(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        target_seed_k: int = 3
    ) -> Dict[str, Any]:
        """
        Greedy degree centrality heuristics for seed selection under influence maximization budget.
        """
        out_degrees = {n["id"]: 0.0 for n in nodes}
        for e in edges:
            u = e["source"]
            w = float(e.get("influence_weight", 1.0))
            if u in out_degrees:
                out_degrees[u] += w

        sorted_nodes = sorted(out_degrees.items(), key=lambda kv: kv[1], reverse=True)
        top_k = sorted_nodes[:max(1, target_seed_k)]

        return {
            "target_k": target_seed_k,
            "selected_seed_nodes": [node_id for node_id, _ in top_k],
            "seed_influence_scores": [{"node_id": k, "out_degree_weight": round(v, 2)} for k, v in top_k]
        }
