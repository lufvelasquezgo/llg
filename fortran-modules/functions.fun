test_suite functions

! Global variables can be declared here


setup
    ! Place code here that should run before each test
end setup

teardown
    ! This code runs immediately after each test
end teardown

test magnetization_vector_function
    integer :: num_sites
    real*8, allocatable, dimension(:, :) :: state
    real*8, dimension(0:2) :: mag
    real*8, dimension(0:2) :: val
    integer :: i

    num_sites = 100
    allocate(state(0:(num_sites - 1), 0:2))
    state = 0.d0
    do i = 0, num_sites - 1
        state(i, :) = (/ 0.d0, 0.d0, 1.d0 /)
    end do

    mag = magnetization_vector(num_sites, state)
    val = (/ 0.d0, 0.d0, 1.d0 /)

    assert_array_equal(mag,val)
end test

test magnetization_vector_by_type_function
    integer :: num_sites
    real*8, allocatable, dimension(:, :) :: state
    integer, allocatable, dimension(:) :: types
    real*8, dimension(0:1, 0:2) :: mag
    real*8, dimension(0:1, 0:2) :: val
    integer :: i

    num_sites = 100
    allocate(state(0:(num_sites - 1), 0:2))
    allocate(types(0:(num_sites - 1)))

    state = 0.d0
    types = 0

    do i = 0, num_sites - 1
        state(i, :) = (/ 0.d0, 0.d0, 1.d0 /)
        if ( mod(i, 2) == 0 ) then
            state(i, :) = (/ 0.d0, 0.d0, -1.d0 /)
            types(i) = 1
        end if
    end do

    mag = magnetization_vector_by_type(num_sites, state, 2, types)
    val(0, :) = (/ 0.d0, 0.d0, 1.d0 /)
    val(1, :) = (/ 0.d0, 0.d0, -1.d0 /)

    assert_array_equal(mag,val)
end test

test total_magnetization_FM_state
    integer :: num_sites
    real*8, allocatable, dimension(:, :) :: state
    integer :: i

    num_sites = 100
    allocate(state(0:(num_sites - 1), 0:2))
    state = 0.d0
    do i = 0, num_sites - 1
        state(i, :) = (/ 0.d0, 0.d0, 1.d0 /)
    end do

    assert_real_equal(total_magnetization(num_sites, state), 1.0e0)
end test

test total_magnetization_AFM_state
    integer :: num_sites
    real*8, allocatable, dimension(:, :) :: state
    integer :: i

    num_sites = 100
    allocate(state(0:(num_sites - 1), 0:2))
    state = 0.d0
    do i = 0, num_sites - 1
        state(i, :) = (/ 0.d0, 0.d0, 1.d0 /)
        if (mod(i, 2) == 0) then
            state(i, :) = (/ 0.0, 0.0, -1.0 /)
        end if
    end do

    assert_real_equal(total_magnetization(num_sites, state), 0.0e0)
end test

end test_suite
