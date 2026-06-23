subroutine keep_me(a)
   real*8, intent(out) :: a
   call compute(a)
end subroutine keep_me

subroutine drop_me(a)
   real*8, intent(out) :: a
   a = 2.0d0
end subroutine drop_me
