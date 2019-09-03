module external_fields
    implicit none
    real*8, parameter :: pi = 4 * atan(1.d0)
    real*8, parameter :: kB = 1.38064852e-29

contains
    function random_normal_matrix(num_sites)
        implicit none
        integer, intent(in) :: num_sites
        real*8, dimension(0:(num_sites - 1), 0:2) :: u1
        real*8, dimension(0:(num_sites - 1), 0:2) :: u2

        real*8, dimension(0:(num_sites - 1), 0:2) :: random_normal_matrix 

        call random_number(u1)
        call random_number(u2)

        random_normal_matrix = sqrt(-2.d0 * log(u1)) * cos(2.d0 * pi * u2)
        
    end function random_normal_matrix


    function thermal_external_field(num_sites, damping, temperature, gyromagnetic, deltat, magnitude_spin_moment)
        implicit none
        integer, intent(in) :: num_sites
        real*8, intent(in) :: damping
        real*8, intent(in):: temperature
        real*8, intent(in) :: gyromagnetic
        real*8, intent(in) :: magnitude_spin_moment
        integer, intent(in) :: deltat

        real*8, dimension(0:(num_sites - 1), 0:2) :: thermal_external_field
        
        thermal_external_field = random_normal_matrix(num_sites) &
                                 * sqrt((2.d0 * kB * temperature * damping) &
                                 / (gyromagnetic * deltat * magnitude_spin_moment)) 
                                    
    end function thermal_external_field


    function external_magnetic_spin_field(num_sites, intensities, directions)
        implicit none
        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1)) :: intensities
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: directions
        real*8, dimension(0:(num_sites - 1), 0:2) :: external_magnetic_spin_field

        integer :: i
        do i = 0, num_sites - 1
            external_magnetic_spin_field(i, :) = intensities(i) * directions(i, :)
        end do
        
    end function external_magnetic_spin_field

end module external_fields