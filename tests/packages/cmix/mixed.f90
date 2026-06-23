! f2py-wrapped Fortran that calls a C routine from a separate library.
! Without the original source compiled into the module (or the C library
! linked), importing this fails with an undefined symbol (issue #20).
subroutine add_them(a, b, c)
  implicit none
  ! Plain double precision in the wrapped signature: older f2py maps the
  ! iso_c_binding c_double kind to C float, which silently corrupts results.
  double precision, intent(in) :: a, b
  double precision, intent(out) :: c
  interface
    function add_in_c(x, y) bind(c, name="add_in_c") result(r)
      use iso_c_binding, only: c_double
      real(c_double), value :: x, y
      real(c_double) :: r
    end function add_in_c
  end interface
  c = add_in_c(a, b)
end subroutine add_them
