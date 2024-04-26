import sys
from heapq import heappush, heappop

from utils import parse_constraints, read_yaml_file, pretty_print_timetable

"""
Constrangerile:
Constrângerile hard sunt de ordin fizic sau logistic, s, i, o dată încălcate, produc
orare imposibil de urmat:
• într-un interval orar s, i într-o sala se poate sust, ine o singură materie de către
un singur profesor.
• într-un interval orar, un profesor poate t, ine o singură materie, într-o singură
sală.
• un profesor poate t, ine ore în maxim 7 intervale pe săptămână.
• o sală permite într-un interval orar prezent,a unui număr de student, i mai mic
sau egal decât capacitatea ei maximă specificată.
• tot, i student, ii de la o materie trebuie să aibă alocate ore la acea materie.
Concret, suma capacităt, ilor sălilor peste toate intervalele în care se t, in ore la
materia respectivă trebuie să fie mai mare sau egală decât numărul de student, i
la materia respectivă. (vezi Exemplu mai sus)
• tot, i profesorii predau doar materiile pe care sunt specializat, i.
• în toate sălile se t, in ore doar la materiile pentru care este repartizată sala.
1.2 Constrângeri încălcabile / soft
Constrângerile soft se referă la preferint,ele profesorilor. Este preferabil să încălcăm
constrângeri soft dacă acest lucru va genera un orar valid, decât să ajungem în
imposibilitatea de a completa orarul.
Constrângerile profesorilor pot fi de următoarele tipuri:
• Preferă anumite zile sau nu doresc să predea într-o zi anume.
– Exemplu:
Luni → profesorul preferă să predea Luni
!Mart, i → profesorul preferă să nu predea mart, i
• Preferă sau nu doresc anumite intervale orare, în oricare din zile
– Exemplu:
8-12 → profesorul preferă să predea în oricare dintre intervalele 8-10 sau
10-12
!14-20 → profesorul preferă să nu predea în intervalele 14-16, 16-18, 18-20
• [bonus] Preferă să nu aibă ferestre în orar mai mari de X ore
– Exemplu:
!Pauză > 0 → profesorul nu dores,te nicio pauză în orarul său
!Pauza > 2 → profesorul nu vrea ferestre mai mari de 2 ore
"""


class TimetableState:
    def __init__(self, intervals, days, subjects, teacher_availability,
                 room_capacity_and_subjects, teacher_subjects, schedule=None):
        self.intervals = intervals
        self.days = days
        self.subjects = subjects
        self.teacher_availability = teacher_availability
        self.room_capacity_and_subjects = room_capacity_and_subjects
        self.teacher_subjects = teacher_subjects
        self.rooms = list(room_capacity_and_subjects.keys())
        self.schedule = schedule if schedule is not None else self.initialize_schedule()

    def initialize_schedule(self):
        schedule = {}
        for day in self.days:
            schedule[day] = {}
            for interval in self.intervals:
                schedule[day][interval] = {}
                for room in self.rooms:
                    schedule[day][interval][
                        room] = None  # in future it will be tupluri (profesor, materie)
        return schedule

    def is_complete(self):
        # we can check if all values from subjects are 0
        # if they are 0, then we have a complete schedule
        print("Subjects: ", self.subjects)
        return all(value == 0 for value in self.subjects.values())

    def assign_subject_teacher(self, room, day, interval, subject, teacher):
        print("Assigning subject to teacher in room: ", room, day, interval, subject, teacher)
        self.schedule[day][interval][room] = (teacher, subject)
        print("Schedule: ", self.schedule)
        self.subjects[subject] -= self.room_capacity_and_subjects[room][0]
        # remove interval from teacher availability
        self.teacher_availability[teacher][day].remove(interval)

    def get_neighbors(self):
        neighbors = []  # list of timetable states
        # TODO: Implement the function that generates the neighbors of the current state
        # don't generate all possible neighbors, just the ones that are valid
        # a neighbor is a state that is obtained by adding a subject to a room in a timeslot

        # a new neighbor is obtained by adding a subject to a room in a timeslot

        for day in self.days:
            for interval in self.intervals:
                for room in self.rooms:
                    for subject in self.subjects:
                        # check if the room is available
                        if self.schedule[day][interval][room] is not None:
                            continue

                        # check if the subject can be added to the room
                        print("Room capacity: ", self.room_capacity_and_subjects[room][0])
                        print("Subject capacity: ", self.subjects[subject])
                        if self.room_capacity_and_subjects[room][0] <= self.subjects[subject]:
                            # check if the teacher is available
                            teacher = None
                            for teacher in self.teacher_availability:
                                # if teacher teaches the subject and is available
                                if subject in self.teacher_subjects[teacher] and interval in self.teacher_availability[teacher][day]:
                                    teacher = teacher
                                    break
                            print("Teacher: ", teacher)
                            print("Teacher availability: ", self.teacher_availability[teacher])
                            if teacher is not None:
                                # check if the teacher is available to teach the subject
                                if (teacher in self.teacher_availability and
                                        subject in self.teacher_subjects[teacher]):
                                    # assign the subject to the teacher
                                    self.assign_subject_teacher(room, day, interval, subject, teacher)
                                    new_state = TimetableState(self.intervals, self.days, self.subjects,
                                                               self.teacher_availability,
                                                               self.room_capacity_and_subjects, self.teacher_subjects,
                                                               self.schedule)
                                    neighbors.append(new_state)

        return neighbors

    def heuristic(self):

        # it will need to take in consideration the remaining subjects and the teacher availability
        # the heuristic should return a value that represents the cost of the current state
        # the cost should be higher if the state is further from the solution

        cost = 0
        for subject in self.subjects:
            cost += self.subjects[subject]

        for teacher in self.teacher_availability:
            for day in self.days:
                for interval in self.intervals:
                    if interval in self.teacher_availability[teacher][day]:
                        cost += 1

        return cost


