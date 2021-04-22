def main():

    from infi.devicemanager import DeviceManager
    import re

    device_manager = DeviceManager()
    device_manager.root.rescan()

    pattern = r"USB Serial Port \(COM(\d)\)"

    for device in device_manager.all_devices:
        try:
            match = re.fullmatch(pattern, device.friendly_name)
        except KeyError:
            continue
        if match is None:
            continue
        com_number = match.group(1)
        print(f"Found device \"{device.friendly_name}\" -> com_number: {com_number}")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())