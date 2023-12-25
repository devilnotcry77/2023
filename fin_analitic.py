import numpy as np
import pandas as pd
from datetime import datetime

df = pd.read_excel('data/financials.xlsx')
df['Date'] = pd.to_datetime(df['order_date'])
print(df)

frequency = df['user_id'].value_counts()
print(frequency)

df_id_frequency = pd.DataFrame({'user_id': frequency.index, 'frequency': frequency.values})
print(df_id_frequency)

df_id_frequency.describe(percentiles=[.20, .40, .60, .80, .90, .99])
df_order_by_total_value_sum = df.groupby(by=['user_name', 'user_id']).sum().groupby(level=[0]).cumsum()
print(df_order_by_total_value_sum)

df_order_by_total_value_sum.rename(columns={'order_value': 'order_total_value'}, inplace=True)
print(df_order_by_total_value_sum)

df_order_by_last_date = df.sort_values("order_date").groupby("user_id").last()
print(df_order_by_last_date)

print(df_order_by_last_date.shape)
df_order_by_last_date.rename(columns={'order_date': 'order_last_date'}, inplace=True)
print(df_order_by_last_date)

df_order_by_last_date = df_order_by_last_date.drop(['order_value'], axis=1)
print(df_order_by_last_date)

frm_raw = df_order_by_last_date.merge(df_order_by_total_value_sum, on=["user_name", "user_id"])
print(frm_raw)

pd.options.display.float_format = "{:.2f}".format
print(frm_raw.describe())

frm_raw.describe(percentiles=[.20, .40, .60, .80, .90, .99])

most_monetary = frm_raw[frm_raw['order_total_value'] > 716252.17]
print(most_monetary)
print(most_monetary.shape)
most_monetary = most_monetary.sort_values(by='order_last_date')
print(most_monetary)

top104 = most_monetary.nlargest(105, ['order_total_value'])
print(top104)

now = '2021-09-19'
frm_raw['current_date'] = now
print(frm_raw)

frm_raw['current_date'] = pd.to_datetime(frm_raw['current_date'], format="%Y-%m-%d")
frm_raw['churn_time'] = frm_raw['current_date'] - frm_raw['order_last_date']
print(frm_raw)

print(frm_raw.describe())
churned_clients = frm_raw[frm_raw['churn_time'] > '730 days']
print(churned_clients)

frm_raw_with_frequency = frm_raw.merge(df_id_frequency, on=["user_id"])
print(frm_raw_with_frequency)
frm_raw_with_frequency.set_index('user_id')

churned_clients_with_frequency = frm_raw_with_frequency[frm_raw_with_frequency['churn_time'] > '730 days']
print(churned_clients_with_frequency)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(churned_clients_with_frequency)

frm_raw_with_frequency['M'] = [1 if x > 716252.51 else 0 for x in frm_raw_with_frequency['order_total_value']]
print(frm_raw_with_frequency)
frm_raw_with_frequency.loc[frm_raw_with_frequency['order_total_value'] <= 716252.52, 'M'] = 2
frm_raw_with_frequency.loc[frm_raw_with_frequency['order_total_value'] <= 91015.00, 'M'] = 3
print(frm_raw_with_frequency)

frm_raw_with_frequency['F'] = [1 if x > 20 else 0 for x in frm_raw_with_frequency['frequency']]
frm_raw_with_frequency.loc[frm_raw_with_frequency['frequency'] <= 20, 'F'] = 2
frm_raw_with_frequency.loc[frm_raw_with_frequency['frequency'] <= 5, 'F'] = 3
print(frm_raw_with_frequency)

from datetime import timedelta

delta3 = timedelta(days=730, hours=0, minutes=0)
delta2 = timedelta(days=290, hours=0, minutes=0)
delta1 = timedelta(days=0, hours=0, minutes=0)
frm_raw_with_frequency['R'] = [3 if x >= delta3 else 0 for x in frm_raw_with_frequency['churn_time']]
frm_raw_with_frequency.loc[frm_raw_with_frequency['churn_time'] < delta3, 'R'] = 2
frm_raw_with_frequency.loc[frm_raw_with_frequency['churn_time'] <= delta2, 'R'] = 1
frm_final = frm_raw_with_frequency
print(frm_final)

