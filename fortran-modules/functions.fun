test_suite functions

! Global variables can be declared here


setup
    ! Place code here that should run before each test
end setup

teardown
    ! This code runs immediately after each test
end teardown

test total_magnetization_FM_state
    integer :: num_sites
    real*8, allocatable, dimension(:, :)  :: state
    integer :: i

    num_sites = 100
    allocate(state(0:(num_sites - 1), 0:2))
    state = 0.d0
    do i = 0, num_sites - 1
        state(i, :) = (/ 0.0, 0.0, 1.0 /)
    end do

    assert_real_equal(total_magnetization(num_sites, state), 1.0e0)
end test

test total_magnetization_AFM_state
    integer :: num_sites
    real*8, allocatable, dimension(:, :)  :: state
    integer :: i

    num_sites = 100
    allocate(state(0:(num_sites - 1), 0:2))
    state = 0.d0
    do i = 0, num_sites - 1
        state(i, :) = (/ 0.0, 0.0, 1.0 /)
        if (mod(i, 2) == 0) then
            state(i, :) = (/ 0.0, 0.0, -1.0 /)
        end if
    end do

    assert_real_equal(total_magnetization(num_sites, state), 0.0e0)
end test

end test_suite
