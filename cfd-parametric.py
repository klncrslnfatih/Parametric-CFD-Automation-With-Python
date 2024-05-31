'''
Merhaba. Ben Fatih KILINÇARSLAN. Bu kod, Lisans bitirme projemi yaparken kullandığım CFD otomatize etme işlemlerini içinde
bulundurmaktadır. TUI kodlarının tamamı ANSYS Fluent 2022 R1'e uygun olacak şekilde yazılmıştır. Kullanımı şu şekildedir:
1. Kullanılacak TUI kodu manipüle edilmeli ve gerekli değişiklikler (sürüme göre) yapılmalıdır. (Örnek TUI kodları "tui-codes"
isimli klasörde bulunmaktadır.)
2. Aynı dizinde analizlerin istenilen parametrelerini bulunduran "cfd-values.xlsx" adında bir excel dosyası olmalıdır.
3. Cmd üzerinden fluent çalıştırılmaya uyumlu olduktan sonra "cfd-parametric.py" üzerine tıklanarak program çalıştırılabilir.
4. Program çalıştırıldıktın sonra klasörler ve journal dosyalarını oluşturmaktadır. Analizlerin lokalde gerçekleştirilmesi
isteniyorsa "enter" e basılarak işlemler devam ettirilebilir.
5. Excel içerisinde belirlenen tüm analizler yapıldıktan sonra sonuçları oluşturacak ve program kendisini kapatacaktır.

Hello. I am Fatih KILINÇARSLAN. This code includes the CFD automation processes that I used while doing my undergraduate graduation
project. All TUI codes were written to be compatible with ANSYS Fluent 2022 R1. Its usage is as follows:
1. The TUI code to be used must be manipulated and the necessary changes must be made (according to the version). (Sample TUI codes
are in the folder named "tui-codes")
2. There must be an excel file named "cfd-values.xlsx" in the same directory that contains the desired parameters of the analysis.
3. After it is compatible with running Fluent via cmd, the program can be run by clicking on "cfd-parametric.py".
4. After the program is run, it creates folders and journal files. If you want to perform the analyzes locally, you can continue the
processes by pressing "enter".
5. After all the analyzes specified in Excel are done, it will create the results and the program will close itself.

Github: @klncrslnfatih
LinkedIn: /fatihkilincarslan
'''

import os
import subprocess
import pandas as pd
import math
import matplotlib.pyplot as plt

def run_fluent_simulation(jou_file):
    fluent_command = "fluent 2ddp -g -i {} -t4".format(jou_file)  #2d, 2ddp, 3d, 3ddp, and -t(cpu/core number)!!! 
    result = subprocess.run(fluent_command, shell=True)

    # Check exit status
    if result.returncode != 0:
        print(f"Error: Fluent could not be executed - Exit status: {result.returncode}")

def run_simulations_in_folders(analysis_folder):
    for root, dirs, files in os.walk(analysis_folder):
        for file in files:
            if file.endswith(".jou"):
                jou_file_path = os.path.join(root, file)
                run_fluent_simulation(jou_file_path)

def write_last_values_to_excel(analysis_folder):
    results = {'AoA': [], 'Cl': [], 'Cd': []}

    for root, dirs, files in os.walk(analysis_folder):
        for file in files:
            if file.endswith("-cl.out"):
                aoa = int(file.split("-")[1].split("_")[0].replace("AoA", ""))
                cl_values = get_last_values(os.path.join(root, file))
                results['AoA'].append(aoa)
                results['Cl'].append(cl_values[-1])

            elif file.endswith("-cd.out"):
                aoa = int(file.split("-")[1].split("_")[0].replace("AoA", ""))
                cd_values = get_last_values(os.path.join(root, file))
                results['Cd'].append(cd_values[-1])

    df = pd.DataFrame(results)
    df.to_excel(os.path.join(analysis_folder, 'analysis_results.xlsx'), index=False)
    print("Analysis results written to Excel file.")

def get_last_values(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        last_line = lines[-1].strip()
        last_values = [float(value) for value in last_line.split()]
        return last_values

def plot_results(excel_file_path):
    # Read the Excel file
    results_df = pd.read_excel(excel_file_path)

    # Cl - AoA plot
    plt.figure(figsize=(10, 6))
    plt.plot(results_df['AoA'], results_df['Cl'], marker='o', linestyle='-', color='b')
    plt.title('Cl - AoA Plot')
    plt.xlabel('AoA (Degrees)')
    plt.ylabel('Cl')
    plt.grid(True)
    plt.savefig(os.path.join(os.path.dirname(excel_file_path), 'Cl_AoA_Plot.png'))

    # Cd - AoA plot
    plt.figure(figsize=(10, 6))
    plt.plot(results_df['AoA'], results_df['Cd'], marker='o', linestyle='-', color='r')
    plt.title('Cd - AoA Plot')
    plt.xlabel('AoA (Degrees)')
    plt.ylabel('Cd')
    plt.grid(True)
    plt.savefig(os.path.join(os.path.dirname(excel_file_path), 'Cd_AoA_Plot.png'))

def read_inputs_from_excel(excel_file):
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)

        # Check for required columns
        required_columns = ['aoa-param', 'case_folder_name', 'scale_param', 'inlet_velocity', 'courant_number', 'convergence_param', 'iteration_param']
        if not set(required_columns).issubset(df.columns):
            raise ValueError(f"Error: Required columns missing. Please check column names. Required columns: {required_columns}")

        # Read user inputs
        aoa_list = df['aoa-param'].tolist()
        params_df = df.drop(columns=['aoa-param'])

        return aoa_list, params_df
    except Exception as e:
        print(f"Error: Failed to read Excel file - {e}")
        return None
    
