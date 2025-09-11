# ailogx/tracebuilder.py

from collections import defaultdict
import networkx as nx

def build_causal_graph(logs):
    """
    Constructs a directed graph from structured logs where nodes represent log events
    and edges represent causal flow within the same trace ID.
    """
    G = nx.DiGraph()

    # Build nodes
    for log in logs:
        trace_id = log.get("trace_id", "")
        context_id = log.get("context_id", "")
        log_id = f"{trace_id}::{context_id}::{log.get('timestamp')}"
        G.add_node(log_id, **log)

    # Group logs by trace_id
    logs_by_trace = defaultdict(list)
    for log in logs:
        trace_id = log.get("trace_id")
        if trace_id:
            logs_by_trace[trace_id].append(log)

    # Create edges based on timestamp order within the same trace
    for trace_id, entries in logs_by_trace.items():
        entries.sort(key=lambda x: x.get("timestamp"))
        for i in range(len(entries) - 1):
            from_log = entries[i]
            to_log = entries[i + 1]
            from_id = f"{trace_id}::{from_log.get('context_id')}::{from_log.get('timestamp')}"
            to_id = f"{trace_id}::{to_log.get('context_id')}::{to_log.get('timestamp')}"
            G.add_edge(from_id, to_id)

    return G

def trace_aware_grouping(logs):
    """
    Groups logs into causally connected chains for downstream analysis or repair.
    Returns a list of list-of-logs.
    """
    G = build_causal_graph(logs)
    chains = list(nx.weakly_connected_components(G))

    grouped_logs = []
    for chain in chains:
        sublogs = [G.nodes[node] for node in chain]
        sublogs.sort(key=lambda x: x.get("timestamp"))
        grouped_logs.append(sublogs)

    return grouped_logs
