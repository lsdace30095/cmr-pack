import numpy as np

class VectorAggregator:
    """Aggregates motion vectors to prepare for coherent region formation."""

    def aggregate(self, flow, grid_size=16):
        h, w, _ = flow.shape
        aggregated = []

        for y in range(0, h, grid_size):
            for x in range(0, w, grid_size):
                cell = flow[y:y+grid_size, x:x+grid_size]
                if cell.size == 0: 
                    continue
                avg_x = np.mean(cell[...,0])
                avg_y = np.mean(cell[...,1])
                aggregated.append(((x, y), (avg_x, avg_y)))

        return aggregated
