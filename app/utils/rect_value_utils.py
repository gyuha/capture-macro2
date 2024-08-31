def is_valid_rect_string_value(value):
    # 1. Check if value is a string
    if not isinstance(value, str):
        return False

    # 2. Split the value by comma
    parts = value.split(",")

    if len(parts) != 4:
        return False

    # 3. Check if each part is a 4-digit number
    for part in parts:
        if not part.isdigit():
            return False

    # 4. All conditions are satisfied
    return True


def string_to_rect_value(value):
    # 1. Split the value by comma
    parts = value.split(",")

    # 2. Convert each part to an integer
    x = int(parts[0])
    y = int(parts[1])
    width = int(parts[2])
    height = int(parts[3])

    # 3. Return the rectangle value
    return x, y, width, height


def rect_str_to_ratio_rect(ratio, value):
    if not is_valid_rect_string_value(value):
        return None
    values = map(int, value.split(","))
    return [int(v * ratio) for v in values]
