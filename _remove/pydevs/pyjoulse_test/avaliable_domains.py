from pyJoules.device.rapl_device import RaplDevice


def print_available_domains():
    # Get and print all available RAPL domains
    available_domains = RaplDevice.available_domains()
    print("Available RAPL domains:", available_domains)

if __name__ == '__main__':
    print_available_domains()
