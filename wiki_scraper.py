import sys

def read_arg(input_data):
    assert (input_data["counter"] < len(input_data["args"]))
    input_data["counter"] += 1

    return input_data["args"][input_data["counter"] - 1]





def look_for_arg(input_data, arg):
    if input_data["counter"] < len(input_data["args"]) and input_data["args"][input_data["counter"]] == arg:
        input_data["counter"] += 1  # skip the --arg
        return True
    return False

def parse_input(input_args):
    input_data = {
        "counter" : 1,
        "args" : input_args
    }

    return_dict = {
        "summary" : None,
        "table" : None,
        "count-words" : None,
        "anal-relat-word-freq" : None,
        "auto-count" : None
    }

    while input_data["counter"] < len(input_args):
        new_arg = read_arg(input_data)

        if new_arg == '--summary':
            return_dict["summary"] = read_arg(input_data)

        elif new_arg == '--table':
            table_dict = {
                "phrase" : read_arg(input_data),
                "number" : 1,
                "first-row-is-header" : False
            }

            if look_for_arg(input_data, '--number'):
                table_dict["number"] = read_arg(input_data)

            if look_for_arg(input_data, '--first-row-is-header'):
                table_dict["first-row-is-header"] = True

            return_dict["table"] = table_dict

        elif new_arg == '--count-words':
            return_dict["count-words"] = read_arg(input_data)

        elif new_arg == "--analyze-relative-word-frequency":
            anal_relative_freq_dict = {
                "mode" : None,
                "chart" : None
            }
            if look_for_arg(input_data, '--mode'):
                anal_relative_freq_dict["mode"] = read_arg(input_data)
            if look_for_arg(input_data, '--chart'):
                anal_relative_freq_dict["chart"] = read_arg(input_data)

            return_dict["anal-relat-word-freq"] = anal_relative_freq_dict

        elif new_arg == '--auto-count-words':
            auto_count_dict = {
                "phrase" : read_arg(input_data),
                "depth" : 1,
                "time" : 0
            }
            if look_for_arg(input_data, '--depth'):
                auto_count_dict["depth"] = read_arg(input_data)
            if look_for_arg(input_data, '--time'):
                auto_count_dict["time"] = read_arg(input_data)

            return_dict["auto-count"] = auto_count_dict

    return return_dict




if __name__ == "__main__":
    parse_input(sys.argv)

