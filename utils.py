import yaml
import argparse
import sys

##################### MACROURI #####################
INTERVALE = 'Intervale'
ZILE = 'Zile'
MATERII = 'Materii'
PROFESORI = 'Profesori'
SALI = 'Sali'

def read_yaml_file(file_path : str) -> dict:
    '''
    Citeste un fișier yaml și returnează conținutul său sub formă de dicționar
    '''
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def acces_yaml_attributes(yaml_dict : dict):
    '''
    Primește un dicționar yaml și afișează datele referitoare la atributele sale
    '''

    print('Zilele din orar sunt:', yaml_dict[ZILE])
    print()
    print('Intervalele orarului sunt:', yaml_dict[INTERVALE])
    print()
    print('Materiile sunt:', yaml_dict[MATERII])
    print()
    print('Profesorii sunt:', end=' ')
    print(*list(yaml_dict[PROFESORI].keys()), sep=', ')
    print()
    print('Sălile sunt:', end=' ')
    print(*list(yaml_dict[SALI].keys()), sep=', ')


def get_profs_initials(profs : list) -> dict:
    '''
    Primește o listă de profesori

    Returnează două dicționare:
    - unul care are numele profesorilor drept chei și drept valori prescurtările lor (prof_to_initials[prof] = initiale)
    - unul care are prescurtările profesorilor drept chei și drept valori numele lor (initials_to_prof[initiale] = prof)
    '''

    initials_to_prof = {}
    prof_to_initials = {}
    initials_count = {}

    for prof in profs:
        name_components = prof.split(' ')
        initials = name_components[0][0] + name_components[1][0]
        
        if initials in initials_count:
            initials_count[initials] += 1
            initials += str(initials_count[initials])
        else:
            initials_count[initials] = 1
        
        initials_to_prof[initials] = prof
        prof_to_initials[prof] = initials
        
    return prof_to_initials, initials_to_prof


def allign_string_with_spaces(s : str, max_len : int, allignment_type : str = 'center') -> str:
    '''
    Primește un string și un număr întreg

    Returnează string-ul dat, completat cu spații până la lungimea dată
    '''

    len_str = len(s)

    if len_str >= max_len:
        raise ValueError('Lungimea string-ului este mai mare decât lungimea maximă dată')
    

    if allignment_type == 'left':
        s = 6 * ' ' + s
        s += (max_len - len(s)) * ' '

    elif allignment_type == 'center':
        if len_str % 2 == 1:
            s = ' ' + s
        s = s.center(max_len, ' ')

    return s


def pretty_print_timetable_aux_zile(timetable : {str : {(int, int) : {str : (str, str)}}}, input_path : str) -> str:
    '''
    Primește un dicționar ce are chei zilele, cu valori dicționare de intervale reprezentate ca tupluri de int-uri, cu valori dicționare de săli, cu valori tupluri (profesor, materie)

    Returnează un string formatat să arate asemenea unui tabel excel cu zilele pe linii, intervalele pe coloane și în intersecția acestora, ferestrele de 2 ore cu materiile alocate în fiecare sală fiecărui profesor
    '''

    max_len = 30

    profs = read_yaml_file(input_path)[PROFESORI].keys()
    profs_to_initials, _ = get_profs_initials(profs)

    table_str = '|           Interval           |             Luni             |             Marti            |           Miercuri           |              Joi             |            Vineri            |\n'

    no_classes = len(timetable['Luni'][(8, 10)])

    first_line_len = 187
    delim = '-' * first_line_len + '\n'
    table_str = table_str + delim
    
    for interval in timetable['Luni']:
        s_interval = '|'
        
        crt_str = allign_string_with_spaces(f'{interval[0]} - {interval[1]}', max_len, 'center')

        s_interval += crt_str

        for class_idx in range(no_classes):
            if class_idx != 0:
                s_interval += f'|{30 * " "}'

            for day in timetable:
                classes = timetable[day][interval]
                classroom = list(classes.keys())[class_idx]

                s_interval += '|'

                if not classes[classroom]:
                    s_interval += allign_string_with_spaces(f'{classroom} - goala', max_len, 'left')
                else:
                    prof, subject = classes[classroom]
                    s_interval += allign_string_with_spaces(f'{subject} : ({classroom} - {profs_to_initials[prof]})', max_len, 'left')
            
            s_interval += '|\n'
        table_str += s_interval + delim

    return table_str

