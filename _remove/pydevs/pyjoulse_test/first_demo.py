# import time
# from pyJoules.energy_meter import measure_energy
# from pyJoules.handler.csv_handler import CSVHandler
# import sys
# sys.path.append("/home/yimoning/util/")
# import singletonFlag as us
# import constants as uc
# # Initialize the CSVHandler to save data to 'energy_consumption.csv'
# # csv_handler = CSVHandler('energy_consumption_run.csv')
# DATA_FOLDER = '/home/yimoning/research/data/'
# csv_handler = CSVHandler(DATA_FOLDER + uc.FILE_NAME)
# # csv_handler = CSVHandler('energy_consumption.csv')
# # Decorate the function to measure its energy consumption
# @measure_energy(handler=csv_handler)
# def measure_energy_for_one_second():
#     time.sleep(1)  # Sleep for one second
#
# if __name__ == '__main__':
#     while not us.Singleton.get_instance().getFlag():
#         # print(us.Singleton.get_instance().getFlag())
#         measure_energy_for_one_second()
#     csv_handler.save_data()
#     us.Singleton.get_instance().flagChange()
