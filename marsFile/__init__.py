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

def parse(file_path):
    sections = []
    current_section = None

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            # Check if the line is a header
            if "`" in line.strip() and not line.startswith('`'):
                    raise ValueError("\n---\nERROR: Invalid comment: \'%s\' in line %s\n---" % (line.strip(), line_number))
            elif line.startswith('`'):
                pass
            elif line.startswith('['):
                if line.startswith('[e~'):
                    end_section_name = line.split('[e~')[1].split(']')[0]  # Extract ender section name
                    if current_section.name == end_section_name:
                        current_section = None
                    else:
                        raise ValueError("\n---\nERROR: Missing/Mismatched header: \'%s\' in line %s\n---" % (line.strip(), line_number))
                        
                elif line.startswith('[s~'):
                    if current_section is None:
                        section_name = line.split('[s~')[1][:-1]  # Extract section name
                        current_section = Section(section_name)
                        sections.append(current_section)  # Append the previous section

            # Check if the line is an entry
            elif line.startswith('{'):
                if current_section is None:
                    raise ValueError("\n---\nERROR: Invalid formatting: \'%s\' in line %s\n---" % (line.strip(), line_number))

                ident, rest = line[1:].split('~')  # Extract identification
                name, value = rest.split('/')  # Extract value name and value
                if ident == 's':
                    entry = Entry(name, value[:-1])
                elif ident == 'c':
                    value = value.split(';')  # Split combo values
                    entry = Entry(name, value[:-1])
                elif ident == 'n':
                    entry = Entry(name, int(value[:-1]))  # Convert value to int for numeric entries
                else:
                    raise ValueError("\n---\nERROR: Invalid identification: \'%s\' in line %s\n---" % (ident, line_number))

                if current_section is None:
                    current_section = Section(None)
                    current_section.add_header(current_section)
                current_section.add_entry(entry)
            else:
                raise ValueError("\n---\nERROR: Invalid syntax: \'%s\' in line %s\n---" % (line.strip(), line_number))
    return sections

def lookUp(file, sectionName, entryName):
    """_summary_

    Args:
        file (_file_): _Takes file path._
        sectionName (_str_): _Takes section name present in given file._
        entryName (_str_): _Takes entry name present in given section, and returns it._

    Returns:
        _str_: _Entry value._
    """
    data = parse(file)
    for section in data:
        if section.name == sectionName:
            for entry in section.entries:
                if isinstance(entry, Entry) and entry.ident == entryName:
                    if entry.value is None or entry.value == "None":
                        raise ValueError("\n---\nERROR: Value is None!\n---")
                    else:
                        return entry.value