directory = dir("../../data");

s = length(directory) - 2;

program = string(1:s)';
names = string(1:s)';
import = [1:s]';
rows = [1:s]';
cols = [1:s]';
nonZeros = [1:s]';
size = [1:s]';
chol_info = [1:s]';
chol_size = [1:s]';
sol_time = [1:s]';
err = [1:s]';

for i=3 : length(directory)
    name = directory(i).name;
    
    % read the matrix
    tic;
    [A, row, col, entries] = mmread("../../data/" + name);
    import_time = toc;
    info_A = whos('A');

    % find b for x to be [1, 1, ..., 1]
    xe = ones(1, col);
    b = A * xe';

    % Cholewski decomposition
    tic;
    R = chol(A);
    cholesky_time = toc;
    info_R = whos('R');

    % R = full(R);

    tic;
    x = R\(R'\b);
    solution_time = toc;

    % relative error
    error = norm(x - xe')/norm(xe');
    
    program(i-2) = "Matlab"
    names(i-2) = name
    import(i-2) = import_time
    rows(i-2) = row
    cols(i-2) = col
    nonZeros(i-2) = nnz(A)
    size(i-2) = info_A.bytes
    chol_info(i-2) = cholesky_time
    chol_size(i-2) = info_R.bytes
    sol_time(i-2) = solution_time
    err(i-2) = error
end

data = table(program, names, rows, cols, nonZeros, size, chol_info, chol_size, sol_time, err);
writetable(data,'results.csv','WriteRowNames',true);

