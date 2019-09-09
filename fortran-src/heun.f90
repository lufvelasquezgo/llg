module heun
    use external_fields
    use spin_fields
    
contains
    function cross(num_sites, A, B)
        implicit none
        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: A
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: B
        real*8, dimension(0:(num_sites - 1), 0:2) :: cross
        cross(:, 0) = A(:, 1) * B(:, 2) - A(:, 2) * B(:, 1)
        cross(:, 1) = A(:, 2) * B(:, 0) - A(:, 0) * B(:, 2)
        cross(:, 2) = A(:, 0) * B(:, 1) - A(:, 1) * B(:, 0)
    end function cross

    function dS_llg(num_sites, state, Heff, damping, gyromagnetic)
        implicit none
        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: state
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: Heff
        real*8, intent(in) :: damping
        real*8, intent(in) :: gyromagnetic

        real*8, dimension(0:(num_sites - 1), 0:2) :: dS_llg
        
        real*8, dimension(0:(num_sites - 1), 0:2) :: cross1, cross2
        real*8 :: alpha

        alpha = - gyromagnetic / (1.d0 + damping * damping)

        cross1 = cross(num_sites, state, Heff)
        cross2 = cross(num_sites, state, cross1)

        dS_llg = alpha * (cross1 + damping * cross2)
    end function dS_llg

    function normalize(num_sites, matrix)
        implicit none
        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: matrix
        
        real*8, dimension(0:(num_sites - 1), 0:2) :: normalize
        
        real*8, dimension(0:(num_sites - 1)) :: norms

        norms = sqrt(sum(matrix * matrix, dim=2))
        normalize(:, 0) = matrix(:, 0) / norms
        normalize(:, 1) = matrix(:, 1) / norms
        normalize(:, 2) = matrix(:, 2) / norms
    end function normalize

    function integrate(num_sites, state, magnitude_spin_moment, &
        random_normal_matrix, temperature, damping, deltat, gyromagnetic, &
        kB, field_intensities, field_directions, num_interactions, j_exchange, &
        num_neighbors, neighbors, anisotropy_constant, anisotropy_vector)
        implicit none
        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: state
        real*8, intent(in), dimension(0:(num_sites - 1)) :: magnitude_spin_moment
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: random_normal_matrix
        real*8, intent(in), dimension(0:(num_sites - 1)) :: temperature
        real*8, intent(in) :: damping
        real*8, intent(in) :: deltat
        real*8, intent(in) :: gyromagnetic
        real*8, intent(in) :: kB
        real*8, intent(in), dimension(0:(num_sites - 1)) :: field_intensities
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: field_directions
        integer, intent(in) :: num_interactions
        real*8, intent(in), dimension(0:(num_interactions - 1)) :: j_exchange
        integer, intent(in), dimension(0:(num_sites - 1)) :: num_neighbors
        integer, intent(in), dimension(0:(num_interactions - 1)) :: neighbors
        real*8, intent(in), dimension(0:(num_sites - 1)) :: anisotropy_constant
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: anisotropy_vector
        
        real*8, dimension(0:(num_sites - 1), 0:2) :: integrate
        
        real*8, dimension(0:(num_sites - 1), 0:2) :: Hext, Heff, Heff_prime
        real*8, dimension(0:(num_sites - 1), 0:2) :: state_prime, dS, dS_prime
        
        ! compute external fields. These fields does not change
        ! because they don't depend on the state
        Hext = thermal_field(num_sites, random_normal_matrix, temperature, &
            magnitude_spin_moment, damping, deltat, gyromagnetic, kB)
        Hext = Hext + magnetic_field(num_sites, field_intensities, field_directions)

        ! predictor step

        ! compute the effective field as the sum of external fields and
        ! spin fields
        Heff = Hext + exchange_interaction_field(num_sites, state, &
            magnitude_spin_moment, num_interactions, j_exchange, &
            num_neighbors, neighbors)
        Heff = Heff + anisotropy_interaction_field(num_sites, state, &
            magnitude_spin_moment, anisotropy_constant, anisotropy_vector)
        
        ! compute dS based on the LLG equation
        dS = dS_llg(num_sites, state, Heff, damping, gyromagnetic)
        
        ! compute the state_prime
        state_prime = state + deltat * dS
        
        ! normalize state_prime
        state_prime = normalize(num_sites, state_prime)
        
        ! corrector step

        ! compute the effective field prime by using the state_prime. We
        ! use the Heff variable for this in order to reutilize the memory.
        Heff = Hext + exchange_interaction_field(num_sites, state_prime, &
        magnitude_spin_moment, num_interactions, j_exchange, &
            num_neighbors, neighbors)
        Heff = Heff + anisotropy_interaction_field(num_sites, state_prime, &
        magnitude_spin_moment, anisotropy_constant, anisotropy_vector)
        
        ! compute dS_prime employing the Heff prime and the state_prime
        dS_prime = dS_llg(num_sites, state_prime, Heff, damping, gyromagnetic)
        
        ! compute the new state
        integrate = state + 0.d5 * (dS + dS_prime) * deltat
        
        ! normalize the new state
        integrate = normalize(num_sites, integrate)
    end function integrate
    
end module heun