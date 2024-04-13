def int test(int a, int b, int c, int d)
	while((a>b) and (c>d)) do
		print a;
		a = a+1
	od;
	if (a>b) then
		print a
	else
		print b 
	fi;
	return a
fed;

int a,b,c,d;
a = 2;
b = a * 2 -3;
c = b/a + 1;
d = test(a, b, c, d);
print(d).