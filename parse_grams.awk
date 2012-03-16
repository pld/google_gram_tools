#!/bin/awk -f
# Keep all entries where the second letter is one of t[1-4]
BEGIN {
  t1="ghetto";
  t2="Ghetto";
  t3="ghettos";
  t4="Ghettos";
}
{ 
  if ($2 == t1 || $2 == t2 || $2 == t3 || $2 == t4) {
    print $0;
  }
}
END {
}

