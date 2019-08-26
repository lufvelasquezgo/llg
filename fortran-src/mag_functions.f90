module mag_functions
    implicit none

contains
    function magnetization_vector(num_sites, state)
        implicit none
        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: state
        real*8, dimension(0:2) :: magnetization_vector

        magnetization_vector = sum(state, dim=1) / num_sites
    end function magnetization_vector


    function magnetization_vector_by_type(num_sites, state, num_types, types)
        implicit none
        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: state
        integer, intent(in) :: num_types
        integer, intent(in), dimension(0:(num_sites - 1)) :: types
        real*8, dimension(0:(num_types - 1), 0:2) :: magnetization_vector_by_type
        integer :: i

        magnetization_vector_by_type = 0.d0
        do i = 0, num_sites - 1
            magnetization_vector_by_type(types(i), :) = magnetization_vector_by_type(types(i), :) + state(i, :)
        end do

        do i = 0, num_types - 1
            magnetization_vector_by_type(i, :) = magnetization_vector_by_type(i, :) / count(types==i)
        end do
    end function magnetization_vector_by_type


    function total_magnetization(num_sites, state)
        implicit none

        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: state
        real*8, dimension(0:2) :: mag
        real*8 :: total_magnetization

        mag = magnetization_vector(num_sites, state)
        total_magnetization = sqrt(sum(mag * mag))
    end function total_magnetization


    function magnetization_by_type(num_sites, state, num_types, types)
        implicit none

        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: state
        integer, intent(in) :: num_types
        integer, intent(in), dimension(0:(num_sites - 1)) :: types

        real*8, dimension(0:(num_types - 1), 0:2) :: mag_by_type
        integer :: i

        real*8, dimension(0:(num_types - 1)) :: magnetization_by_type
        
        mag_by_type = magnetization_vector_by_type(num_sites, state, num_types, types)

        do i = 0, num_types - 1
            magnetization_by_type(i) = sqrt(sum(mag_by_type(i, :) * mag_by_type(i, :)))
        end do
    end function magnetization_by_type

end module mag_functions