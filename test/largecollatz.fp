0 @ ANS
0 @ ANSLEN
27 {
  : @ X
  1 @ N

  {
    # X 2 % 0 =
    : [ # X 2 / @ X ]
    ! [ # X 3 * 1 + @ X ]
    # N 1 + @ N
    # X 1 = !
  }

  # N # ANSLEN >
  [ 
    # N @ ANSLEN
    : @ ANS
  ]

  1 +
  : 1000000 <
}
# ANS ~
# ANSLEN ~
