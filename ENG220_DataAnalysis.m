% Computes summary statistics for each country's the CO2 emissions.

% Read the CSV file 
%Copy the file path of the dataset on your coputer and enter it in here.
T = readtable("file path");

% Remove rows with missing values
T = rmmissing(T);

% Column names
countryVar = 'Country';                
emissionVar = 'CO2Emission_Tons_';     

% Extract data
country = string(T.(countryVar));
emissions = T.(emissionVar);

% Group by country
G = findgroups(country);
countries = splitapply(@(x) x(1), country, G);

% Calculate statistics
Count  = splitapply(@(x) sum(~isnan(x)), emissions, G);
Mean   = splitapply(@(x) mean(x,'omitnan'), emissions, G);
Std    = splitapply(@(x) std(x,'omitnan'), emissions, G);
Min    = splitapply(@(x) min(x,[],'omitnan'), emissions, G);
Median = splitapply(@(x) median(x,'omitnan'), emissions, G);
Max    = splitapply(@(x) max(x,[],'omitnan'), emissions, G);
Sum    = splitapply(@(x) sum(x,'omitnan'), emissions, G);

% Build result table
Result = table(countries, Count, Mean, Std, Min, Median, Max, Sum);
Result.Properties.VariableNames{1} = countryVar;

% Display & save
disp(Result);