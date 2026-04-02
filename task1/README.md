# Task 1 – Emergency Dispatch System

## Overview

This project is an Emergency Dispatch System developed in Python using Object-Oriented Programming (OOP).
It simulates how emergency units respond to incidents based on priority.

## Important Note

All Python files must be placed in the same folder when running the program.
Although files are organized into task 1 and task 2 in the repository, execution requires them together.

## Features

* Report incidents with type, location, and severity
* Automatic unit dispatch
* Priority-based handling using Max Heap
* Resolve incidents and track history
* GUI interface using Tkinter

## OOP Concepts

* Encapsulation
* Inheritance
* Abstraction
* Polymorphism

## Project Structure

```
main.py
gui.py
controller.py
models.py
heap_structure.py
```

## Requirements

* Python 3.x
* Tkinter (built-in)

## How to Run

```
python main.py
```

## Usage

1. Select incident details
2. Click "Report Incident"
3. Click "Dispatch Unit"
4. Resolve incidents

## Data Structure

* Max Heap
* Heap Sort

## Notes

* Severity must be 1–5
* Units change status after dispatch/resolution
