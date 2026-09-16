<div align="center">

# 💻 Problem Solving Hub

<p align="center">
  <b>A structured multi-language repository dedicated to C Programming, Advanced Algorithms, and PostgreSQL Database Management Systems.</b><br>
  Department of Computer Science & Engineering (CSE) <br> Begum Rokeya University, Rangpur (BRUR)
</p>

[![C](https://img.shields.io/badge/Language-C-A8B9CC?style=flat-square&logo=c&logoColor=white)](https://en.wikipedia.org/wiki/C_(programming_language))
[![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Course: CSE 2201](https://img.shields.io/badge/Course-CSE%202201%20(Algo)-blue?style=flat-square)](#-curriculum--focus-areas)
[![Course: CSE 2203](https://img.shields.io/badge/Course-CSE%202203%20(DBMS)-316192?style=flat-square)](#-curriculum--focus-areas)
[![Workflow](https://img.shields.io/badge/Tracker-GitHub%20Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)](#-progress-tracker)
[![Author](https://img.shields.io/badge/Author-With--ALIF-181717?style=flat-square&logo=github)](https://github.com/With-ALIF)


</div>

---

## 📌 Overview

This repository serves as a centralized, production-grade archive for coursework, university lab assignments, algorithmic problem-solving, and database engineering. Each solution is implemented with clean coding standards, modular structure, and clear documentation to foster deep conceptual mastery.

### Key Objectives
- **Algorithmic Rigor:** Implement foundational and advanced data structures and algorithms from scratch in ANSI C.
- **Relational Mastery:** Design optimized schemas, write complex queries, and utilize PostgreSQL-specific features for DBMS problem-solving.
- **Reproducibility:** Maintain standalone, easily executable source files paired with dedicated module guides.

---

## 📂 Repository Structure

```yaml
./
├── .github/
│   └── workflows/
│       └── update-problem-count.yml   # Automated progress sync workflow
│ 
├── DSA/                               # Data Structure & Algorithm (CSE 2201)
│   ├── readme.md                      # Detailed C environment & run instructions
│   └── ...                            # Unit scripts & lab exercises
│ 
├── DBMS/                              # Database Management Systems (CSE 2203)
│   ├── readme.md                      # Detailed PostgreSQL CLI & helper setup
│   └── ....                           # Schema definitions, procedures & queries
│ 
└── README.md                          # Repository hub documentation
```

| Directory | Course / Domain | Technology |
| :--- | :--- | :--- |
| [`/DSA`](./DSA) | **DSA** (`CSE 2201`) | C (GCC) |
| [`/DBMS`](./DBMS) | **DBMS** (`CSE 2203`) | PostgreSQL |

---

## 🎯 Curriculum & Focus Areas

### 1. Data Structure & Algorithm (`CSE 2201`)


- **Core Fundamentals:** Pointers, dynamic memory allocation (`malloc`, `free`), memory management, and file I/O.
- **Linear Data Structures:** Singly & doubly linked lists, stacks, queues, and circular buffers.
- **Non-Linear Data Structures:** Binary trees, Binary Search Trees (BST), AVL trees, heaps, and graph representations.
- **Algorithmic Paradigms:**
  - *Sorting & Searching:* Merge Sort, Quick Sort, Heap Sort, Binary Search.
  - *Divide & Conquer and Greedy:* Fractional Knapsack, Activity Selection.
  - *Dynamic Programming:* Longest Common Subsequence (LCS), 0/1 Knapsack, Matrix Chain Multiplication.
  - *Graph Algorithms:* BFS, DFS, Dijkstra, Kruskal, and Prim.


### 2. Database Management Systems (`CSE 2203`)

- **Data Definition Language (DDL):** Schema architecture, tables, constraints (`PRIMARY KEY`, `FOREIGN KEY`, `CHECK`, `UNIQUE`), and domain types.
- **Data Manipulation Language (DML):** Advanced inserts, bulk operations, upserts (`ON CONFLICT`), cascading updates, and transactions.
- **Data Query Language (DQL):** Multi-table joins (Inner, Outer, Cross, Self), grouping sets, aggregations, and subqueries.
- **Advanced PostgreSQL:**
  - Common Table Expressions (CTEs) & Recursive CTEs.
  - Window Functions (`ROW_NUMBER`, `RANK`, `LEAD`, `LAG`).
  - Stored Procedures, User-Defined Functions (PL/pgSQL), and Index Optimization (B-Tree, Hash).

---

## ⚡ Quick Start Guide

### 1. Clone the Repository

```yaml
# Clone the repository
git clone https://github.com/With-ALIF/problem-solving-hub.git

# Navigate into project directory
cd problem-solving-hub
```

### 2. Running C Programs

Using **GCC** via terminal:

```yaml
# Compile
gcc C/test/hello.c -o hello

# Execute
./hello
```

### 3. Executing SQL Queries

Using **PostgreSQL CLI (`psql`)**:

```yaml
# Execute script directly against database
psql -U postgres -d practice -f SQL/test/sum.sql
```

---

## 📊 Progress Tracker

The table below is automatically updated on every push via `GitHub Actions` based on committed solution files.

<!-- PROBLEM_COUNT_START -->
<table>
  <thead>
    <tr>
      <th align="left">Language</th>
      <th align="center">Solved</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>C</td>
      <td align="center">1</td>
    </tr>
    <tr>
      <td>SQL</td>
      <td align="center">7</td>
    </tr>
    <tr>
      <td><b>Total</b></td>
      <td align="center"><b>8</b></td>
    </tr>
  </tbody>
</table>
<!-- PROBLEM_COUNT_END -->

---

## 🤝 Contributing

Contributions, feedback, and optimization suggestions are welcome:

1. **Fork** the repository.
2. **Clone your fork:**
   ```yaml
   git clone https://github.com/With-ALIF/problem-solving-hub.git
   cd problem-solving-hub
   ```
3. **Create a feature branch:**
   ```yaml
   git checkout -b feature/improved-solution
   ```
4. **Commit your changes:**
   ```yaml
   git commit -m "feat(C): optimize binary search implementation"
   ```
5. **Push to the branch:**
   ```yaml
   git push origin feature/improved-solution
   ```
6. **Open a Pull Request** with a detailed explanation of your changes.

---

## 👨‍💻 Author

<table border="0">
  <tr>
    <td width="80" align="center" valign="middle">
      <img src="https://github.com/With-ALIF.png?size=100" width="80" height="80" style="border-radius: 50%;" alt="Abdullah Al Khalid Alif" />
    </td>
    <td>
      <b>Abdullah Al Khalid Alif</b><br>
      Undergraduate Student, Department of Computer Science & Engineering (CSE)<br>
      <b>Begum Rokeya University, Rangpur (BRUR)</b><br>
    </td>
  </tr>
</table>

---

<div align="center">
  <sub>Maintained for academic & professional growth • If you find this helpful, give it a ⭐!</sub>
</div>