program main
    use functions
    implicit none

    integer :: num_sites
    real*8, allocatable, dimension(:, :) :: state
    integer:: num_types
    integer, allocatable, dimension(:) :: types
    integer :: i

    num_sites = 10
    num_types = 2

    allocate(state(0:(num_sites - 1), 0:2))
    allocate(types(0:(num_sites - 1)))

    state = 0.d0

    do i = 0, num_sites - 1
        state(i, :) = (/ 0.d0, 0.d0, 1.d0 /)
        types(i) = 0
        if (mod(i, 2) == 0) then
            state(i, :) = (/ 0.d0, 0.d0, -1.d0 /)
            types(i) = 1
        end if
    end do

    write(*, *) "*********************"
    write(*, *) magnetization_by_type(num_sites, state, num_types, types)
    write(*, *) "*********************"
    
end program main