module Energy
    implicit none

contains
    function exchange_energy(num_sites, num_interactions, state, &
        j_exchange, num_neighbors, neighbors)
        implicit none
        integer, intent(in) :: num_sites
        integer, intent(in) :: num_interactions
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: state
        real*8, intent(in), dimension(0:(num_interactions - 1)) :: j_exchange
        integer, intent(in), dimension(0:(num_sites - 1)) :: num_neighbors
        integer, intent(in), dimension(0:(num_interactions - 1)) :: neighbors

        real*8, dimension(0:(num_sites - 1), 0:2) :: exchange_energy

        integer :: i, j
        integer :: start, end
        integer :: nhb
        
        exchange_energy = 0.d0
        do i = 0, num_sites - 1
            start = sum(num_neighbors(0:i)) - num_neighbors(0)
            end = start + num_neighbors(i) - 1

            do j = start, end
                nhb = neighbors(j)
                exchange_energy(i, :) = exchange_energy(i, :) - &
                    j_exchange(i) * dot_product(state(i, :), state(nhb, :)) 
            end do
        end do

        exchange_energy = 0.5 * exchange_energy

    end function exchange_energy


    function anisotropy_energy(num_sites, state, &
        anisotropy_constant, anisotropy_vector)
        implicit none
        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: state
        real*8, intent(in), dimension(0:(num_sites - 1)) :: anisotropy_constant
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: anisotropy_vector

        real*8, dimension(0:(num_sites - 1), 0:2) :: anisotropy_energy

        integer :: i

        anisotropy_energy = 0.d0
        do i = 0, num_sites - 1
            anisotropy_energy(i, :) = anisotropy_energy(i, :) - &
                anisotropy_constant(i) * &
                dot_product(state(i, :), anisotropy_vector(i, :)) ** 2
        end do
        
    end function anisotropy_energy


    function magnetic_field(num_sites, magnitude_spin_moment, state, intensities, directions)
        implicit none
        integer, intent(in) :: num_sites
        real*8, dimension(0:(num_sites - 1)) :: magnitude_spin_moment
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: state
        real*8, intent(in), dimension(0:(num_sites - 1)) :: intensities
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: directions
        real*8, dimension(0:(num_sites - 1), 0:2) :: magnetic_field
        integer :: i

        magnetic_field = 0.d0
        do i = 0, num_sites - 1
            magnetic_field(i, :) = magnetic_field(i, :) - &
                magnitude_spin_moment(i) * &
                dot_product(state(i, :), directions(i, :)) * intensities(i)
        end do
        
    end function magnetic_field

end module Energy
