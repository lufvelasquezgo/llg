from numba import jit


@jit(nopython=True)
def compute_exchange_energy(
    state,
    exchanges,
    neighbors,
) -> float:
    total = 0
    N = len(state)
    for i in range(N):
        state_i = state[i]
        exchanges_i = exchanges[i]
        neighbors_i = state[neighbors[i]]
        total -= (exchanges_i * (state_i * neighbors_i).sum(axis=1)).sum()
    return 0.5 * total


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
