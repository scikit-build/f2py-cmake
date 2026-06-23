! Linked into the extension but absent from the signature: keep_me calls it,
! yet it is never exposed to Python.
subroutine compute(a)
   real*8, intent(out) :: a
   a = 42.0d0
end subroutine compute
