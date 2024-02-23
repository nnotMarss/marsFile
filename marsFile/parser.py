def readFile(file_path):
    """
    this doesn't work yet
    """
    data = {}
    current_section = None
    current_parent = None
    current_sub_section = None
    current_depth = 0

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1].strip()
                data[current_section] = {}
                current_depth = 0
                current_parent = None
                current_sub_section = None
            elif line.startswith('\\'):
                depth = line.count('-')
                if depth <= current_depth + 1:
                    current_depth = depth
                    current_parent = None
                    if current_section in data:
                        current_parent = list(data[current_section].keys())[-1]  
                    current_sub_section = line.strip('\\').strip('-').strip()
                    if current_parent is None or current_parent not in data[current_section]:
                        if current_parent is None:
                            data[current_section][current_sub_section] = {}
                        else:
                            if not isinstance(data[current_section][current_parent], dict):
                                data[current_section][current_parent] = {} 
                            data[current_section][current_parent][current_sub_section] = {}
                    else:
                        raise ValueError("Layout syntax error: Subsection already exists")
                else:
                    raise ValueError("Layout syntax error: Subsection depth error")
            elif line.startswith('{') and line.endswith('}'):
                if current_parent is None:
                    data[current_section][line[1:-1].split('~')[0].strip()] = line[1:-1].split('~')[1].strip()
                else:
                    if not isinstance(data[current_section][current_parent], dict):
                        data[current_section][current_parent] = {} 
                    data[current_section][current_parent][line[1:-1].split('~')[0].strip()] = line[1:-1].split('~')[1].strip()
            elif line.startswith('`'):
                continue
            else:
                raise ValueError("Layout syntax error")

    return data

