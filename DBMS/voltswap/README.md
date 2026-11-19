# VoltSwap Dhaka — Database Management System

A PostgreSQL database system for **VoltSwap Dhaka**, an automated smart battery-swapping network for electric three-wheelers (e-rickshaws) and electric motorbikes across Dhaka.

---

## 📁 Project Files

| File | Purpose |
| :--- | :--- |
| [`voltswap.sql`](voltswap.sql) | Full DDL schema (23 tables, constraints, CHECKs, FKs, and views) |
| [`test.sql`](test.sql) | Sample seed data & 4 analytical business queries |
| [`erd.mmd`](erd.mmd) | Crow's foot ER diagram in Mermaid format |
| [`Take-Home ERD Assignment Deliver.pdf`](Take-Home%20ERD%20Assignment%20Deliver.pdf) | Assignment problem specification |

---

## 🚀 Setup & Execution

Run the scripts in PostgreSQL using `psql`:

```bash
# 1. Create database
psql -U postgres -c "CREATE DATABASE voltswap_db;"

# 2. Run DDL schema
psql -U postgres -d voltswap_db -f voltswap.sql

# 3. Insert test data & run queries
psql -U postgres -d voltswap_db -f test.sql
```

---

## 📊 Core Analytical Queries (from Assignment)

- **Q1 (Health Degradation):** Identifies batteries with `< 80%` State-of-Health (SOH) that need cell rebalancing or maintenance.
- **Q2 (Peak Depletion):** Detects stations having zero batteries with `SOC ≥ 80%` in slots during peak hours (08:00–11:00 & 17:00–20:00).
- **Q3 (Top Referrers):** Finds drivers with the highest number of successful recruits via the recursive referral hierarchy.
- **Q4 (Swap Audit Trail):** Pulls the complete chronological lifecycle history for battery `VS-B-00917` (both issued and returned).

---

## 🛠️ Key Design Highlights

- **Weak Entities (Composite PKs):**
  - `Cabinet` (owner: `Station`, partial key: `cabinet_number`)
  - `Slot` (owner: `Cabinet`, partial key: `slot_number`)
  - `Telemetry` (owner: `Battery`, partial key: `reading_timestamp`) with `ON DELETE CASCADE`.
- **Specialization / Generalization (Disjoint & Total):**
  - `Vehicle` specializes into `E_Rickshaw` (passenger capacity, permit) and `E_Motorbike` (top speed, delivery flag).
  - `Employee` specializes into `Technician` (certification level) and `Station_Operator` (assigned station 1:1, shift).
- **Dual Battery Roles in Swap:**
  - Each swap records two distinct relationships to `Battery`: `returned_battery` (with depleted charge %) and `issued_battery` (with the source slot).
- **Recursive Referral Relationship:**
  - `Driver` self-references with roles `referrer` (senior mentor) and `referee` (new recruit); self-referrals are blocked via a `CHECK` constraint.
- **Derived Attributes via Dynamic Views:**
  - Driver `age` (computed from `date_of_birth`) and battery `cycle_count` (computed from total swap returns) are handled via views (`v_driver_details`, `v_battery_cycle_count`) instead of redundant physical columns.
- **Polymorphic Payment Arc & History Tracking:**
  - A `CHECK` constraint ensures each payment settles *either* an ad-hoc swap *or* a monthly subscription plan.
  - Temporal tracking on `driver_vehicle_assignment` and `driver_subscription` uses `start_date` and nullable `end_date` to preserve full operational history.
- **ERD Visualization:**
  - Open [`erd.mmd`](erd.mmd) in [mermaid.live](https://mermaid.live) to visualize and download high-resolution SVG/PNG for submission reports.
