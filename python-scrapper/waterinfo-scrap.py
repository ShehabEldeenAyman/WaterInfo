from pywaterinfo import Waterinfo
import os
import pandas as pd

vmm = Waterinfo("vmm")
hic = Waterinfo("hic")

def fetch_vmm_hic_group_list():
    vmm_group_list = vmm.get_group_list()
    hic_group_list = hic.get_group_list()

    vmm_group_list = vmm_group_list[vmm_group_list['group_type'].isin(['timeseries', 'timeseries_dynamic'])]
    hic_group_list = hic_group_list[hic_group_list['group_type'].isin(['timeseries', 'timeseries_dynamic'])]

    vmm_group_list.to_csv('../CSV-data/vmm_group_list.csv', index=False)
    hic_group_list.to_csv('../CSV-data/hic_group_list.csv', index=False)
    
    return vmm_group_list, hic_group_list

def fetch_vmm_hic_group_id(vmm_group_list, hic_group_list):
    vmm_ts_id = pd.DataFrame()
    hic_ts_id = pd.DataFrame()

    for i in vmm_group_list["group_id"]:
        ts_data = vmm.get_timeseries_value_layer(timeseriesgroup_id=i)
        if ts_data is not None and not ts_data.empty:
            ts_data['group_id'] = i
            vmm_ts_id = pd.concat([vmm_ts_id, ts_data], ignore_index=True)

    vmm_ts_id.to_csv('../CSV-data/vmm_ts_id.csv', index=False)

    for i in hic_group_list["group_id"]:
        ts_data = hic.get_timeseries_value_layer(timeseriesgroup_id=i)
        if ts_data is not None and not ts_data.empty:
            ts_data['group_id'] = i
            hic_ts_id = pd.concat([hic_ts_id, ts_data], ignore_index=True)

    hic_ts_id.to_csv('../CSV-data/hic_ts_id.csv', index=False)
    
    return vmm_ts_id, hic_ts_id

def get_vmm_hic_timeseries(vmm_ts_id, hic_ts_id):
    vmm_file = '../CSV-data/vmm_ts_values.csv'
    hic_file = '../CSV-data/hic_ts_values.csv'

    for index, row in vmm_ts_id.iterrows():
        ts_values = vmm.get_timeseries_values(row['ts_id'], period="P1D")
        if not os.path.exists(vmm_file):
            ts_values.to_csv(vmm_file, index=False, mode='a', header=True)
        else:
            ts_values.to_csv(vmm_file, index=False, mode='a', header=False)

    for index, row in hic_ts_id.iterrows():
        ts_values = hic.get_timeseries_values(row['ts_id'], period="P1D")
        if not os.path.exists(hic_file):
            ts_values.to_csv(hic_file, index=False, mode='a', header=True)
        else:
            ts_values.to_csv(hic_file, index=False, mode='a', header=False)

def main():
    os.makedirs('../CSV-data', exist_ok=True)
    
    vmm_group_list, hic_group_list = fetch_vmm_hic_group_list()
    vmm_ts_id, hic_ts_id = fetch_vmm_hic_group_id(vmm_group_list, hic_group_list)
    get_vmm_hic_timeseries(vmm_ts_id, hic_ts_id)

if __name__ == "__main__":
    main()
