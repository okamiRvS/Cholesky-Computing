% read the matrix
[A, rows, col, entries] = mmread('/Users/king/git/cholesky-computing/data/ex15.mtx');

% memory calculation after loading the matrix
%initial = memory;
%initial_memory = initial.MemUsedMATLAB;

% find b for x to be [1, 1, ..., 1]
xe = ones(1, col);
b = A * xe';

% tic-toc command used to compute the calculation time of x
tic

% Cholewski decomposition
R = chol(A);
x = R\(R'\b);

time = toc;

% memory calculation after Cholewski decomposition
%final = memory;
%final_memory = final.MemUsedMATLAB;

% memory needeed to solve the system
%system_memory = final_memory - initial_memory;

% relative error
error = norm(x - xe')/norm(xe');

% Graphic
%semilogx(x, y);


