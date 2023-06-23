function F = call_solar_from_matlab(x)

system('rm vecout.out');
str = ['python3 solar_command_line.py ', num2str(x,'%16.16f ')];
% disp(str)
system(str);    
F = load('vecout.out')';
assert(all(size(F) == [1 7]), "F is not the correct size")