def pretty_print_timetable_aux_intervale(timetable : {(int, int) : {str : {str : (str, str)}}}, input_path : str) -> str:
    '''
    Primește un dicționar de intervale reprezentate ca tupluri de int-uri, cu valori dicționare de zile, cu valori dicționare de săli, cu valori tupluri (profesor, materie)

    Returnează un string formatat să arate asemenea unui tabel excel cu zilele pe linii, intervalele pe coloane și în intersecția acestora, ferestrele de 2 ore cu materiile alocate în fiecare sală fiecărui profesor
    '''

    max_len = 30

    profs = read_yaml_file(input_path)[PROFESORI].keys()
    profs_to_initials, _ = get_profs_initials(profs)

    table_str = '|           Interval           |             Luni             |             Marti            |           Miercuri           |              Joi             |            Vineri            |\n'

    no_classes = len(timetable[(8, 10)]['Luni'])

    first_line_len = 187
    delim = '-' * first_line_len + '\n'
    table_str = table_str + delim
    
    for interval in timetable:
        s_interval = '|' + allign_string_with_spaces(f'{interval[0]} - {interval[1]}', max_len, 'center')

        for class_idx in range(no_classes):
            if class_idx != 0:
                s_interval += '|'

            for day in timetable[interval]:
                classes = timetable[interval][day]
                classroom = list(classes.keys())[class_idx]

                s_interval += '|'

                if not classes[classroom]:
                    s_interval += allign_string_with_spaces(f'{classroom} - goala', max_len, 'left')
                else:
                    prof, subject = classes[classroom]
                    s_interval += allign_string_with_spaces(f'{subject} : ({classroom} - {profs_to_initials[prof]})', max_len, 'left')
            
            s_interval += '|\n'
        table_str += s_interval + delim

    return table_str

def pretty_print_timetable(timetable : dict, input_path : str) -> str:
    '''
    Poate primi fie un dictionar de zile conținând dicționare de intervale conținând dicționare de săli cu tupluri (profesor, materie)
    fie un dictionar de intervale conținând dictionare de zile conținând dicționare de săli cu tupluri (profesor, materie)
    
    Pentru cazul în care o sală nu este ocupată la un moment de timp, se așteaptă 'None' în valoare, în loc de tuplu
    '''
    if 'Luni' in timetable:
        return pretty_print_timetable_aux_zile(timetable, input_path)
    else:
        return pretty_print_timetable_aux_intervale(timetable, input_path)

def parse_constraints(yaml_data):
    """
    Parse the YAML data and extract constraints into dictionaries.
    """
    # Extract intervals, days, subjects, professors, and rooms
    intervals = yaml_data[INTERVALE]
    days = yaml_data[ZILE]
    subjects = yaml_data[MATERII]
    professors = yaml_data[PROFESORI]
    rooms = yaml_data[SALI]

    # Initialize dictionaries for constraints
    teacher_availability = {}
    room_capacity_and_subjects = {}
    professor_preferred = {}

    # Parse professor constraints
    for professor, info in professors.items():
        preferred = {}
        availability = {}

        for constraint in info['Constrangeri']:
            if isinstance(constraint, str):
                if constraint in days or constraint[1:] in days:
                    if constraint.startswith('!'):
                        day = constraint[1:]
                    else:
                        day = constraint
                        preferred[day] = []
                    availability[day] = []
                else:
                    if constraint.startswith('!'):
                        interval = constraint[1:]
                    else:
                        interval = constraint
                        for day in preferred:
                            preferred[day].append(interval)
                    for day in availability:
                        availability[day].append(interval)

        # Split intervals with differences more than 2 hours
        split_intervals(preferred)
        split_intervals(availability)

        professor_preferred[professor] = preferred
        teacher_availability[professor] = availability

    # Parse room capacities and subjects
    for room, info in rooms.items():
        room_capacity_and_subjects[room] = (info['Capacitate'], info['Materii'])

    return intervals, days, subjects, teacher_availability, room_capacity_and_subjects, professor_preferred


def split_intervals(non_preferred):
    for day in non_preferred:
        updated_intervals = []
        for interval in non_preferred[day]:
            start, end = map(int, interval.split('-'))
            if end - start > 2:
                # Split the interval into two-hour intervals
                for i in range(start, end, 2):
                    updated_intervals.append((i, i + 2))
            else:
                updated_intervals.append((start, end))
        non_preferred[day] = updated_intervals


if __name__ == '__main__':
    import numpy as np

    # Definirea datelor din orar
    days = ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri']
    intervals = [(8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20)]
    subjects = {'PA': 330, 'PCom': 330, 'PL': 300}

    # Definirea tabloului NumPy
    timetable_np = np.empty((len(days), len(intervals)), dtype=object)

    # Umplerea tabloului cu datele orarului
    for i, day in enumerate(days):
        for j, interval in enumerate(intervals):
            timetable_np[i, j] = {
                'profesor': 'Nume profesor',
                'materie': 'Nume materie'
                # alte informații relevante pentru intervalul de timp
            }

    # Afișarea tabloului NumPy
    print(timetable_np)

    # Apelul functiei pretty_print_timetable

#     filename = f'inputs/orar_mic_exact.yaml'
#
    # timetable_specs = read_yaml_file(filename)
#
#     acces_yaml_attributes(timetable_specs)
#
#     (intervals, days, subjects, teacher_availability, room_capacity_and_subjects,
#      professor_preferred) = parse_constraints(timetable_specs)
#
#     print('Intervalele sunt:', intervals)
#     print()
#     print('Zilele sunt:', days)
#     print()
#     print('Materiile sunt:', subjects)
#     print()
#     print('Disponibilitatea profesorilor este:', teacher_availability)
#     print()
#     print('Capacitatile salilor sunt:', room_capacity_and_subjects)
#     print()
#     print('Preferintele profesorilor sunt:', professor_preferred)



    # print(pretty_print_timetable(timetable, filename))
