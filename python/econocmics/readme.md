# 📊 Economics Revision Note Generator

A Python-based document generator that compiles a comprehensive, beautifully styled 15-page **Economics Revision Note** PDF tailored for BRUR CSE. The document includes foundational concepts, formulas, tables, curves, diagrams, and quick-revision cheat sheets for exams.

---

## 📂 File Directory & Overview

| File Name | Description | Key Libraries |
| :--- | :--- | :--- |
| [`main.py`](./main.py) | Generates the complete 15-page Economics revision note (`Economics_Revision_15pages.pdf`). | `reportlab`, `math` |
| [`Economics_Revision_15pages.pdf`](./Economics_Revision_15pages.pdf) | The compiled PDF ready for print and revision. | — |

---

## 🛠️ Prerequisites & Installation

To run the script, ensure you have Python 3 and the `reportlab` library installed.

### Option A: WSL / Linux (Ubuntu)

```bash
# 1. Update package lists
sudo apt update

# 2. Install Python and ReportLab
sudo apt install python3 python3-pip python3-reportlab -y
```

*Or via pip inside a Virtual Environment:*
```bash
python3 -m venv venv
source venv/bin/activate
pip install reportlab
```

### Option B: Windows (Command Prompt / PowerShell)

```bash
pip install reportlab
```

---

## 🚀 Usage & Execution

Run the script to build the PDF:

- **WSL:**
  ```bash
  python3 main.py
  ```
- **Windows:**
  ```bash
  python main.py
  ```

Upon completion, you will see `built` in the console, and **`Economics_Revision_15pages.pdf`** will be generated in the same directory.

---

## 📑 15-Page Content Breakdown

| Page | Topic | Key Concepts Covered |
| :---: | :--- | :--- |
| **1** | Ten Principles of Economics | Scarcity, Opportunity Cost, Rational Decision Making, Market Mechanisms |
| **2** | Thinking Like an Economist | Scientific Method, Assumptions, PPF Curve, Positive vs. Normative Statements |
| **3** | Interdependence & Gains from Trade | Absolute Advantage, Comparative Advantage, Opportunity Cost in Trade |
| **4** | Market Forces: Supply & Demand | Law of Demand, Law of Supply, Demand/Supply Schedules & Curves |
| **5** | Market Equilibrium & Shifts | Equilibrium Price/Quantity, Surplus/Shortage, Shifts vs. Movements, 3-Step Analysis |
| **6** | Elasticity (Fundamentals) | Price Elasticity of Demand (PED), Midpoint Method, Elasticity Types |
| **7** | Elasticity (Advanced & Applications) | Total Revenue Test, Income Elasticity, Cross-Price Elasticity, Supply Elasticity |
| **8** | Market Efficiency & Welfare | Consumer Surplus (CS), Producer Surplus (PS), Market Efficiency Benchmark |
| **9** | Market Failure & Deadweight Loss | Efficiency Loss, Underproduction, Overproduction, Market Imperfections |
| **10** | Costs of Taxation | Tax Incidence, Tax Wedge, Deadweight Loss (DWL) Determinants, Laffer Curve |
| **11** | Theory of Production & Costs | Explicit/Implicit Costs, Economic Profit, Production Function, Law of Diminishing Returns |
| **12** | Cost Curves (Short & Long Run) | FC, VC, TC, AFC, AVC, ATC, Marginal Cost (MC), Economies & Diseconomies of Scale |
| **13** | Competitive Markets | Perfect Competition Characteristics, Profit Maximization ($MR = MC$), Shutdown vs. Exit |
| **14** | Monopoly & Market Power | Barriers to Entry, Monopoly Pricing, Deadweight Loss, Price Discrimination |
| **15** | Quick Exam Cheat-Sheet | High-Yield Formulas, Shift Rules, Core Definitions & Exam Tips |
