# COMP8090 Project – Emergency Dispatch System

## Overview

This repository contains a course project for COMP8090 Data Structures and Algorithms.

The project consists of:

* Task 1: Emergency Dispatch System using Object-Oriented Programming
* Task 2: Implementation of Heap data structure and Heap Sort algorithm

---

## Repository Structure

```
COMP8090-Project/
├── task1/
│   ├── README.md
│   ├── controller.py
│   ├── gui.py
│   ├── main.py
│   ├── models.py
│
├── task2/
│   ├── README.md
│   ├── heap_structure.py
│
└── README.md
```

---

## Important Note

The system requires all Python files to be in the same directory when running.

Before execution, move or copy the following file:

* `heap_structure.py` (from task2/)
  into the task1/ folder.

Final structure for execution:

```
task1/
├── main.py
├── gui.py
├── controller.py
├── models.py
├── heap_structure.py
```

---

## How to Run

1. Ensure all required files are in the same folder (task1/)
2. Run:

```
python main.py
```

---

## Task Summary

### Task 1

* OOP-based system design
* GUI using Tkinter
* Incident management and dispatch logic

### Task 2

* Max Heap data structure
* Heap Sort algorithm
* Used for priority handling in Task 1

---

## Requirements

* Python 3.x
* Tkinter (built-in)

---

## Notes

* Incidents are prioritized by severity and waiting time
* Heap is used as a priority queue for dispatching
