project 1

Not - if in=0 then out=1 else out=0
And - if a=b=1 then out=1 else out=0
Or - if a=b=0 then out=0 else out=1
Xor -if a!=b then out=1 else out=0
Mux - if sel=0 then out=a else out=b
DMux - if sel=0 then {a=in, b=0} else {a=0, b=in}
Not16 -  for i=0..15: out[i] = not in[i]
And16 - for i = 0..15: out[i] = (a[i] and b[i])
Or16 -  for i = 0..15 out[i] = (a[i] or b[i])
Mux16 - for i = 0..15 out[i] = a[i] if sel == 0 
Or8Way - out = (in[0] or in[1] or ... or in[7])
Mux4Way16 - out = a if sel == 00, b if sel == 01, c if sel == 10, d if sel == 11
Mux8Way16 - out = a if sel == 000, b if sel == 001, etc. h if sel == 111
DMux4Way - {a, b, c, d} = {in, 0, 0, 0} if sel == 00, {0, in, 0, 0} if sel == 01, {0, 0, in, 0} if sel == 10, {0, 0, 0, in} if sel == 11
DMux8Way - {a, b, c, d, e, f, g, h} = {in, 0, 0, 0, 0, 0, 0, 0} if sel == 000, {0, in, 0, 0, 0, 0, 0, 0} if sel == 001, etc., {0, 0, 0, 0, 0, 0, 0, in} if sel == 111
