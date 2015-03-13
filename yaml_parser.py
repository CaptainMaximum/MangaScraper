import yaml
import sys

required_input = ["name", "url", "volumes"]
valid_extras = []

def get_yaml_dict(filename):
    try:
        stream = open(filename, "r")
        return yaml.safe_load(stream)
    except IOError:
        return None

def find_missing_params(yaml_dict):
    return ([x for x in required_input if x not in yaml_dict.keys()])

def main():
    # Get file name
    if len(sys.argv) < 2:
        print "No .yaml file entered"
        sys.exit(-1)
    filename = sys.argv[1]

    # get yaml details
    yaml_dict = get_yaml_dict(filename)
    if not yaml_dict:
        print "Could not open: '%s'.  Is the file name correct?" % filename
        sys.exit(-1)
    print yaml_dict
    # validate yaml parameters
    missing_params = find_missing_params(yaml_dict)
    if missing_params:
        print "Invalid .yaml file: missing required parameters: %s" % str(missing_params)
        sys.exit(-1)

if __name__ == "__main__":
    main()