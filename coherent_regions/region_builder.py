import numpy as np

class RegionBuilder:
    """Builds coherent motion regions from aggregated vectors."""

    def build_regions(self, aggregated_vectors, angle_threshold=np.pi/8):
        regions = []
        for anchor, vec in aggregated_vectors:
            added = False
            for region in regions:
                if self._is_similar_direction(region['direction'], vec, angle_threshold):
                    region['vectors'].append((anchor, vec))
                    added = True
                    break
            if not added:
                regions.append({'direction': vec, 'vectors': [(anchor, vec)]})
        return regions

    def _is_similar_direction(self, vec1, vec2, threshold):
        ang1 = np.arctan2(vec1[1], vec1[0])
        ang2 = np.arctan2(vec2[1], vec2[0])
        return abs(ang1 - ang2) < threshold
