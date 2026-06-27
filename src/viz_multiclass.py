import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import pickle

data = pickle.load(open("models/rf_multiclass.pkl","rb"))
model =data['model']
feature_names = data['feature_names']

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

df_train = pd.read_csv("data/KDDTrain+.txt",header=None,names=cols)
df_test = pd.read_csv("data/KDDTest+.txt",header=None,names=cols)

df_train['src']='train'
df_test['src'] = 'test'

df_all =pd.concat([df_train,df_test],ignore_index=True)
df_all =pd.get_dummies(df_all,columns=['protocol_type','service','flag'])

train_mask = df_all['src']=="train"
df_train_enc = df_all[train_mask]
df_test_enc = df_all[~train_mask]

def map_label(label):
    dos={'back','land','neptune','pod','teardrop'}
    probe = {'ipsweep','nmap','portsweep','satan'}
    r2l = {'ftp_write','guess_passwd','imap','multihop','phf','spy','warezclient','warezmaster'}
    u2r = {'buffer_overflow','loadmodule','perl','rootkit'}
    if label == 'normal': return 0
    if label in dos: return 1
    if label in probe: return 2
    if label in r2l: return 3
    if label in u2r: return 4
    return -1

for d in [df_train_enc,df_test_enc]:
    d['label_multi'] = d['label'].map(map_label)
    d.drop(['label','difficulty','src'],axis=1,inplace=True)

y_test_real = df_test_enc['label_multi'].values
X_test_real = df_test_enc[feature_names].values    
y_pred_real = model.predict(X_test_real)

# cm = confusion_matrix(y_test_real,y_pred_real)
# labels = ['Normal','Dos','Probe','R2l','U2R','Unknown']

# plt.figure(figsize=(8,6))
# sns.heatmap(cm,annot=True,fmt='d',cmap='Blues',
#             xticklabels=labels,yticklabels=labels)
# plt.xlabel("predicted")
# plt.ylabel("acutal")
# plt.title("Confusion Matrix")
# plt.tight_layout()
# plt.savefig("confusion_matrix.png")
# plt.show()

importances = model.feature_importances_
indices = np.argsort(importances)[-20:]

plt.figure(figsize=(10,8))
plt.barh(range(20),importances[indices])
plt.yticks(range(20),[feature_names[i] for i in indices])
plt.xlabel("feature Importances")
plt.title("top 20 features - Random Forest Multi Class")
plt.tight_layout()
plt.savefig('feature.png')
plt.show()
