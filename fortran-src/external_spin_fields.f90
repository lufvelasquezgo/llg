module external_fields
    implicit none
    
contains
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