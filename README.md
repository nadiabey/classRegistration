# classRegistration

This project analyzes roughly how long it takes for classes to fill up during the fall 2021 registration window.

1. Search DukeHub by department and scrape HTML for class enrollment numbers in Python (registration2.py).
2. Clean (line up columns, split section values) and merge raw data for individual departments in Tableau Prep.
3. Iterate through list of class numbers by department for course names and topics if applicable (class_name.py). Insert columns into preexisting file.
4. Split course name values.
5. Visualize data by department.
