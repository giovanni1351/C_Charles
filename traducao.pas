program charles;
var
    x: real;
    a: integer;
    i: integer;
    valor2: real;
    valor: integer;
    teste: string;

begin
teste:='teste';
valor:= ((3+4)+2)*3;
valor2:= 0.23;

writeln(valor);

writeln(valor2);

writeln(teste);
x:= 0;
 while x<10 do 
begin

writeln(x);
if x<2 then 
begin

writeln('x eh menor que 2');

end
;
x:=x+0.2;

end
;
if x<2 then 
begin

writeln('x eh menor que 2');

end
else
begin

writeln('Valor do a:');

writeln(a);
if a<5 then 
begin

writeln('a é menor que 5');

end
else
begin

writeln('a é maior que 5');

end
;

writeln('x é maior que 2');

end
;
i:= 0;
while i <> 10 do
 
begin

writeln(i);
i:=i+1;

end
;

end
.


