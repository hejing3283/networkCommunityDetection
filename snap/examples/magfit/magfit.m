
data_orig = load('pp_networks_num-magfitf');
attr_orig = load('pp_networks_num-magfit');

data = data_orig > 0.5;

[L, x] = size(attr_orig);
attr_data = cell(2, 2, L);
for i=1:L
    attr_data{1,1,i} = attr_orig(i, 2);
    attr_data{1,2,i} = attr_orig(i, 3);
    attr_data{2,1,i} = attr_orig(i, 4);
    attr_data{2,2,i} = attr_orig(i, 5);
end

[m, n] = size(data);

result = zeros(m, m);

for i=1:m
    for j=1:m
        sum = 0.0;
        for l=1:n
            f_i = data(i, l) + 1;
            f_j = data(j, l) + 1;
            sum = sum + log(attr_data{f_i, f_j, l});
        end
        result(i, j) = sum/m;
    end
end

[C, L, U] = SpectralClustering(result, 4, 2);

