root_dir = '../../../';
trsp_root = [root_dir 'goombah/m/subproblems/'];
addpath(trsp_root);
addpath('../../../manifold_sampling/m/h_examples/')
addpath('../')
addpath('../../../manifold_sampling/m/tests/')
addpath('../../../manifold_sampling/m/')


hfun = @solar_penalized_objective;
Ffun = @call_solar_from_matlab;
x0 = [900.0, 10.0, 12.0, 0.20, 0.20];
LB = [ 793.0,  2.0,  2.0, 0.01, 0.01 ];
UB = [ 995.0, 50.0, 30.0, 5.00, 5.00 ];
nfmax = 60;
subprob_switch = 'linprog';


GAMS_options.file = [trsp_root 'minimize_solar_penalized_objective.gms'];
GAMS_options.solvers = 1:3;

[X, F, h, xkin] = goombah(hfun, Ffun, nfmax, x0, LB, UB, GAMS_options, subprob_switch);
