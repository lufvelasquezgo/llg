module spin_fields
    implicit none
    
contains
    function exchange_interaction_field(num_sites, state, num_interactions, j_exchange, num_neighbors, neighbors)
        implicit none
        integer, intent(in) :: num_sites
        real*8, intent(in), dimension(0:(num_sites - 1), 0:2) :: state
        integer, intent(in) :: num_interactions
        real*8, intent(in), dimension(0:(num_interactions - 1)) :: j_exchange
        integer, intent(in), dimension(0:(num_sites - 1)) :: num_neighbors
        integer, intent(in), dimension(0:(num_interactions - 1)) :: neighbors
        
        real*8, dimension(0:(num_sites - 1), 0:2) :: exchange_interaction_field

        integer :: i, j
        integer :: nbh
        integer :: start, final

        exchange_interaction_field = 0.d0
        do i = 0, num_sites - 1
            start = sum(num_neighbors(0:i)) - num_neighbors(0)
            final = start + num_neighbors(i) - 1

            do j = start, final
                nbh = neighbors(j)
                exchange_interaction_field(i, :) = exchange_interaction_field(i, :) + j_exchange(nbh) * state(nbh, :)
            end do
        end do

        
    end function exchange_interaction_field
    
end module spin_fields