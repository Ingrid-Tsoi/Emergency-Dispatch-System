# Task 2 – Heap and Heap Sort

## Overview

This task studies the Heap data structure and Heap Sort algorithm.
They are implemented in Python and used in Task 1.

## Important Note

The heap implementation is shared with Task 1.
All files must be placed in the same folder to run the system correctly.

## Data Structure: Max Heap

A Max Heap is a complete binary tree where each parent node is greater than its children.

### Operations

* push
* pop
* heapify
* build heap

### Application

Used as a priority queue for incident dispatching.

## Algorithm: Heap Sort

### Steps

1. Build max heap
2. Extract maximum repeatedly

### Time Complexity

* O(n log n)

### Space Complexity

* O(n)

## Implementation

```
heap_structure.py
```

## Usage in Project

* Sort incidents
* Dispatch highest priority first
