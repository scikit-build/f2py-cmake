/* C routine called from Fortran, exposed under a fixed name for bind(C).
   Lives in a separate library to mirror issue #20 (Fortran calling into C). */
double add_in_c(double a, double b) {
  return a + b;
}
