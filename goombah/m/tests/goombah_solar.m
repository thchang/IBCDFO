root_dir = '../../../';
trsp_root = [root_dir 'goombah/m/subproblems/'];
addpath(trsp_root);
addpath('../../../manifold_sampling/m/h_examples/');
addpath('../');
addpath('../../../pounders/m/');
addpath('../../../manifold_sampling/m/tests/');
addpath('../../../manifold_sampling/m/');

mkdir('../benchmark_results');

x0s = load('x0_LH30.txt');

hfun = @solar_penalized_objective;
Ffun = @call_solar_from_matlab;
LB = [793.0,  2.0,  2.0, 0.01, 0.01];
UB = [995.0, 50.0, 30.0, 5.00, 5.00];
nfmax = 500;
subprob_switch = 'linprog';

GAMS_options.file = [trsp_root 'minimize_solar_penalized_objective.gms'];
GAMS_options.solvers = 1;

for i = 1:30
    filename = ['../benchmark_results/prob=' int2str(i) '.mat'];

    if exist(filename, 'file')
        continue
    end
    system(['touch ' filename]);

    x0 = x0s(i,:);

    [X, F, h, xkin] = goombah(hfun, Ffun, nfmax, x0, LB, UB, GAMS_options, subprob_switch);

    save(filename, "X", "F", "h")
end