def csp(start_state):
    pass


def astar(start_state):
    # Frontier as a list of tuples (cost_f, state)
    frontier = []
    heappush(frontier, (start_state.heuristic(), start_state))

    # Discovered nodes as a dictionary node -> (parent, cost_g-to-node)
    discovered = {start_state: (None, 0)}

    print("Initial state: ", start_state.schedule)
    print("Initial state heuristic: ", start_state.heuristic())
    print("Initial state neighbors: ", len(start_state.get_neighbors()))

    # check if is complete
    if start_state.is_complete():
        print("Initial state is complete")

    # Implement A* algorithm
    while frontier:
        # Get the node with the lowest f from the frontier
        cost_f, current_state = heappop(frontier)

        # Check if the current state is the solution
        if current_state.is_complete():
            return current_state

        # Get the neighbors of the current state
        neighbors = current_state.get_neighbors()

        print("Neighbors: ", len(neighbors))

        # Iterate through the neighbors
        for neighbor in neighbors:
            # Calculate the cost to the neighbor
            cost_g = discovered[current_state][1] + 1
            cost_f = cost_g + neighbor.heuristic()

            # Check if the neighbor is discovered
            if neighbor not in discovered or cost_g < discovered[neighbor][1]:
                # Add the neighbor to the frontier and discovered
                heappush(frontier, (cost_f, neighbor))
                discovered[neighbor] = (current_state, cost_g)

    return None


