#usr/bin/bash

echo "BIG TEST 1 : TO DETECT POSSIBLE TIMETABLES"
python3 test_sat.py

echo "BIG TEST 2 : TO DETECT IMPOSSIBLE TIMETABLES"
python3 test_unsat.py
