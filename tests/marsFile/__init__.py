import base64
import base58
class _:
    version = '1.3.1'
    supported = ['1.3', '1.3.1']

class Section:
    def __init__(self, name):
        self.name = name
        self.entries = []

    def add_entry(self, entry):
        self.entries.append(entry)

class Entry:
    def __init__(self, ident, value):
        self.ident = ident
        self.value = value

def parse(filePathP): 
    """
    Args:
        filePathP (str): Relative path to a MFC/MFC-Stylized file.

    Returns:
        data: Data block from MFC/MFC-Stylized file.
    """
    sections = []
    current_section = None

    with open(filePathP, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if "`" in line and not line.startswith('`'):
                    raise ValueError("\n---\nERROR: Invalid comment: \'%s\' in line %s\n---" % (line, line_number))
            elif line.startswith('`'):
                pass
            elif line.startswith("$<") and line.endswith(">"):
                if line_number == 1:
                    extracted_version = line.split('$<')[1].split('>')[0]
                    if extracted_version not in _.supported:
                        raise ValueError("\n---\nERROR: Unsupported file version: %s.\nSupported file versions: %s\nCurrent module version: %s\n---" % (extracted_version, _.supported, _.version))
                else:
                    raise ValueError("\n---\nERROR: Invalid version tag position: \'%s\' in line %s. Should be 1.\n---" % (line, line_number))
            elif line.startswith('['):
                if line.startswith('[e~'):
                    end_section_name = line.split('[e~')[1].split(']')[0]
                    if current_section.name == end_section_name:
                        current_section = None
                    else:
                        raise ValueError("\n---\nERROR: Missing/Mismatched header: \'%s\' in line %s\n---" % (line, line_number))
                        
                elif line.startswith('[s~'):
                    if current_section is None:
                        section_name = line.split('[s~')[1][:-1]
                        current_section = Section(section_name)
                        sections.append(current_section)

            elif line.startswith('{'):
                if current_section is None:
                    raise ValueError("\n---\nERROR: Invalid formatting: \'%s\' in line %s\n---" % (line, line_number))

                ident, rest = line[1:].split('~')
                name, value = rest.split('/')
                value = value[:-1]

                if ident == 'sS':
                    entry = Entry(name, str(value))
                elif ident == 'sI':
                    entry = Entry(name, int(value))
                elif ident == 'sF':
                    entry = Entry(name, float(value))
                elif ident == "sB":
                    entry = Entry(name, bool(value))
                elif ident == 'sL':
                    value = value.split(';')
                    entry = Entry(name, value)
                elif ident == 'bF':
                    try:
                        entry = Entry(name, base58.b58decode(value))
                    except TypeError:
                        raise ValueError("\n---\nERROR: Invalid BASE58: \'%s\' in line %s" % (line, line_number))
                elif ident == 'bU':
                    try:
                        entry = Entry(name, base58.b58decode(value[1:]))
                    except TypeError:
                        raise ValueError("\n---\nERROR: Invalid BASEURL: \'%s\' in line %s" % (line, line_number))
                    except UnicodeDecodeError:
                        raise ValueError("\n---\nERROR: Invalid BASEURL: \'%s\' in line %s" % (line, line_number))
                elif ident == 'bS':
                    try:
                        entry = Entry(name, base64.b64decode(value))
                    except TypeError:
                        raise ValueError("\n---\nERROR: Invalid BASE64: \'%s\' in line %s" % (line, line_number))
                else:
                    raise ValueError("\n---\nERROR: Invalid identification: \'%s\' in line %s\n---" % (ident, line_number))
                if current_section is None:
                    current_section = Section(None)
                    current_section.add_header(current_section)
                current_section.add_entry(entry)
            else:
                raise ValueError("\n---\nERROR: Invalid syntax: \'%s\' in line %s\n---" % (line, line_number))
    return sections

class lookUp:
    def _(file: str, sectionName: str, entryName: str):
        data = parse(file)
        for section in data:
            if section.name == sectionName:
                for entry in section.entries:
                    if isinstance(entry, Entry) and entry.ident == entryName:
                        if entry.value is None or entry.value == "None":
                            raise ValueError("\n---\nERROR: Value is None!\n---")
                        else:
                            return entry.value

    def sS(file: str, sectionName: str, entryName: str):
        return str(lookUp._(file, sectionName, entryName))
    
    def sI(file: str, sectionName: str, entryName: str):
        return int(lookUp._(file, sectionName, entryName))

    def sF(file: str, sectionName: str, entryName: str):
        return float(lookUp._(file, sectionName, entryName))
    
    def sB(file: str, sectionName: str, entryName: str):
        return bool(lookUp._(file, sectionName, entryName))

    def sL(file: str, sectionName: str, entryName: str):
        return lookUp._(file, sectionName, entryName)

    def bS(file: str, sectionName: str, entryName: str, inBytes: bool = True):
        data = parse(file)
        for section in data:
            if section.name == sectionName:
                for entry in section.entries:
                    if isinstance(entry, Entry) and entry.ident == entryName:
                        if entry.value is None or entry.value == "None":
                            raise ValueError("\n---\nERROR: Value is None!\n---")
                        else:
                            if inBytes:
                                return entry.value
                            elif not inBytes:
                                try:
                                    return entry.value.decode('UTF-8')
                                except AttributeError:
                                    return entry.value
                                except UnicodeDecodeError:
                                    raise ValueError("\n---\nERROR: Invalid BASE64: \'%s\'" % entry.value)
                            else:
                                raise ValueError("\n---\nERROR: Invalid BOOL value: %s\n---" % inBytes)
    
    def bF(file: str, sectionName: str, entryName: str, inBytes: bool = True):
        data = parse(file)
        for section in data:
            if section.name == sectionName:
                for entry in section.entries:
                    if isinstance(entry, Entry) and entry.ident == entryName:
                        if entry.value is None or entry.value == "None":
                            raise ValueError("\n---\nERROR: Value is None!\n---")
                        else:
                            if inBytes:
                                return entry.value
                            elif not inBytes:
                                try:
                                    return entry.value.decode('UTF-8')
                                except AttributeError:
                                    return entry.value
                                except UnicodeDecodeError:
                                    raise ValueError("\n---\nERROR: Invalid BASE58: \'%s\'" % entry.value)
                            else:
                                raise ValueError("\n---\nERROR: Invalid BOOL value: %s\n---" % inBytes)

    def bU(file: str, sectionName: str, entryName: str):
        data = parse(file)
        for section in data:
            if section.name == sectionName:
                for entry in section.entries:
                    if isinstance(entry, Entry) and entry.ident == entryName:
                        if entry.value is None or entry.value == "None":
                            raise ValueError("\n---\nERROR: Value is None!\n---")
                        else:
                            try:
                                return entry.value.decode('UTF-8')
                            except AttributeError:
                                return entry.value
                            except UnicodeDecodeError:
                                raise ValueError("\n---\nERROR: Invalid BASEURL: \'%s\'" % entry.value)

def override(filePathO: str, section_name: str, entry_name: str, new_value):
    with open(filePathO, 'r') as file:
        lines = file.readlines()
    entry_found = False

    for i, line in enumerate(lines):
        if line.strip().startswith('{') and entry_name in line:
            if line.split("~")[0][-1:] == 'b':
                try:
                    new_value = base64.b64encode(new_value)
                    lines[i] = "{%s~%s/%s}\n" % (line.split("~")[0][-1:],entry_name,new_value.decode('UTF-8'))
                except TypeError:
                    raise ValueError("\n---\nERROR: Not a valid BASE64: %s" % new_value)
                entry_found = True
                break
            elif line.split("~")[0][-1:] == 'c':
                mars_list = ""
                for obj in new_value:
                    mars_list = mars_list+obj+";"
                lines[i] = "{%s~%s/%s}\n" % (line.split("~")[0][-1:],entry_name,mars_list[:-1])
                entry_found = True
                break
            else:
                lines[i] = "{%s~%s/%s}\n" % (line.split("~")[0][-1:],entry_name,new_value)
                entry_found = True
                break
                

    if entry_found:
        with open(filePathO, 'w') as file:
            file.writelines(lines)
    else:
        raise ValueError("\n---\nERROR: Entry mismatched/missing!\n---")