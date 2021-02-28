import pandas as pd
import numpy as np

data1 = pd.read_csv('./dataset/csv1.csv')
data2 = pd.read_csv('./dataset/csv2.csv')

# Union of columns
columns = list(set(data1.columns | data2.columns))

d = {col: data1[col] if col in data1.columns else data2[col] for col in columns}
merged_data = pd.DataFrame(data=d)


# Rearranging columns
new_order = ['DY', 'MO', 'YEAR', 'LAT', 'LON']
columns_list = merged_data.columns.tolist()
for col_name in new_order:
    columns_list.remove(col_name)

columns_list = new_order + columns_list
merged_data = merged_data[columns_list]


# If data has KT (Insolation Clearness Index) column it must be converted to float
if 'KT' in merged_data:
    # 'KT' column may have 2 different values that describes missing values. nan and -999.0
    merged_data['KT'] = merged_data['KT'].replace('               nan', '-999')
    merged_data['KT'] = merged_data['KT'].astype(float)


# Value for missing model data cannot be computed or out of model availability range: -999.0
# Replace these values to np.nan in order to use pre-defined functions effectively.
merged_data.replace(-999.0, np.nan, inplace=True)

# Save merged csv file
#TODO add optional parameter using argparse
merged_data.to_csv('./dataset/merged_data.csv', index=False)