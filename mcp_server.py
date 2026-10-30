# -*- coding: utf-8 -*-
"""
GenPark Agent Social MCP Server
FastMCP standard interface for Granovetter cascade simulations, R0 estimation, and seed selection.
"""

import json
from typing import Dict, Any, List
from client import GenParkAgentSocial

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("genpark-agent-social")
except ImportError:
    class MockFastMCP:
        def __init__(self, name):
            self.name = name
        def tool(self):
            def decorator(f):
                return f
            return decorator
    mcp = MockFastMCP("genpark-agent-social")

social = GenParkAgentSocial()

@mcp.tool()
def simulate_granovetter_linear_threshold_cascade(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    seed_node_ids: List[str],
    max_rounds: int = 10
) -> str:
    """
    Simulates information cascade under Granovetter's Linear Threshold Model.
    """
    res = social.simulate_granovetter_linear_threshold_cascade(nodes, edges, seed_node_ids, max_rounds)
    return json.dumps(res, indent=2)

@mcp.tool()
def estimate_basic_reproduction_number_r0(
    average_contact_rate_per_agent: float = 12.0,
    transmission_probability_per_interaction: float = 0.15,
    average_active_duration_days: float = 2.5
) -> str:
    """
    Estimates epidemic basic reproduction number R0 in network interaction.
    """
    res = social.estimate_basic_reproduction_number_r0(average_contact_rate_per_agent, transmission_probability_per_interaction, average_active_duration_days)
    return json.dumps(res, indent=2)

@mcp.tool()
def select_influential_seed_nodes_greedy(
    nodes: List[Dict[str, Any]],
    edges: List[Dict[str, Any]],
    target_seed_k: int = 3
) -> str:
    """
    Greedy degree centrality heuristics for seed selection under influence maximization budget.
    """
    res = social.select_influential_seed_nodes_greedy(nodes, edges, target_seed_k)
    return json.dumps(res, indent=2)

def main():
    print("Testing Agent Social:")
    print(estimate_basic_reproduction_number_r0(10, 0.2, 2.0))

if __name__ == "__main__":
    main()
