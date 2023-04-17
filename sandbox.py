# Ammon's testing spot

# TODO: copy ChoosingGraphSchema last cell, but with few columns
import pandas as pd
data = pd.read_csv('datasets/suicide_rates_by_category.csv')
# TODO: turn suicides/100k pop into suicide buckets


# suicides_per_100k_bins
# 0-25       21712
# 25-75       2959
# 75-100       317
# 100-125       60
# 125-150       14
# 150-300       14

ageRateGdp = data[['country', 'year', 'age', 'suicides/100k pop', 'gdp_per_capita ($)']]
ageRateGdp['suicide bucket'] = '0-25'

highRisk = pd.DataFrame()

for index in ageRateGdp.index:
    rowSuicideRate = ageRateGdp['suicides/100k pop'][index]
    if rowSuicideRate < 25:
        ageRateGdp['suicide bucket'][index] = '0-25'
    elif rowSuicideRate < 75:
        ageRateGdp['suicide bucket'][index] = '25-75'
    elif rowSuicideRate < 100:
        ageRateGdp['suicide bucket'][index] = '75-100'
    elif rowSuicideRate < 125:
        ageRateGdp['suicide bucket'][index] = '100-125'
    elif rowSuicideRate < 150:
        ageRateGdp['suicide bucket'][index] = '125-150'
    elif rowSuicideRate > 150:
        ageRateGdp['suicide bucket'][index] = '150-300'
    if rowSuicideRate > 100:
        entry = ageRateGdp.loc[ageRateGdp['suicide bucket'] == '150-300']
        highRisk = pd.concat([highRisk, entry])
print(highRisk.to_string())

# TODO: only graph lowest suicide bucket
