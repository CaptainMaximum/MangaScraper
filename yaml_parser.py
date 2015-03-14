import yaml
import sys, re

# Function to exit the application with an error
def exit_app(message):
    print "error='" + message + "'"
    sys.exit(-1)

# Returns a dictionary representation of a .yaml file
# @param 'filename' (type=String): .yaml filename
# returns a dictionary if the file is valid, None if the filename does not exist,
#   or -1 if the file is invalid
def dict_from_yaml_file(filename):
    try:
        stream = open(filename, "r")
        return yaml.safe_load(stream)
    except IOError:
        return None
    except yaml.scanner.ScannerError:
        return -1

def find_missing_params(yaml_dict):
    required_input = ["name", "url", "volumes"]
    return ([x for x in required_input if x not in yaml_dict.keys()])

# Safely gets the value out of a dictionary.
# @param 'dictionary' (type=dict): Dictionary to retrieve the value from
# @param 'value' (type=any): Value to search for
# @param 'fail' (type=any): Value to return if 'value' is not in the dictionary
def safe_get_value(dictionary, value, fail = None):
    if value in dictionary.keys():
        return dictionary[value]
    else:
        return fail

# For each volume in the volume dictionary, map that volume to the list of
# chapters in that volume
# @param 'volumes' (type=dict): Maps a string (volume name) to a dictionary of
#   chapters in that volume (start chapter, end chapter, other chapters)
def get_volume_chapters(volumes):
    volume_chapters = {}
    for volume in volumes.keys():
        start_chapter = safe_get_value(volumes[volume], 'start_chapter')
        end_chapter = safe_get_value(volumes[volume], 'end_chapter')
        other_chapters = safe_get_value(volumes[volume], 'other_chapters', fail = [])
        # Error case, user has defined either a start chapter or an end chapter, but not both.
        if (start_chapter == None and end_chapter != None) or (start_chapter != None and end_chapter == None):
            return {"error": volume}
        elif start_chapter == None and end_chapter == None:
            chapter_range = []
        else:
            chapter_range = range(int(start_chapter), int(end_chapter) + 1)
        chapter_range.extend(other_chapters)
        volume_chapters[volume] = chapter_range
    return volume_chapters

# Turn each volume name into a valid bash variable and return a space-delimeted string of all values
# @param 'volume_list' (type=list<String>): List of volumes to be stringified
def stringify_volume_list(volume_list):
    variable_list = ["$" + re.sub(" ", "", str(x)) for x in volume_list]
    variable_string = " ".join(variable_list)
    return "VOLS='" + variable_string + "'"

# Turn the volume-chapter map into a list of strings that represent bash variable assignments
# @param 'volume_chapter_map' (type=dict)
# returns a list of bash variable assignment strings (e.g. ["V1='V1 1 2 3 4'", "V2='V2 5 6 7'", ...])
def chapters_to_bash_assignments(volume_chapter_map):
    ret_array = []
    for v in volume_chapter_map.keys():
        assign_string = re.sub(" ", "", str(v)) + "='*" + str(v) + "* "
        chapter_list = [str(x) for x in volume_chapter_map[v]]
        assign_string += " ".join(chapter_list)
        assign_string += "'"
        ret_array.append(assign_string)
    return sorted(ret_array)

def get_file_name():
    if len(sys.argv) < 2:
        exit_app("No .yaml file entered")
    return sys.argv[1]

def parse_yaml_file(filename):
    yaml_dict = dict_from_yaml_file(filename)
    if not yaml_dict:
        exit_app("Could not open: '%s'.  Is the file name correct?" % filename)
    if yaml_dict == -1:
        exit_app("Error parsing .yaml file")
    return yaml_dict

# Ensures that the yaml file is not missing any parameters
# Exits the application if missing parameters, returns true if good
def validate_yaml_dict(dictionary):
    missing_params = find_missing_params(dictionary)
    if missing_params:
        exit_app('Invalid .yaml file: missing parameters: %s' % missing_params)
    return True

# Takes a yaml dict and turns the volume value and turns it into bash variable
# assignments
def get_assignment_strings(yaml_dict):
    volume_chapter_map = get_volume_chapters(yaml_dict['volumes'])
    if "error" in volume_chapter_map.keys():
        exit_app('Error in chapter definition for volume: %s' % str(volume_chapter_map['error']))
    volume_string = stringify_volume_list(sorted(volume_chapter_map.keys()))
    volume_chapter_strings = chapters_to_bash_assignments(volume_chapter_map)
    return (volume_string, volume_chapter_strings)

# Prints the values out so they may be captured by the script and turned into
# variable assignments
def print_for_capture(name, url, volume_chapters, volume_string):
    print "NAME='" + name + "'"
    print "URL='" + url + "'"
    for chapter_assign in volume_chapters:
        print chapter_assign
    print volume_string


def main():
    filename = get_file_name()
    yaml_dict = parse_yaml_file(filename)
    validate_yaml_dict(yaml_dict)
    volume_string, volume_chapter_strings = get_assignment_strings(yaml_dict)
    print_for_capture(yaml_dict['name'], yaml_dict['url'], volume_chapter_strings, volume_string)

if __name__ == "__main__":
    main()