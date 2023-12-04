import matplotlib.pyplot as plt
import pandas as pd

file_path = "/home/yimoning/research/pydevs/pyjoulse_test/result1.csv"
df = pd.read_csv(file_path, sep=';')

df['time'] = df['duration'].cumsum()

columns = ['package_0', 'dram_0', 'core_0', 'uncore_0']
for col in columns:
    plt.figure(figsize=(10, 6))
    plt.plot(df['time'], df[col], label=col, linestyle='-', linewidth=2)
    plt.title(col)
    plt.xlabel('Time (s)')
    plt.ylabel('Value')
    plt.legend()
    plt.grid(True)
    plt.show()
