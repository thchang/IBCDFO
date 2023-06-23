addpath('../h_examples/')
addpath('../')
addpath('../../../pounders/m/')
hfun = @solar_penalized_objective;
Ffun = @call_solar_from_matlab;
x0 = [900.0, 10.0, 12.0, 0.20, 0.20];
LB = [ 793.0,  2.0,  2.0, 0.01, 0.01 ];
UB = [ 995.0, 50.0, 30.0, 5.00, 5.00 ];
nfmax = 60;
subprob_switch = 'linprog';

[X, F, h, xkin, flag] = manifold_sampling_primal(hfun, Ffun, x0, LB, UB, nfmax, subprob_switch);
