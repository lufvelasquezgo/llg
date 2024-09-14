from numba import jit


def compute_exchange_energy(
    state,
    exchanges,
    neighbors,
) -> float:
    exchange_field = (
        exchanges.reshape(tuple((*exchanges.shape, 1))) * state[neighbors]
    ).sum(axis=1)
    return -0.5 * (exchange_field * state).sum()


@jit(nopython=True)
def compute_anisotropy_energy(
    state,
    anisotropy_constants,
    anisotropy_vectors,
) -> float:
    return -(anisotropy_constants * (state * anisotropy_vectors).sum(axis=1) ** 2).sum()


@jit(nopython=True)
def compute_magnetic_energy(
    state,
    magnitude_spin_moment,
    magnetic_fields,
) -> float:
    return -(magnitude_spin_moment * (state * magnetic_fields).sum(axis=1)).sum()
