import logging
import os


def log_init():
    # Determine the root directory of the project
    project_root_dir = os.path.dirname(os.path.abspath(__file__))

    # Set the base directory for logging
    base_log_dir = os.path.join(project_root_dir, 'logging')
    info_log_dir = os.path.join(base_log_dir, 'info')
    error_log_dir = os.path.join(base_log_dir, 'error')

    # Create directories if they don't exist
    os.makedirs(info_log_dir, exist_ok=True)
    os.makedirs(error_log_dir, exist_ok=True)

    log_level = logging.DEBUG
    enable_stdout_log = True
    log_format_str = "[%(asctime)s][%(levelname)s][%(process)d][%(module)s.%(funcName)s] %(message)s"
    formatter = logging.Formatter(log_format_str)

    if enable_stdout_log:
        stdout_handle = logging.StreamHandler()
        stdout_handle.setLevel(log_level)
        stdout_handle.setFormatter(formatter)
        logging.getLogger().addHandler(stdout_handle)

    log_handle = logging.FileHandler(os.path.join(info_log_dir, 'info.log'))
    log_handle.setFormatter(formatter)
    log_handle.setLevel(log_level)

    error_handle = logging.FileHandler(os.path.join(error_log_dir, 'error.log'))
    error_handle.setFormatter(formatter)
    error_handle.setLevel(logging.WARNING)

    logging.getLogger().setLevel(log_level)
    logging.getLogger().addHandler(log_handle)
    logging.getLogger().addHandler(error_handle)
