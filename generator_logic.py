import csv


WINDOWS_RESERVED_NAMES = (
    {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"}
    | {f"COM{number}" for number in range(1, 10)}
    | {f"LPT{number}" for number in range(1, 10)}
)


def parse_input_line(line):
    line = line.strip()
    if not line:
        return None

    if "," in line:
        try:
            values = next(csv.reader([line], skipinitialspace=True, strict=True))
        except csv.Error as error:
            raise ValueError("Malformed CSV row") from error
        values = [value.strip() for value in values]
    else:
        values = line.split()

    if [value.casefold() for value in values] == ["account", "device"]:
        return None

    if len(values) != 2 or not all(values):
        raise ValueError("Expected an account and a device")

    return values[0], values[1]


def is_valid_device_name(device):
    if not device or device in {".", ".."} or device.endswith((" ", ".")):
        return False

    invalid_characters = '<>:"/\\|?*'
    if any(ord(character) < 32 or character in invalid_characters for character in device):
        return False

    reserved_name = device.split(".", 1)[0].upper()
    return reserved_name not in WINDOWS_RESERVED_NAMES