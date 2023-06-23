function [h, grads, Hash] = solar_penalized_objective(z, H0)
% Evaluates the unconstrained objective for problem 10 in the solar % black-box
% optimization benchmark framework (https://github.com/bbopt/solar)
%    y = 1E-6 f + 0.5 ( (c1+)^2 + (2E-6 c2+)^2 + (c3+)^2 + (c4+)^2 + (c5+)^2 + (c6+)^2 )
% with f, c1, c2, ..., c6 as intermediate outputs and cj+ = max{0,cj} j=1,2,...,6

% Inputs:
%  z:              [1 x p]   point where we are evaluating h
%  H0: (optional)  [1 x l cell of strings]  set of hashes where to evaluate z

% Outputs:
%  h: [dbl]                       function value
%  grads: [p x l]                 gradients of each of the l manifolds active at z
%  Hash: [1 x l cell of strings]  set of hashes for each of the l manifolds active at z (in the same order as the elements of grads)

z = z(:);
p = length(z);
eqtol = 1e-4;

coeffs = [1e-6 0.5 1e-6 0.5 0.5 0.5 0.5];

if nargin == 1
    zk = z;
    zk(2:p) = max(zk(2:p), 0).^2;
    h = dot(coeffs, zk);

    zero_inds = 1 + find(zk(2:end) < eqtol);
    active_inds = 1 + find(zk(2:end) >= eqtol);

    fun_inds = intersect(zero_inds, active_inds);

    if ~isempty(fun_inds)
        error('a');
    end

    g = cell(p, 1);
    H = cell(p, 1);

    g{1}(1) = 0; % gradient of first component is zero
    H{1}(1) = {'0'}; % Hash of first component is zero

    for i = 2:p
        lg = 0;
        if ismember(i, active_inds)
            lg = lg + 1;
            g{i}(lg) = 2 * coeffs(i) * z(i);
            H{i}(lg) = {'1'};
        end
        if ismember(i, zero_inds)
            lg = lg + 1;
            g{i}(lg) = 0;
            H{i}(lg) = {'0'};
        end
    end

    grads = allcomb(g{:})';  % Can get this here: https://www.mathworks.com/matlabcentral/fileexchange/10064-allcomb-varargin-
    hashes_as_mat = cell2mat(allcomb(H{:}));
    b = size(hashes_as_mat, 1);
    Hash = cell(1, b);
    for i = 1:b
        Hash{i} = hashes_as_mat(i, :);
    end

elseif nargin == 2
    J = length(H0);
    h = zeros(1, J);
    grads = zeros(p, J);
    vals = zeros(p, J);

    for j = 1:J
        vals(1, j) = coeffs(1) * z(1);
        for i = 2:p
            switch H0{j}(i)
                case '0'
                    vals(i, j) = 0;
                    grads(i, j) = 0;
                case '1'
%                     assert(z(i)> 0, "why not?")
                    vals(i, j) = coeffs(i) * z(i)^2;
                    grads(i, j) = 2 * coeffs(i) * z(i);
            end
        end
        h(j) = sum(vals(:, j));
    end

else
    error('Too many inputs to function');
end
