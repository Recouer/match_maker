import random as rd
import numpy as np


def create_people(number_of_people, ratio):
    peoples = []
    for i in range(number_of_people):
        if i > number_of_people * ratio:
            peoples += [Person("female", "long term")]
            peoples += [Person("male", "long term")]
        else:
            peoples += [Person("female", "one night")]
            peoples += [Person("male", "one night")]

    return peoples


class Match:
    def __init__(self, personality):
        self.personality = personality
        self.time = 1

    def __repr__(self):
        return f"{self.personality} {self.time}"


class Person:
    def __init__(self, gender, personality):
        self.gender = gender
        self.personality = personality
        self.match: list[Match] = []


class Simulation:
    def __init__(self, people, ratio):
        self.free_people: list[Person] = create_people(people, ratio)
        self.matched_people: list[(Person, Person)] = []

    def run_simulation(self, number_of_steps):
        for _ in range(number_of_steps):
            self.step()

    def step(self):
        next_step_free_people = []
        next_step_matched_people = []

        size = len(self.free_people)
        matches = np.zeros((size, size))
        for i, people in enumerate(self.free_people):
            if people.personality == "one night":
                for _ in range(10):
                    matches[i, rd.randrange(0, size)] = 1
            else:
                for _ in range(1):
                    matches[i, rd.randrange(0, size)] = 1

        available_people = [i for i in range(size)]
        for i in range(size):
            if i in available_people:
                for people in available_people:
                    if matches[i, people] == matches[people, i] == 1:
                        if self.free_people[i].gender != self.free_people[people].gender:
                            next_step_matched_people += [(self.free_people[i], self.free_people[people])]
                            available_people.remove(i)
                            available_people.remove(people)
                            self.free_people[i].match.append(Match(self.free_people[people].personality))
                            self.free_people[people].match.append(Match(self.free_people[i].personality))
                            break

        for people in available_people:
            next_step_free_people += [self.free_people[people]]

        for matched in self.matched_people:
            if matched[0].personality == "one night" or matched[1].personality == "one night":
                if rd.random() > 0.01:
                    next_step_free_people += [matched[0]]
                    next_step_free_people += [matched[1]]
                else:
                    next_step_matched_people += [matched]
                    matched[0].match[len(matched[0].match) - 1].time += 1
                    matched[1].match[len(matched[1].match) - 1].time += 1
            else:
                if rd.random() < 0.01:
                    next_step_free_people += [matched[0]]
                    next_step_free_people += [matched[1]]
                else:
                    next_step_matched_people += [matched]
                    matched[0].match[len(matched[0].match) - 1].time += 1
                    matched[1].match[len(matched[1].match) - 1].time += 1

        self.free_people = next_step_free_people
        self.matched_people = next_step_matched_people

    def extract_data(self):
        matches = {}

        matches["female"] = {}
        matches["female"]["one night"] = []
        matches["female"]["long term"] = []

        matches["male"] = {}
        matches["male"]["one night"] = []
        matches["male"]["long term"] = []

        for people in self.free_people:
            matches[people.gender][people.personality] += [people.match]
        for people in self.matched_people:
            matches[people[0].gender][people[0].personality] += [people[0].match]
            matches[people[1].gender][people[1].personality] += [people[1].match]

        matches_long_term = []
        time_long_term = []
        matches_one_night = []
        time_one_night = []
        for people_matches in matches["female"]["long term"]:
            if people_matches:
                matches_long_term += [sum([1 for match in people_matches if match.personality == "long term"])]
                time_long_term += [sum([match.time for match in people_matches if match.personality == "long term"])]
                matches_one_night += [sum([1 for match in people_matches if match.personality == "one night"])]
                time_one_night += [sum([match.time for match in people_matches if match.personality == "one night"])]
            pass

        print(sum(matches_long_term) / len(matches_long_term))
        print(sum(time_long_term) / len(time_long_term))
        print(sum(matches_one_night) / len(matches_one_night))
        print(sum(time_one_night) / len(time_one_night))


if __name__ == "__main__":
    sim = Simulation(100, 0.2)
    sim.run_simulation(1000)
    sim.extract_data()
