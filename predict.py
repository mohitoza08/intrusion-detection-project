import argparse
import pickle
import pandas as pd
import json

model_bin = pickle.load(open("models/rf_binary.pkl","rb"))
model_multi = pickle.load(open("models/rf_multiclass.pkl",'rb'))['model']

cols = ['duration', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot',
        'num_failed_logins', 'logged_in', 'num_compromised', 'root_shell', 'su_attempted',
        'num_root', 'num_file_creations', 'num_shells', 'num_access_files', 'num_outbound_cmds',
        'is_host_login', 'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
        'rerror_rate', 'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
        'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
        'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 
        'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 
        'protocol_type_icmp', 'protocol_type_tcp', 'protocol_type_udp', 'service_IRC', 
        'service_X11', 'service_Z39_50', 'service_aol', 'service_auth', 'service_bgp', 
        'service_courier', 'service_csnet_ns', 'service_ctf', 'service_daytime', 
        'service_discard', 'service_domain', 'service_domain_u', 'service_echo', 
        'service_eco_i', 'service_ecr_i', 'service_efs', 'service_exec', 'service_finger', 
        'service_ftp', 'service_ftp_data', 'service_gopher', 'service_harvest', 'service_hostnames', 
        'service_http', 'service_http_2784', 'service_http_443', 'service_http_8001', 'service_imap4', 
        'service_iso_tsap', 'service_klogin', 'service_kshell', 'service_ldap', 'service_link', 'service_login', 
        'service_mtp', 'service_name', 'service_netbios_dgm', 'service_netbios_ns', 'service_netbios_ssn', 
        'service_netstat', 'service_nnsp', 'service_nntp', 'service_ntp_u', 'service_other', 'service_pm_dump', 
        'service_pop_2', 'service_pop_3', 'service_printer', 'service_private', 'service_red_i', 
        'service_remote_job', 'service_rje', 'service_shell', 'service_smtp', 'service_sql_net', 
        'service_ssh', 'service_sunrpc', 'service_supdup', 'service_systat', 'service_telnet', 
        'service_tftp_u', 'service_tim_i', 'service_time', 'service_urh_i', 'service_urp_i', 
        'service_uucp', 'service_uucp_path', 'service_vmnet', 'service_whois', 'flag_OTH', 
        'flag_REJ', 'flag_RSTO', 'flag_RSTOS0', 'flag_RSTR', 'flag_S0', 'flag_S1', 'flag_S2', 
        'flag_S3', 'flag_SF', 'flag_SH']


def preprocess(data):
    df = pd.DataFrame([data])
    df = pd.get_dummies(df,columns=['protocol_type','service','flag'])
    for col in cols:
        if col not in df.columns:
            df[col]=0
    return df[cols]        
def preprocess_batch(df):
    df = pd.get_dummies(df, columns=['protocol_type', 'service', 'flag'])
    for col in cols:
        if col not in df.columns:
            df[col] = 0
    return df[cols].values

def predict_single(features):
    df = preprocess(features)
    pred_bin = int(model_bin.predict(df.values)[0])
    label = "Attack" if pred_bin == 1 else "Normal"
    print(f"Binary: {pred_bin} ({label})")

def predict_single(features):
    df = preprocess(features)
    pred_bin = int(model_bin.predict(df.values)[0])
    label = "Attack" if pred_bin == 1 else "Normal"
    pred_multi = int(model_multi.predict(df.values)[0])
    types = {0: "Normal", 1: "DoS", 2: "Probe", 3: "R2L", 4: "U2R"}
    print(f"Prediction: {pred_bin} ({label})")
    print(f"Attack Type: {pred_multi} ({types.get(pred_multi, 'Unknown')})")    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="IDS CLI Predictor")
    parser.add_argument("--src_bytes", type=int, default=0)
    parser.add_argument("--dst_bytes", type=int, default=0)
    parser.add_argument("--protocol_type", default="tcp")
    parser.add_argument("--service", default="http")
    parser.add_argument("--flag", default="SF")
    parser.add_argument("--csv", help="Batch predict from CSV file")
    parser.add_argument("--output", default="predictions.csv", help="Output CSV file")
    args = parser.parse_args()

    if args.csv:
       if args.csv:
        df = pd.read_csv(args.csv)
        X = preprocess_batch(df)
        preds = model_bin.predict(X)
        df['prediction'] = preds
        df['label'] = ['Attack' if p == 1 else 'Normal' for p in preds]
        df.to_csv(args.output, index=False)
        print(f"Saved predictions to {args.output}")
    else:
        # Single predict
        features = {
            "duration": 0, "src_bytes": args.src_bytes, "dst_bytes": args.dst_bytes,
            "protocol_type": args.protocol_type, "service": args.service, "flag": args.flag
        }
        predict_single(features)    