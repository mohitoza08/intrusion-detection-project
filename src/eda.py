import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


cols = [
    "duration","protocol_type","service","flag","src_bytes","dst_bytes",
    "land","wrong_fragment","urgent","hot","num_failed_logins","logged_in",
    "num_compromised","root_shell","su_attempted","num_root","num_file_creations",
    "num_shells","num_access_files","num_outbound_cmds","is_host_login",
    "is_guest_login","count","srv_count","serror_rate","srv_serror_rate",
    "rerror_rate","srv_rerror_rate","same_srv_rate","diff_srv_rate",
    "srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate","label","difficulty"
]

df = pd.read_csv("data/KDDTrain+.txt",header=None,names=cols)

df = df.drop('difficulty',axis=1)

#class dirtibution of label

# plt.figure(figsize=(12,5))
# sns.countplot(data=df,x='label')
# plt.xticks(rotation=90)
# plt.title("Class Distribution")
# plt.show()

#categorcal data summary
# categorical = ['protocol_type','service','flag']
# for col in categorical:
#     print(f" ---{col}--- ")
#     print(df[col].value_counts())

df_neumeric = df.select_dtypes(include=[np.number])
corr = df_neumeric.corr()

# plt.figure(figsize=(18,12))
# sns.heatmap(corr,cmap='coolwarm',annot=False)
# plt.title("Feature Correlation Matrix")
# plt.show()

# corr = df_neumeric.corr()

# # Upper triangle lo (duplicate nahi)
# high_corr = []
# for i in range(len(corr.columns)):
#     for j in range(i+1, len(corr.columns)):
#         if abs(corr.iloc[i,j]) > 0.9:
#             high_corr.append((corr.columns[i], corr.columns[j], corr.iloc[i,j]))

# print(len(high_corr), "highly correlated pairs (|r| > 0.9):")
# for pair in high_corr:
#     print(f"{pair[0]} <-> {pair[1]} : {pair[2]:.3f}")

# Binary label: normal=0, attack=1
df['label_binary'] = (df['label'] != 'normal').astype(int)
print(df['label_binary'].value_counts())