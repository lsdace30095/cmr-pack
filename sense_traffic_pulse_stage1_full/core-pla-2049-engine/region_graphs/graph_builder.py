import numpy as np

class RegionGraphBuilder:
    """Builds an adjacency graph of coherent regions based on spatial proximity."""

    def build_graph(self, regions, distance_threshold=50):
        graph = {}
        for i, r1 in enumerate(regions):
            graph[i] = []
            for j, r2 in enumerate(regions):
                if i == j:
                    continue
                if self._close(r1, r2, distance_threshold):
                    graph[i].append(j)
        return graph

    def _close(self, r1, r2, threshold):
        (x1, y1), _ = r1['vectors'][0]
        (x2, y2), _ = r2['vectors'][0]
        return np.sqrt((x1-x2)**2 + (y1-y2)**2) < threshold
