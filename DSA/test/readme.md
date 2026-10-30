# 🧪 DSA & C Environment Verification Scripts

This directory contains starter C programs used for verifying compiler installation, testing standard I/O streams, and checking basic arithmetic computation in C.

---

## 📂 File Directory & Overview

| File Name | Topic | Key Concepts | Description |
| :--- | :--- | :--- | :--- |
| [`hello.c`](./hello.c) | Basic Standard Output | `#include <stdio.h>`, `printf()`, `main(void)` | Minimal C program printing `"Hello, World!"` to verify toolchain & compiler setup. |
| [`sum.c`](./sum.c) | Console Input & Arithmetic | `scanf()`, `%d`, Variables, Addition | Takes two integer inputs from standard input and displays their computed sum. |

---

## 🔍 Detailed File Breakdown

### 1. `hello.c` (Toolchain Sanity Check)
- **Purpose:** Smoke test to ensure GCC / MinGW is properly configured in the system PATH and capable of compiling C source code without errors.
- **Workflow:**
  1. Includes the standard input/output header `<stdio.h>`.
  2. Defines the entry point `int main(void)`.
  3. Uses `printf()` to output a greeting string with a newline (`\n`).
  4. Returns `0` indicating successful execution.

### 2. `sum.c` (Interactive User Input & Arithmetic)
- **Purpose:** Demonstrates basic console interaction, reading formatted user inputs using `scanf()`, and performing simple integer arithmetic.
- **Workflow:**
  1. Declares two integer variables `a` and `b`.
  2. Prompts the user to enter the first number and reads it via `scanf("%d", &a)`.
  3. Prompts the user to enter the second number and reads it via `scanf("%d", &b)`.
  4. Calculates `a + b` inline and prints the formatted result.

---