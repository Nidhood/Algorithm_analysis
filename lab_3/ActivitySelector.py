## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

import copy, math

## -------------------------------------------------------------------------
def Print( M ):
  print( "------------" )
  for j in range( len( M ) ):
    for i in range( len( M ) ):
      if M[ i ][ j ] != -math.inf:
        print( "X ", end = '' )
      else:
        print( "- ", end = '' )
      # end if
    # end for
    print( " " )
  # end for
  print( "------------" )
# end def

## -------------------------------------------------------------------------
def DynamicProgramming_Aux( A, i, j, M ):
  if M[ i ][ j ] == -math.inf:
    S = []
    for k in range( i, j + 1 ):
      if A[ k ][ 1 ] >= A[ i ][ 2 ] and A[ k ][ 2 ] <= A[ j ][ 1 ]:
        S.append( k )
      # end if
    # end for

    if len( S ) == 0:
      M[ i ][ j ] = 0
    else:
      q = -math.inf
      for k in S:
        v = 1 + DynamicProgramming_Aux( A, i, k, M )
        v = v + DynamicProgramming_Aux( A, k, j, M )
        if q < v:
          q = v
        # end if
      # end for
      M[ i ][ j ] = q
    # end if
  # end if
  return M[ i ][ j ]
# end def

## -------------------------------------------------------------------------
def DynamicProgramming( A ):
  C = sorted( A, key = lambda a: a[ 2 ] )
  C.insert( 0, [ "__not_valid__", -math.inf, 0 ] )
  C.append( [ "__not_valid__", C[ -1 ][ 2 ], math.inf ] )
  M = [ [ -math.inf for j in range( len( C ) ) ] for i in range( len( C ) ) ]
  return DynamicProgramming_Aux( C, 0, len( C ) - 1, M )
# end def

## -------------------------------------------------------------------------
def Greedy( A ):
  C = sorted( A, key = lambda a: a[ 2 ] )
  R = [ C[ 0 ] ]
  k = 0
  for m in range( 1, len( C ) ):
    if C[ m ][ 1 ] >= C[ k ][ 2 ]:
      R.append( C[ m ] )
      k = m
    # end if
  # end for
  return R
# end def

## eof - ActivitySelector.py
