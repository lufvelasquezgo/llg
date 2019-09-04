module external_fields
    implicit none
    real*8, parameter :: kB = 1.38064852e-29

contains
    function thermal_field(random_normal_matrix, num_sites, damping, temperature, gyromagnetic, deltat, magnitude_spin_moment)
        implicit none
        integer, intent(in) :: num_sites
        real*8, dimension(0:(num_sites - 1), 0:2) :: random_normal_matrix
        real*8, intent(in) :: damping
        real*8, intent(in):: temperature
        real*8, intent(in) :: gyromagnetic
        real*8, intent(in) :: magnitude_spin_moment
        integer, intent(in) :: deltat

        real*8, dimension(0:(num_sites - 1), 0:2) :: thermal_field
        
        thermal_field = random_normal_matrix &
                                 * sqrt((2.d0 * kB * temperature * damping) &
                                 / (gyromagnetic * deltat * magnitude_spin_moment)) 
                                    
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