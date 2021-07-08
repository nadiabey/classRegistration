# classRegistration

This project analyzes roughly how long it takes for classes to fill up during the fall 2021 registration window.

1. Search DukeHub by department and scrape HTML for class enrollment numbers in Python (registration2.py).
2. Wildcard union raw data for individual departments in Tableau Prep.
3. Iterate through list of class numbers by department for course names and topics if applicable (class_name.py).
4. Join course names to other data.
5. Clean data (line up columns, split section values, split course name values) (finaldata.csv)
6. Visualize data by department.