def merge_and_save_output(output_file):
    folder_path = os.path.dirname(os.path.realpath(__file__))  # Path of the directory where the script resides
    
    # Content to be merged from journal files
    merged_content = ""

    # Iterate through folders
    for folder_name in os.listdir(folder_path):
        if folder_name.startswith("AoA-"):  # Process only folders starting with "AoA-"
            folder_path_aoa = os.path.join(folder_path, folder_name)
            
            # Iterate through files inside the folder
            for file_name in os.listdir(folder_path_aoa):
                if file_name.startswith("journal-AoA-") and file_name.endswith(".jou"):  # Process only desired file formats
                    file_path = os.path.join(folder_path_aoa, file_name)
                    
                    # Check if file exists
                    if os.path.exists(file_path):
                        # Read and merge the file content
                        with open(file_path, 'r') as file:
                            content = file.readlines()[:-1]  # Skip the last line to avoid duplication
                            merged_content += ''.join(content)  # Append to merged content

    # Add "/exit" command at the end
    merged_content += "/exit\n"

    # Save the merged content
    with open(output_file, 'w') as output:
        output.write(merged_content)

    print("Journal files merged and saved.")

def create_analysis_folders_from_excel(excel_file, analysis_folder_param=None):
    inputs = read_inputs_from_excel(excel_file)

    if inputs:
        aoa_list, params_df = inputs

        # Get input for analysis folder path
        if analysis_folder_param is None:
            analysis_folder_param = os.path.dirname(os.path.abspath(__file__))  # Directory where the script resides
        
        for aoa, params in zip(aoa_list, params_df.to_dict(orient='records')):
            aoa_str = f"({aoa})" if aoa < 0 else str(aoa)
            aoa_param = f"AoA-{aoa_str}"
            folder_name = aoa_param
            folder_path = os.path.join(analysis_folder_param, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            print(f"Folder '{folder_name}' created.")

            # Calculate velocity components
            aoa_rad = math.radians(aoa)
            velocity_x = math.cos(aoa_rad)
            velocity_y = math.sin(aoa_rad)

            # Create journal file
            journal_file_name = f"journal-{aoa_param}.jou"
            journal_file_path = os.path.join(folder_path, journal_file_name)

            # Write content to journal file
            with open(journal_file_path, 'w') as journal_file:
                journal_file.write(
f"""\
;{aoa_param}
/file/read-case/"{params['case_folder_name']}"
/mesh/check
/mesh/repair-improve/repair
/mesh/check
/mesh/scale/ {params['scale_param']} {params['scale_param']}
/mesh/check
/mesh/quality
/define/models/solver/pressure-based y
/solve/set/gradient-scheme n n
/define/models/viscous/kw-sst? y
/define/boundary-conditions/velocity-inlet inlet-velocity y y n {params['inlet_velocity']} n 0 n {velocity_x} n {velocity_y} n n y 5.0 10.0
/define/boundary-conditions/pressure-outlet outlet-pressure y n 0 n y n n y 5.0 10.0 y n n
/report/reference-values/area 0.1
/report/reference-values/density 1.225
/report/reference-values/depth 1
/report/reference-values/enthalpy 0
/report/reference-values/length 0.101
/report/reference-values/pressure 101325
/report/reference-values/temperature 288.16
/report/reference-values/velocity {params['inlet_velocity']}
/report/reference-values/viscosity 1.7894e-05
/solve/set p-v-coupling 24
/solve/set p-v-controls {params['courant_number']} 0.5 0.5
/solve/report-definitions/add Cl lift force-vector -{velocity_y} {velocity_x} average-over 1 pe-zone? n thread-names wall () q
/solve/report-definitions/add Cd drag force-vector {velocity_x} {velocity_y} average-over 1 pe-zone? n thread-names wall () q
/solve/report-files/add Cl frequency-of iteration frequency 1 file-name "{folder_path}\{aoa_param}-cl.out" report-defs Cl () q
/solve/report-files/add Cd frequency-of iteration frequency 1 file-name "{folder_path}\{aoa_param}-cd.out" report-defs Cd () q
/solve/monitors/residual/convergence-criteria {params['convergence_param']} {params['convergence_param']} {params['convergence_param']} {params['convergence_param']} {params['convergence_param']}
/solve/initialize/hyb-initialization
/solve/iterate {params['iteration_param']}
/file/write-case-data "{folder_path}\{aoa_param}.cas.h5"
/exit
"""
                )

        print("Folder and journal files creation completed.")

if __name__ == "__main__":
    excel_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cfd-values.xlsx")
    create_analysis_folders_from_excel(excel_file_path)
    output_file = "merged_journal.txt"  # Output file name
    merge_and_save_output(output_file)

    analysis_folder_param = input("Path to analysis folder (Use current directory if empty): ").strip()

    if not analysis_folder_param:
        analysis_folder_param = os.getcwd()  # Use current directory if empty

    run_simulations_in_folders(analysis_folder_param)
    excel_file_path = os.path.join(analysis_folder_param, 'analysis_results.xlsx')

    # Write analysis results to Excel file
    write_last_values_to_excel(analysis_folder_param)

    # Generate plots
    plot_results(excel_file_path)
