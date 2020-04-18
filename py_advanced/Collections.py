# Demonstrate the usage of Counter objects
from collections import Counter
# Demonstrate the usage of defaultdict object
from collections import defaultdict
# deque objects are like double-ended queues
import collections
import string
# Demonstrate the usage of namdtuple objects

# Demonstrate the usage of OrderedDict objects
from collections import OrderedDict

def main():
    # list of students in class 1
    class1 = ["Bob", "James", "Chad", "Darcy", "Penny", "Hannah"
              "Kevin", "James", "Melanie", "Becky", "Steve", "Frank"]

    # list of students in class 2
    class2 = ["Bill", "Barry", "Cindy", "Debbie", "Frank",
              "Gabby", "Kelly", "James", "Joe", "Sam", "Tara", "Ziggy"]

    # Create a Counter for class1 and class2
    c1 = Counter(class1)
    c2 = Counter(class2)

    # How many students in class 1 named James?
    print(c1["James"])

    # How many students are in class 1?
    print(sum(c1.values()), "students in class 1")

    # Combine the two classes
    c1.update(class2)
    print(sum(c1.values()), "students in class 1 and 2")

    # What's the most common name in the two classes?
    print(c1.most_common(3))

    # Separate the classes again
    c1.subtract(class2)
    print(c1.most_common(1))

    # What's common between the two classes?
    print(c1 & c2)

    # define a list of items that we want to count
    fruits = ['apple', 'pear', 'orange', 'banana',
              'apple', 'grape', 'banana', 'banana']

    # use a dictionary to count each element
    fruitCounter = defaultdict(int)

    # Count the elements in the list
    for fruit in fruits:
        fruitCounter[fruit] += 1

    # print the result
    for (k, v) in fruitCounter.items():
        print(k + ": " + str(v))


    # initialize a deque with lowercase letters
    d = collections.deque(string.ascii_lowercase)

    # deques support the len() function
    print("Item count: " + str(len(d)))

    # deques can be iterated over
    for elem in d:
        print(elem.upper(), end=",")

    # manipulate items from either end
    d.pop()
    d.popleft()
    d.append(2)
    d.appendleft(1)
    print(d)

    # rotate the deque
    print(d)
    d.rotate(1)
    print(d)

    # create a Point namedtuple
    Point = collections.namedtuple("Point", "x y")

    p1 = Point(10, 20)
    p2 = Point(30, 40)

    print(p1, p2)
    print(p1.x, p1.y)

    # use _replace to create a new instance
    p1 = p1._replace(x=100)
    print(p1)

    # list of sport teams with wins and losses
    sportTeams = [("Royals", (18, 12)), ("Rockets", (24, 6)), 
                ("Cardinals", (20, 10)), ("Dragons", (22, 8)),
                ("Kings", (15, 15)), ("Chargers", (20, 10)), 
                ("Jets", (16, 14)), ("Warriors", (25, 5))]

    # sort the teams by number of wins
    sortedTeams = sorted(sportTeams, key=lambda t: t[1][0], reverse=True)

    # create an ordered dictionary of the teams
    teams = OrderedDict(sortedTeams)
    print(teams)

    # Use popitem to remove the top item
    tm, wl = teams.popitem(False)
    print("Top team: ", tm, wl)

    # What are next the top 4 teams?
    for i, team in enumerate(teams, start=1):
        print(i, team)
        if i == 4:
            break

    # test for equality
    a = OrderedDict({"a": 1, "b": 2, "c": 3})
    b = OrderedDict({"a": 1, "c": 3, "b": 2})
    print("Equality test: ", a == b)



if __name__ == "__main__":
    main()
