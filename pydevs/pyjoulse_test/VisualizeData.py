import sys

import pandas as pd
import matplotlib.pyplot as plt

def moving_average_smoothing(data, window_size):
    smoothed_data = pd.Series(data).rolling(window=window_size, center=True).mean()
    return smoothed_data

class Visual:
    def __init__(self, file_path, start_time, end_time):
        self.col_list = ['timestamp', 'duration', 'package_0', 'dram_0', 'core_0', 'uncore_0']
        self.df = pd.read_csv(file_path, usecols=self.col_list, sep=';')
        self.start_time = start_time
        self.end_time = end_time
        self.__process_data()

    def __process_data(self):
        # Adjust timestamp
        self.df['timestamp'] = self.df['timestamp'] - self.df.loc[0, 'timestamp']
        # Calculate average power for each column
        for col in ['package_0', 'dram_0', 'core_0', 'uncore_0']:
            self.df[f'{col}_power'] = self.df[col] / self.df['duration']

    def plot(self, columns, granularity=1):
        for col in columns:
            if col in ['package_0', 'dram_0', 'core_0', 'uncore_0']:
                plt.figure(figsize=(12, 7))
                power_col = f'{col}_power'
                i = 0
                max_plotted_power = 0
                while i < len(self.df['timestamp']) - 1:
                    time_diff = self.df.loc[min(i + granularity, len(self.df) - 1), 'timestamp'] - self.df.loc[
                        i, 'timestamp']
                    energy_consumed = self.df.loc[i, power_col] * time_diff
                    avg_power = energy_consumed / time_diff

                    if avg_power > max_plotted_power:
                        max_plotted_power = avg_power

                    plt.hlines(y=avg_power,
                               xmin=self.df.loc[i, 'timestamp'],
                               xmax=self.df.loc[min(i + granularity, len(self.df) - 1), 'timestamp'],
                               color='blue')
                    i += granularity
                plt.axvline(x=self.start_time, linestyle='--', color='red')
                plt.axvline(x=self.end_time, linestyle='--', color='red')
                plt.text(self.start_time, max_plotted_power, 'sim start', verticalalignment='top')
                plt.text(self.end_time, max_plotted_power, 'sim end', verticalalignment='top')
                plt.ylim(0, max_plotted_power + max_plotted_power * 0.4)
                plt.title(f'Average Power Consumption for {col}')
                plt.xlabel('Time (s)')
                plt.ylabel('Power Consumption')
                plt.grid(True)
                plt.tight_layout()
                plt.show()
    def plot_continuous(self, columns, window_size=3):
        for col in columns:
            if col in ['package_0', 'dram_0', 'core_0', 'uncore_0']:
                plt.figure(figsize=(12, 7))
                power_col = f'{col}_power'
                plt.plot(self.df['timestamp'], self.df[power_col], color='blue', label=power_col)
                smoothed_data = moving_average_smoothing(self.df[power_col], window_size)
                plt.plot(self.df['timestamp'], smoothed_data, color='red', linestyle='--', label=f'{power_col}_smoothed')
                plt.axvline(x=self.start_time, linestyle='--', color='red')
                plt.axvline(x=self.end_time, linestyle='--', color='red')
                plt.text(self.start_time, self.df[power_col].max(), 'sim start', verticalalignment='top')
                plt.text(self.end_time, self.df[power_col].max(), 'sim end', verticalalignment='top')
                plt.title(f'Power Consumption over Time for {col}')
                plt.xlabel('Time (s)')
                plt.ylabel('Power Consumption')
                plt.grid(True)
                plt.legend()
                plt.tight_layout()
                plt.show()



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Visual.py <start_time> <end_time>")
        file_path = "/home/yimoning/research/data/96*96_96_times.csv"
        test = Visual(file_path, 0, 30)
        test.plot_continuous(['package_0', 'dram_0', 'core_0', 'uncore_0'])
        sys.exit(1)

    file_path = "/home/yimoning/research/data/100*100_100times.csv"
    start_time = float(sys.argv[1])
    end_time = float(sys.argv[2])
    print("start_time: " + str(start_time) + " endTime: " + str(end_time))
    test = Visual(file_path, start_time, end_time)
    test.plot_continuous(['package_0', 'dram_0', 'core_0', 'uncore_0'])

pass