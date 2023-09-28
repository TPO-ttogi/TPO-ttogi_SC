import pandas as pd

df = pd.read_csv('sales_and_traffic_detail_sales_traffic_by_sku.csv')

df = df[df['TITLE'].str.contains('Jin')]

mild = df[df['TITLE'].str.contains('Mild')]
print("mild session total: ", mild['SESSIONS_TOTAL'].sum())
mild.sort_values(by='date', inplace = True, ascending=False)
print(mild)
# mild: 293 sessions/per day

spicy = df[df['TITLE'].str.contains('Spicy')]
print("spicy session total: ", spicy['SESSIONS_TOTAL'].sum())
spicy.sort_values(by='date', inplace = True, ascending=False)
print(spicy)
# spicy: 216 sessions/per day


# print("Jin Ramen Mild: \n", df[df['TITLE'].str.contains('Mild')])
# print("Jin Ramen Spicy: \n", df[df['TITLE'].str.contains('Spicy')])