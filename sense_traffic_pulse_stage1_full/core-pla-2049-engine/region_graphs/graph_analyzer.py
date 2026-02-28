class RegionGraphAnalyzer:
    """Analyzes region adjacency graphs for flow patterns and anomalies."""

    def dominant_flows(self, graph):
        return sorted(graph.items(), key=lambda x: len(x[1]), reverse=True)

    def isolated_regions(self, graph):
        return [node for node, edges in graph.items() if len(edges) == 0]
