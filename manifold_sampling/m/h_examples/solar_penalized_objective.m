function [h, grads, Hash] = solar_penalized_objective(z, H0)
% Evaluates the unconstrained objective for problem 10 in the solar % black-box
% optimization benchmark framework (https://github.com/bbopt/solar)
%    y = 1E-6 f + 0.5 ( (c1+)^2 + (2E-6 c2+)^2 + (c3+)^2 + (c4+)^2 + (c5+)^2 + (c6+)^2 )
% with f, c1, c2, ..., c6 as intermediate outputs and cj+ = max{0,cj} j=1,2,...,6

% Since this problem is smooth, there is only one Hash, which we denote by '0'

% Inputs:
%  z:              [1 x p]   point where we are evaluating h
%  H0: (optional)  [1 x l cell of strings]  set of hashes where to evaluate z

% Outputs:
%  h: [dbl]                       function value
%  grads: [p x l]                 gradients of each of the l manifolds active at z
%  Hash: [1 x l cell of strings]  set of hashes for each of the l manifolds active at z (in the same order as the elements of grads)

z = z(:);
p = length(z);

% coeffs = [1e-6 0.5 2e-12 0.5 0.5 0.5 0.5]';
coeffs = ones(p, 1);

zk = z;
zk(2:p) = max(zk(2:p), 0).^2;
h = dot(coeffs, zk);

grads = 2 * coeffs .* zk;
grads(1) = 0; % gradient of first component is zero

if nargin == 1
    Hash = {'0'};
end
