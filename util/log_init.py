import logging


def log_init():
    log_level = logging.DEBUG
    log_file_path = '/home/yimoning/mcmaster/fall2023/new_simMeasure/_remove/logging/info/'  # Set your log file path here
    log_error_file_path = '/home/yimoning/mcmaster/fall2023/new_simMeasure/_remove/logging/error/'  # Set your error log file path here
    enable_stdout_log = True
    log_format_str = "[%(asctime)s][%(levelname)s][%(process)d][%(module)s.%(funcName)s] %(message)s"
    formatter = logging.Formatter(log_format_str)

    if enable_stdout_log:
        stdout_handle = logging.StreamHandler()
        stdout_handle.setLevel(log_level)
        stdout_handle.setFormatter(formatter)
        logging.getLogger().addHandler(stdout_handle)

    log_handle = logging.FileHandler(log_file_path + 'info.log')
    log_handle.setFormatter(formatter)
    log_handle.setLevel(log_level)

    error_handle = logging.FileHandler(log_error_file_path + 'error.log')
    error_handle.setFormatter(formatter)
    error_handle.setLevel(logging.WARNING)

    logging.getLogger().setLevel(log_level)
    logging.getLogger().addHandler(log_handle)
    logging.getLogger().addHandler(error_handle)
