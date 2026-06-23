subroutine keep_me(a)
   real*8, intent(out) :: a
   a = 1.0d0
end subroutine keep_me

subroutine drop_me(a)
   real*8, intent(out) :: a
   a = 2.0d0
end subroutine drop_me
