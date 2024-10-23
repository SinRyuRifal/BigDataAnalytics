import os
import pandas as pd
import mimetypes
from pandas import json_normalize

folder_data = '/home/bda/data_raw'

def is_binary_file(filepath):
    mime = mimetypes.guess_type(filepath)[0]
    if mime:
        return mime.startswith('image/') or mime.startswith('video/')
    return False

def convert_json_to_csv(json_path):
    csv_path = json_path.replace('.json', '.csv')
    try:
        with open(json_path, 'r') as f:
            json_data = pd.read_json(f)

        if 'Rekapitulasi' in json_data:
            rekap_df = json_normalize(json_data['Rekapitulasi'])
            flat_df = pd.concat([json_data.drop(columns='Rekapitulasi'), rekap_df], axis=1)
        else:
            flat_df = json_data

        flat_df.to_csv(csv_path, index=False)
        print(f"File JSON '{json_path}' telah diubah menjadi CSV: '{csv_path}'")
        return csv_path
    except ValueError as e:
        print(f"Error saat mengonversi {json_path}: {e}")
        return None

def combine_data_files(folder_data):
    combined_df = pd.DataFrame()

    for root, dirs, files in os.walk(folder_data):
        for file in files:
            file_path = os.path.join(root, file)

            if is_binary_file(file_path):
                print(f"File '{file_path}' adalah file biner. Melewati...")
                continue

            if file.lower().endswith('.json'):
                csv_file = convert_json_to_csv(file_path)
                if csv_file:
                    df = pd.read_csv(csv_file)
                    combined_df = pd.concat([combined_df, df], ignore_index=True)
                continue

            if file.lower().endswith(('.csv', '.xls', '.xlsx')):
                print(f"Memproses file: {file_path}")
                if file.lower().endswith('.csv'):
                    df = pd.read_csv(file_path)
                elif file.lower().endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file_path)

                combined_df = pd.concat([combined_df, df], ignore_index=True)

    combined_df = combined_df.loc[:, ~combined_df.columns.duplicated()]  
    return combined_df

def save_combined_data(output_path, combined_df):
    combined_df.to_csv(output_path, index=False)
    print(f"Hasil data berhasil disimpan ke: {output_path}")

output_csv_path = '/home/bda/data_raw/Combined_Data.csv'
combined_df = combine_data_files(folder_data)
save_combined_data(output_csv_path, combined_df)