# Main function to parse command-line arguments and run the algorithm
def main():
    if len(sys.argv) != 3:
        print("Usage: python orar.py [astar|csp] input_file")
        return

    algorithm = sys.argv[1]
    input_file = sys.argv[2]

    timetable_specs = read_yaml_file(input_file)

    (intervals  # ['(8, 10)', '(10, 12)', '(12, 14)', '(14, 16)', '(16, 18)', '(18, 20)']
     , days  # ['Luni', 'Marti', 'Miercuri', 'Joi', 'Vineri']
     , subjects  # {'PA': 330, 'PCom': 330, 'PL': 300}
     , teacher_availability
     # {'Alexandru Popa': {'Luni': [(8, 10), (14, 16), (10, 12), (12, 14), (16, 18), (18, 20)], 'Marti': [(8, 10), (14, 16), (10, 12), (12, 14), (16, 18), (18, 20)], 'Miercuri': [(8, 10), (14, 16), (10, 12), (12, 14), (16, 18), (18, 20)], 'Joi': [(8, 10), (14, 16), (10, 12), (12, 14), (16, 18), (18, 20)], 'Vineri': [(8, 10), (14, 16), (10, 12), (12, 14), (16, 18), (18, 20)]}, 'Andrei Ilie': {'Luni': [(8, 10), (10, 12), (18, 20), (12, 14), (14, 16), (16, 18)], 'Marti': [(8, 10), (10, 12), (18, 20), (12, 14), (14, 16), (16, 18)], 'Miercuri': [(8, 10), (10, 12), (18, 20), (12, 14), (14, 16), (16, 18)], 'Joi': [(8, 10), (10, 12), (18, 20), (12, 14), (14, 16), (16, 18)], 'Vineri': [(8, 10), (10, 12), (18, 20), (12, 14), (14, 16), (16, 18)]}, 'Andrei Ionescu': {'Luni': [(8, 10), (12, 14), (16, 18), (18, 20), (10, 12), (14, 16)], 'Marti': [(8, 10), (12, 14), (16, 18), (18, 20), (10, 12), (14, 16)], 'Miercuri': [(8, 10), (12, 14), (16, 18), (18, 20), (10, 12), (14, 16)], 'Joi': [(8, 10), (12, 14), (16, 18), (18, 20), (10, 12), (14, 16)], 'Vineri': [(8, 10), (12, 14), (16, 18), (18, 20), (10, 12), (14, 16)]}, 'Andrei Moldovan': {'Luni': [(16, 18), (18, 20), (8, 10), (10, 12), (12, 14), (14, 16)], 'Marti': [(16, 18), (18, 20), (8, 10), (10, 12), (12, 14), (14, 16)], 'Miercuri': [(16, 18), (18, 20), (8, 10), (10, 12), (12, 14), (14, 16)], 'Joi': [(16, 18), (18, 20), (8, 10), (10, 12), (12, 14), (14, 16)], 'Vineri': [(16, 18), (18, 20), (8, 10), (10, 12), (12, 14), (14, 16)]}, 'Cristina Dinu': {'Luni': [(8, 10), (12, 14), (14, 16), (18, 20), (10, 12), (16, 18)], 'Marti': [(8, 10), (12, 14), (14, 16), (18, 20), (10, 12), (16, 18)], 'Miercuri': [(8, 10), (12, 14), (14, 16), (18, 20), (10, 12), (16, 18)], 'Joi': [(8, 10), (12, 14), (14, 16), (18, 20), (10, 12), (16, 18)], 'Vineri': [(8, 10), (12, 14), (14, 16), (18, 20), (10, 12), (16, 18)]}, 'Dumitru Moldovan': {'Luni': [(8, 10), (10, 12), (12, 14), (16, 18), (18, 20), (14, 16)], 'Marti': [(8, 10), (10, 12), (12, 14), (16, 18), (18, 20), (14, 16)], 'Miercuri': [(8, 10), (10, 12), (12, 14), (16, 18), (18, 20), (14, 16)], 'Joi': [(8, 10), (10, 12), (12, 14), (16, 18), (18, 20), (14, 16)], 'Vineri': [(8, 10), (10, 12), (12, 14), (16, 18), (18, 20), (14, 16)]}, 'Elena Ionescu': {'Luni': [(8, 10), (10, 12), (12, 14), (18, 20), (14, 16), (16, 18)], 'Marti': [(8, 10), (10, 12), (12, 14), (18, 20), (14, 16), (16, 18)], 'Miercuri': [(8, 10), (10, 12), (12, 14), (18, 20), (14, 16), (16, 18)], 'Joi': [(8, 10), (10, 12), (12, 14), (18, 20), (14, 16), (16, 18)], 'Vineri': [(8, 10), (10, 12), (12, 14), (18, 20), (14, 16), (16, 18)]}, 'Ioana Scarlatescu': {'Luni': [(10, 12), (12, 14), (14, 16), (16, 18), (8, 10), (18, 20)], 'Marti': [(10, 12), (12, 14), (14, 16), (16, 18), (8, 10), (18, 20)], 'Miercuri': [(10, 12), (12, 14), (14, 16), (16, 18), (8, 10), (18, 20)], 'Joi': [(10, 12), (12, 14), (14, 16), (16, 18), (8, 10), (18, 20)], 'Vineri': [(10, 12), (12, 14), (14, 16), (16, 18), (8, 10), (18, 20)]}, 'Madalina Dinu': {'Luni': [(8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20)], 'Marti': [(8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20)], 'Miercuri': [(8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20)], 'Joi': [(8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20)], 'Vineri': [(8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20)]}, 'Madalina Gheorghe': {'Luni': [(8, 10), (10, 12), (12, 14), (14, 16), (18, 20), (16, 18)], 'Marti': [(8, 10), (10, 12), (12, 14), (14, 16), (18, 20), (16, 18)], 'Miercuri': [(8, 10), (10, 12), (12, 14), (14, 16), (18, 20), (16, 18)], 'Joi': [(8, 10), (10, 12), (12, 14), (14, 16), (18, 20), (16, 18)], 'Vineri': [(8, 10), (10, 12), (12, 14), (14, 16), (18, 20), (16, 18)]}, 'Maria Ilie': {'Luni': [(8, 10), (12, 14), (10, 12), (14, 16), (16, 18), (18, 20)], 'Marti': [(8, 10), (12, 14), (10, 12), (14, 16), (16, 18), (18, 20)], 'Miercuri': [(8, 10), (12, 14), (10, 12), (14, 16), (16, 18), (18, 20)], 'Joi': [(8, 10), (12, 14), (10, 12), (14, 16), (16, 18), (18, 20)], 'Vineri': [(8, 10), (12, 14), (10, 12), (14, 16), (16, 18), (18, 20)]}, 'Petru Chiriac': {'Luni': [(8, 10), (10, 12), (14, 16), (16, 18), (18, 20), (12, 14)], 'Marti': [(8, 10), (10, 12), (14, 16), (16, 18), (18, 20), (12, 14)], 'Miercuri': [(8, 10), (10, 12), (14, 16), (16, 18), (18, 20), (12, 14)], 'Joi': [(8, 10), (10, 12), (14, 16), (16, 18), (18, 20), (12, 14)], 'Vineri': [(8, 10), (10, 12), (14, 16), (16, 18), (18, 20), (12, 14)]}, 'Roxana Ilie': {'Luni': [(8, 10), (12, 14), (16, 18), (18, 20), (10, 12), (14, 16)], 'Marti': [(8, 10), (12, 14), (16, 18), (18, 20), (10, 12), (14, 16)], 'Miercuri': [(8, 10), (12, 14), (16, 18), (18, 20), (10, 12), (14, 16)], 'Joi': [(8, 10), (12, 14), (16, 18), (18, 20), (10, 12), (14, 16)], 'Vineri': [(8, 10), (12, 14), (16, 18), (18, 20), (10, 12), (14, 16)]}}
     , room_capacity_and_subjects  # {'ED010': (20, ['PA']), 'ED020': (30, ['PA', 'PCom', 'PL'])}
     , professor_preferred
     # {'Alexandru Popa': {'Luni': [(10, 12), (12, 14), (16, 18), (18, 20)], 'Marti': [(10, 12), (12, 14), (16, 18), (18, 20)], 'Miercuri': [(10, 12), (12, 14), (16, 18), (18, 20)]}, 'Andrei Ilie': {'Luni': [(12, 14), (14, 16), (16, 18)], 'Marti': [(12, 14), (14, 16), (16, 18)], 'Vineri': [(12, 14), (14, 16), (16, 18)]}, 'Andrei Ionescu': {'Joi': [(10, 12), (14, 16)], 'Vineri': [(10, 12), (14, 16)]}, 'Andrei Moldovan': {'Luni': [(8, 10), (10, 12), (12, 14), (14, 16)], 'Marti': [(8, 10), (10, 12), (12, 14), (14, 16)], 'Joi': [(8, 10), (10, 12), (12, 14), (14, 16)], 'Vineri': [(8, 10), (10, 12), (12, 14), (14, 16)]}, 'Cristina Dinu': {'Luni': [(10, 12), (16, 18)], 'Miercuri': [(10, 12), (16, 18)]}, 'Dumitru Moldovan': {'Marti': [(14, 16)]}, 'Elena Ionescu': {'Luni': [(14, 16), (16, 18)], 'Miercuri': [(14, 16), (16, 18)]}, 'Ioana Scarlatescu': {'Miercuri': [(8, 10), (18, 20)], 'Joi': [(8, 10), (18, 20)], 'Vineri': [(8, 10), (18, 20)]}, 'Madalina Dinu': {'Marti': [(18, 20)]}, 'Madalina Gheorghe': {'Vineri': [(16, 18)]}, 'Maria Ilie': {'Luni': [(10, 12), (14, 16), (16, 18), (18, 20)], 'Miercuri': [(10, 12), (14, 16), (16, 18), (18, 20)], 'Joi': [(10, 12), (14, 16), (16, 18), (18, 20)]}, 'Petru Chiriac': {'Luni': [(12, 14)], 'Vineri': [(12, 14)]}, 'Roxana Ilie': {'Luni': [(10, 12), (14, 16)], 'Miercuri': [(10, 12), (14, 16)]}}
     , teacher_subjects
     # {'Alexandru Popa': ['PA', 'PCom'], 'Andrei Ilie': ['PA', 'PL'], 'Andrei Ionescu': ['PCom'], 'Andrei Moldovan': ['PA', 'PL'], 'Cristina Dinu': ['PL', 'PA'], 'Dumitru Moldovan': ['PCom', 'PL'], 'Elena Ionescu': ['PCom', 'PL'], 'Ioana Scarlatescu': ['PL', 'PCom'], 'Madalina Dinu': ['PL'], 'Madalina Gheorghe': ['PL'], 'Maria Ilie': ['PCom', 'PA'], 'Petru Chiriac': ['PCom', 'PL'], 'Roxana Ilie': ['PA', 'PL', 'PCom']}
     ) = parse_constraints(timetable_specs)

    initial_state = TimetableState(intervals, days, subjects, teacher_availability,
                                   room_capacity_and_subjects, teacher_subjects)

    # Run the selected algorithm
    if algorithm == "astar":
        final_state = astar(initial_state)
    elif algorithm == "csp":
        final_state = csp(initial_state)
    else:
        print("Invalid algorithm. Choose 'astar' or 'csp'.")
        return

    # Print the solution
    if final_state is not None:
        print("Solution found:")
        print(final_state.schedule)
        print(pretty_print_timetable(final_state.schedule, input_file))
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
