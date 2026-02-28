def test_region_builder():
    from core_pla_2049_engine.coherent_regions.region_builder import RegionBuilder
    rb = RegionBuilder()
    regions = rb.build_regions([((0,0),(1.0,1.0))])
    assert len(regions) == 1
