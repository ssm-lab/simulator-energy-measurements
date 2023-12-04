import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    use_col = ['duration', 'package_0', 'dram_0', 'core_0', 'uncore_0']
    df_os = pd.read_csv("energy_consumption.csv", usecols=use_col, sep=';')
    df_all = pd.read_csv("energy_consumption_run.csv", usecols=use_col, sep=';')
    df_os = df_os[df_os['duration'] <= 0.2]
    df_all = df_all[df_all['duration'] <= 0.2]
    df_os['time'] = df_os['duration'].cumsum()
    df_all['time'] = df_all['duration'].cumsum()
    # Plotting
    columns = ['package_0', 'dram_0', 'core_0', 'uncore_0']
    columns = ['package_0', 'dram_0', 'core_0', 'uncore_0']
    columns = ['package_0', 'dram_0', 'core_0', 'uncore_0']
    for col in columns:
        plt.figure(figsize=(10, 6))

        plt.plot(df_os['time'], df_os[col], color='blue', label='df_os', linestyle='--', linewidth=2, marker='o',
                 alpha=0.7)
        plt.plot(df_all['time'], df_all[col], color='red', label='df_all', linestyle='-', linewidth=1, marker='x',
                 alpha=0.7)

        plt.title(col)
        plt.xlabel('Time')
        plt.ylabel(col)
        plt.legend()
        plt.grid(True)
        plt.show()