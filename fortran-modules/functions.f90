module functions

    contains
        function total_magnetization(num_sites, state)
            implicit none

            integer, intent(in) :: num_sites
            real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: state
            real*8, dimension(0:2) :: mag
            real*8 :: total_magnetization

            mag = sum(state, dim=1) / num_sites
            total_magnetization = sum(mag * mag) ** 0.5

        end function total_magnetization

    function magnetization_by_type(num_sites, state, num_types, types)
        implicit none

        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: state
        integer, intent(in) :: num_types
        integer, intent(in), dimension(0:(num_sites - 1)) :: types

        real*8, dimension(0:(num_types - 1), 0:2) :: mag_by_type
        integer, dimension(0:(num_types - 1)) :: amount_type
        integer :: i

        real*8, dimension(0:(num_types - 1)) :: magnetization_by_type
        
        mag_by_type = 0.0d0
        amount_type = 0

        do i = 0, num_sites - 1
            mag_by_type(types(i), :) = mag_by_type(types(i), :) + state(i, :)
            amount_type(types(i)) = amount_type(types(i)) + 1
        end do

        do i = 0, num_types - 1
            mag_by_type(i, :) = mag_by_type(i, :) / amount_type(i)
        end do

        do i = 0, num_types - 1
            magnetization_by_type(i) = sum(mag_by_type(i, :) * mag_by_type(i, :)) ** 0.5
        end do
        
    end function magnetization_by_type

end module functions