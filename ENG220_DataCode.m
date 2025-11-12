% process_CO2_data_fixed.m
% Read table, remove any rows with missing values, then compute count,
% mean, std, min, median, max, and sum for each numeric column grouped by country.

% Read the CSV
T = readtable("C:\Users\darkl\Downloads\CO2 emission by countries.csv");

% Remove rows with any missing values
T = rmmissing(T);

% Find the country column: choose first non-numeric column (common pattern)
varTypes = varfun(@class, T, 'OutputFormat', 'cell');
isNumericCol = varfun(@isnumeric, T, 'OutputFormat', 'uniform');
nonNumericIdx = find(~isNumericCol, 1);

if isempty(nonNumericIdx)
    % fallback: assume first column is country if all numeric
    countryVarName = T.Properties.VariableNames{1};
else
    countryVarName = T.Properties.VariableNames{nonNumericIdx};
end

% Extract country column and convert to string for safety
countryCol = T.(countryVarName);
countryStr = string(countryCol);  % works for cellstr, char, categorical, string

% Identify numeric columns to summarize
numericMask = varfun(@isnumeric, T, 'OutputFormat', 'uniform');
numericNames = T.Properties.VariableNames(numericMask);

if isempty(numericNames)
    error('No numeric columns found to summarize.');
end

% Grouping
G = findgroups(countryStr);
nGroups = max(G);

% Get list of unique countries (in group order)
countries = splitapply(@(x) x(1), countryStr, G);   % string array

% Preallocate result table with country column
Result = table;
Result.Country = countries;

% For each numeric variable compute stats per group and add to Result
for i = 1:numel(numericNames)
    colName = numericNames{i};
    vec = T.(colName);           % numeric vector
    % Make sure it's a column vector
    vec = vec(:);

    % Count non-NaN values per group
    cnt = splitapply(@(x)sum(~isnan(x)), vec, G);

    % Mean, Std, Min, Median, Max, Sum using omitnan
    mn = splitapply(@(x)mean(x,'omitnan'), vec, G);
    sd = splitapply(@(x)std(x,'omitnan'), vec, G);
    mnm = splitapply(@(x)min(x,[],'omitnan'), vec, G);
    med = splitapply(@(x)median(x,'omitnan'), vec, G);
    mxx = splitapply(@(x)max(x,[],'omitnan'), vec, G);
    ssum = splitapply(@(x)sum(x,'omitnan'), vec, G);

    % Add columns to Result with descriptive names
    safeName = matlab.lang.makeValidName(colName); % ensure valid var name
    Result.([safeName '_Count'])  = cnt;
    Result.([safeName '_Mean'])   = mn;
    Result.([safeName '_Std'])    = sd;
    Result.([safeName '_Min'])    = mnm;
    Result.([safeName '_Median']) = med;
    Result.([safeName '_Max'])    = mxx;
    Result.([safeName '_Sum'])    = ssum;
end

% Display and optionally save
disp('Summary statistics by country:');
disp(Result);

writetable(Result, 'country_summary_stats_fixed.csv');
disp('Saved to country_summary_stats_fixed.csv');
