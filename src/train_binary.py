import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

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

df_train = pd.read_csv("data/KDDTrain+.txt", header=None, names=cols)
df_test = pd.read_csv("data/KDDTest+.txt", header=None, names=cols)

df_train['src'] = 'train'
df_test['src'] = 'test'

df_all = pd.concat([df_train, df_test], ignore_index=True)
df_all = pd.get_dummies(df_all, columns=['protocol_type', 'service', 'flag'])

train_mask = df_all['src'] == 'train'
df_train_enc = df_all[train_mask].copy()
df_test_enc = df_all[~train_mask].copy()

for d in [df_train_enc, df_test_enc]:
    d['label_bin'] = (d['label'] != 'normal').astype(int)
    d.drop(['label', 'difficulty', 'src'], axis=1, inplace=True)

X = df_train_enc.drop('label_bin', axis=1).values
y = df_train_enc['label_bin'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc_train = accuracy_score(y_test, y_pred)
print(f"Validation Accuracy: {acc_train}")

X_test_real = df_test_enc.drop('label_bin', axis=1).values
y_test_real = df_test_enc['label_bin'].values

y_pred_real = model.predict(X_test_real)
acc_real = accuracy_score(y_test_real, y_pred_real)
print(f"Real Test Accuracy: {acc_real}")

with open("models/rf_binary.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to ids-project/models/rf_binary.pkl")

print(list(df_train_enc.drop('label_bin', axis=1).columns))
