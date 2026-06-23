module kinds
  implicit none
  integer, parameter :: dp = kind(1.0d0)
contains
  subroutine scale_dp(x, y)
    real(kind=dp), intent(in) :: x
    real(kind=dp), intent(out) :: y
    y = 2.0_dp * x
  end subroutine scale_dp
end module kinds
