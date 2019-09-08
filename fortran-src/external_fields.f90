module external_fields
    implicit none

contains
    function thermal_field(num_sites, random_normal_matrix, temperature, magnitude_spin_moment, damping, deltat, gyromagnetic, kB)
        implicit none
        integer, intent(in) :: num_sites
        real*8, dimension(0:(num_sites - 1), 0:2) :: random_normal_matrix
        real*8, dimension(0:(num_sites - 1)) :: temperature
        real*8, dimension(0:(num_sites - 1)) :: magnitude_spin_moment
        real*8, intent(in) :: damping
        real*8, intent(in) :: deltat
        real*8, intent(in) :: gyromagnetic
        real*8, intent(in) :: kB

        real*8, dimension(0:(num_sites - 1), 0:2) :: thermal_field

        integer :: i

        do i = 0, num_sites - 1
            thermal_field(i, :) = random_normal_matrix(i, :) &
                        * sqrt((2.d0 * kB * temperature(i) * damping) &
                        / (gyromagnetic * deltat * magnitude_spin_moment(i))) 
        end do
                                    
    end function thermal_field


    function magnetic_field(num_sites, intensities, directions)
        implicit none
        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1)) :: intensities
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: directions
        real*8, dimension(0:(num_sites - 1), 0:2) :: magnetic_field

        integer :: i
        do i = 0, num_sites - 1
            magnetic_field(i, :) = intensities(i) * directions(i, :)
        end do
        
    end function magnetic_field

end module external_fields