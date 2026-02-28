def test_vector_field():
    import numpy as np
    from core_pla_2049_engine.vector_processing.vector_field import VectorField
    vf = VectorField(np.zeros((10,10,2)))
    assert vf.magnitude().shape == (10,10)
