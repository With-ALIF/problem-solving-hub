\set QUIET on
SET client_min_messages = WARNING;
\pset pager off

-- Clean up existing data and restart serial sequences
TRUNCATE TABLE 
    telemetry,
    maintenance_ticket,
    payment,
    swap,
    station_operator,
    technician_certification,
    technician,
    employee,
    driver_subscription,
    subscription_plan,
    driver_vehicle_assignment,
    driver_phone,
    driver,
    vehicle_battery_compatibility,
    emotorbike,
    erickshaw,
    vehicle,
    battery,
    battery_model,
    slot,
    cabinet,
    station_phone,
    station
RESTART IDENTITY CASCADE;

-- -----------------------------------------------------------------------------
-- 1. POPULATE STATIONS & PHONES (Rule 1)
-- -----------------------------------------------------------------------------
INSERT INTO station (station_id, name, road, area, city, latitude, longitude, opening_time, closing_time) VALUES
('ST-DHK-01', 'Mirpur-10 Swap Hub', 'Mirpur Main Road', 'Mirpur-10', 'Dhaka', 23.806900, 90.368700, '06:00:00', '23:00:00'),
('ST-DHK-02', 'Dhanmondi-27 Station', 'Road 27 (Old 16)', 'Dhanmondi', 'Dhaka', 23.753400, 90.376800, '06:00:00', '23:30:00'),
('ST-DHK-03', 'Uttara Sector-7 Hub', 'Rabindra Sarani', 'Uttara Sector-7', 'Dhaka', 23.868100, 90.398200, '05:30:00', '23:00:00');

INSERT INTO station_phone (station_id, phone_number) VALUES
('ST-DHK-01', '01711000001'),
('ST-DHK-01', '01711000002'),
('ST-DHK-02', '01811000001'),
('ST-DHK-03', '01911000001');

-- -----------------------------------------------------------------------------
-- 2. POPULATE CABINETS & SLOTS (Rules 2 & 3 - Weak Entities)
-- -----------------------------------------------------------------------------
INSERT INTO cabinet (station_id, cabinet_number, installation_date, total_slots) VALUES
('ST-DHK-01', 1, '2025-01-10', 8),
('ST-DHK-01', 2, '2025-02-15', 8),
('ST-DHK-02', 1, '2025-03-01', 6),
('ST-DHK-03', 1, '2025-04-01', 6);

-- Slots for Station 1, Cabinet 1
INSERT INTO slot (station_id, cabinet_number, slot_number) VALUES
('ST-DHK-01', 1, 1), ('ST-DHK-01', 1, 2), ('ST-DHK-01', 1, 3), ('ST-DHK-01', 1, 4),
('ST-DHK-01', 1, 5), ('ST-DHK-01', 1, 6), ('ST-DHK-01', 1, 7), ('ST-DHK-01', 1, 8);

-- Slots for Station 1, Cabinet 2
INSERT INTO slot (station_id, cabinet_number, slot_number) VALUES
('ST-DHK-01', 2, 1), ('ST-DHK-01', 2, 2), ('ST-DHK-01', 2, 3), ('ST-DHK-01', 2, 4);

-- Slots for Station 2, Cabinet 1
INSERT INTO slot (station_id, cabinet_number, slot_number) VALUES
('ST-DHK-02', 1, 1), ('ST-DHK-02', 1, 2), ('ST-DHK-02', 1, 3), ('ST-DHK-02', 1, 4);

-- Slots for Station 3, Cabinet 1
INSERT INTO slot (station_id, cabinet_number, slot_number) VALUES
('ST-DHK-03', 1, 1), ('ST-DHK-03', 1, 2), ('ST-DHK-03', 1, 3), ('ST-DHK-03', 1, 4);

-- -----------------------------------------------------------------------------
-- 3. POPULATE BATTERY MODELS (Rule 4)
-- -----------------------------------------------------------------------------
INSERT INTO battery_model (model_code, manufacturer, chemistry, nominal_voltage, rated_capacity_kwh) VALUES
('BM-LFP-60', 'VoltPower BD Ltd.', 'LFP', 60.00, 3.20),
('BM-NMC-72', 'Bengal Energy Corp.', 'NMC', 72.00, 4.00);

-- -----------------------------------------------------------------------------
-- 4. POPULATE VEHICLES & SUBCLASSES (Rule 6 - Specialization)
-- -----------------------------------------------------------------------------
INSERT INTO vehicle (registration_number, make, year, vehicle_type) VALUES
('DHA-THA-11-2024', 'Runner EV', 2024, 'E_RICKSHAW'),
('DHA-THA-12-3045', 'Nitol Motors', 2023, 'E_RICKSHAW'),
('DHA-HA-55-1020', 'Akij Motors', 2024, 'E_MOTORBIKE'),
('DHA-HA-66-8899', 'Walton Digi-Tech', 2025, 'E_MOTORBIKE');

INSERT INTO erickshaw (registration_number, passenger_capacity, route_permit_number) VALUES
('DHA-THA-11-2024', 5, 'RP-DHK-MIRPUR-9021'),
('DHA-THA-12-3045', 6, 'RP-DHK-DHANMONDI-9045');

INSERT INTO emotorbike (registration_number, top_speed, is_delivery) VALUES
('DHA-HA-55-1020', 65.00, TRUE),   -- Delivery motorbike
('DHA-HA-66-8899', 80.00, FALSE);  -- Personal commuter

-- Vehicle-Battery Compatibility
INSERT INTO vehicle_battery_compatibility (registration_number, model_code) VALUES
('DHA-THA-11-2024', 'BM-LFP-60'),
('DHA-THA-12-3045', 'BM-LFP-60'),
('DHA-THA-12-3045', 'BM-NMC-72'),
('DHA-HA-55-1020', 'BM-NMC-72'),
('DHA-HA-66-8899', 'BM-NMC-72');

-- -----------------------------------------------------------------------------
-- 5. POPULATE BATTERIES (Rule 5)
-- -----------------------------------------------------------------------------
INSERT INTO battery (serial_number, manufacture_date, current_soh_percent, model_code, current_station_id, current_cabinet_number, current_slot_number, current_vehicle_reg_no, is_in_maintenance) VALUES
('VS-B-00917', '2024-05-10', 78.50, 'BM-LFP-60', 'ST-DHK-01', 1, 1, NULL, FALSE), -- Below 80% SOH
('VS-B-00101', '2025-01-15', 94.00, 'BM-LFP-60', 'ST-DHK-01', 1, 2, NULL, FALSE),
('VS-B-00102', '2025-01-18', 91.50, 'BM-LFP-60', 'ST-DHK-01', 1, 3, NULL, FALSE),
('VS-B-00103', '2024-03-20', 74.00, 'BM-LFP-60', NULL, NULL, NULL, NULL, TRUE),     -- Below 80% SOH & In Maintenance
('VS-B-00104', '2024-06-11', 79.00, 'BM-LFP-60', NULL, NULL, NULL, 'DHA-THA-11-2024', FALSE), -- Below 80% SOH & in vehicle
('VS-B-00201', '2025-02-01', 96.00, 'BM-NMC-72', 'ST-DHK-02', 1, 1, NULL, FALSE),
('VS-B-00202', '2025-02-10', 88.00, 'BM-NMC-72', NULL, NULL, NULL, 'DHA-HA-55-1020', FALSE),
('VS-B-00203', '2024-04-14', 72.50, 'BM-NMC-72', NULL, NULL, NULL, NULL, TRUE),     -- Below 80% SOH & In Maintenance
('VS-B-00301', '2025-03-01', 98.00, 'BM-LFP-60', 'ST-DHK-03', 1, 1, NULL, FALSE); -- Only battery in ST-DHK-03 slot, but depleted (35%)

-- -----------------------------------------------------------------------------
-- 6. POPULATE DRIVERS & REFERRALS & PHONES (Rules 7 & 9)
-- -----------------------------------------------------------------------------
INSERT INTO driver (driver_id, first_name, last_name, date_of_birth, mobile_wallet_number, referred_by_driver_id) VALUES
('DRV-001', 'Rafiqul', 'Islam', '1985-06-15', '01712345678', NULL),        -- Root referrer (3 referrals)
('DRV-002', 'Abdul', 'Karim', '1990-03-22', '01812345678', 'DRV-001'),     -- Referred by DRV-001 (1 referral)
('DRV-003', 'Kamal', 'Hossain', '1994-11-05', '01912345678', 'DRV-001'),   -- Referred by DRV-001
('DRV-004', 'Sumon', 'Mia', '1998-08-19', '01612345678', 'DRV-001'),       -- Referred by DRV-001
('DRV-005', 'Tariqul', 'Anam', '1992-01-30', '01512345678', 'DRV-002');    -- Referred by DRV-002

INSERT INTO driver_phone (driver_id, phone_number) VALUES
('DRV-001', '01712345678'),
('DRV-001', '01312345678'),
('DRV-002', '01812345678'),
('DRV-003', '01912345678'),
('DRV-004', '01612345678'),
('DRV-005', '01512345678');

-- -----------------------------------------------------------------------------
-- 7. POPULATE DRIVER-VEHICLE ASSIGNMENTS (Rule 8 - History over time)
-- -----------------------------------------------------------------------------
INSERT INTO driver_vehicle_assignment (driver_id, registration_number, start_date, end_date) VALUES
('DRV-001', 'DHA-THA-11-2024', '2025-01-01', '2025-06-30'), -- Past assignment
('DRV-001', 'DHA-THA-11-2024', '2025-07-01', NULL),         -- Day shift active assignment
('DRV-002', 'DHA-THA-11-2024', '2025-07-01', NULL),         -- Night shift shared active assignment
('DRV-003', 'DHA-THA-12-3045', '2025-02-01', NULL),         -- Active assignment
('DRV-004', 'DHA-HA-55-1020', '2025-03-01', NULL);          -- Active delivery motorbike

-- -----------------------------------------------------------------------------
-- 8. POPULATE SUBSCRIPTION PLANS & DRIVER SUBSCRIPTIONS (Rule 10)
-- -----------------------------------------------------------------------------
INSERT INTO subscription_plan (plan_code, name, monthly_fee, swaps_per_month) VALUES
('PLAN-UNLIM', 'Dhaka Pro Unlimited', 4500.00, 120),
('PLAN-COMMUTER', 'Daily Commuter Lite', 2000.00, 40);

INSERT INTO driver_subscription (driver_id, plan_code, start_date, end_date) VALUES
('DRV-001', 'PLAN-COMMUTER', '2025-01-01', '2025-05-31'), -- Past expired plan
('DRV-001', 'PLAN-UNLIM', '2025-06-01', NULL),             -- Current active plan
('DRV-002', 'PLAN-COMMUTER', '2025-06-01', NULL);          -- Current active plan

-- -----------------------------------------------------------------------------
-- 9. POPULATE EMPLOYEES & SPECIALIZATIONS (Rule 13)
-- -----------------------------------------------------------------------------
INSERT INTO employee (employee_id, name, phone, hire_date, role_type) VALUES
('EMP-OP-01', 'Farhan Ahmed', '01711223344', '2024-11-01', 'STATION_OPERATOR'),
('EMP-OP-02', 'Nasir Uddin', '01811223344', '2024-11-01', 'STATION_OPERATOR'),
('EMP-OP-03', 'Hasan Ali', '01911223344', '2024-11-01', 'STATION_OPERATOR'),
('EMP-TC-01', 'Engr. Mahbubur Rahman', '01511223344', '2024-10-15', 'TECHNICIAN'),
('EMP-TC-02', 'Sajid Hassan', '01611223344', '2025-01-10', 'TECHNICIAN');

INSERT INTO station_operator (employee_id, shift, assigned_station_id) VALUES
('EMP-OP-01', 'morning', 'ST-DHK-01'),
('EMP-OP-02', 'evening', 'ST-DHK-02'),
('EMP-OP-03', 'morning', 'ST-DHK-03');

INSERT INTO technician (employee_id, certification_level) VALUES
('EMP-TC-01', 'Level 3 Master Technician'),
('EMP-TC-02', 'Level 2 Certified Specialist');

INSERT INTO technician_certification (employee_id, model_code) VALUES
('EMP-TC-01', 'BM-LFP-60'),
('EMP-TC-01', 'BM-NMC-72'),
('EMP-TC-02', 'BM-LFP-60');

-- -----------------------------------------------------------------------------
-- 10. POPULATE SWAPS (Rule 11 - Two battery roles, slot recorded)
-- -----------------------------------------------------------------------------
INSERT INTO swap (swap_id, swap_timestamp, station_id, driver_id, registration_number, 
                  returned_battery_serial, returned_charge_percent, 
                  issued_battery_serial, issued_from_station_id, issued_from_cabinet_number, issued_from_slot_number) 
VALUES
-- Swap 1: Battery VS-B-00917 was ISSUED to driver DRV-001
('SWP-2026-001', '2026-11-15 08:30:00', 'ST-DHK-01', 'DRV-001', 'DHA-THA-11-2024',
 'VS-B-00104', 15.00, 'VS-B-00917', 'ST-DHK-01', 1, 1),

-- Swap 2: Driver DRV-001 returned VS-B-00917 later that evening, took VS-B-00101
('SWP-2026-002', '2026-11-15 18:45:00', 'ST-DHK-01', 'DRV-001', 'DHA-THA-11-2024',
 'VS-B-00917', 22.00, 'VS-B-00101', 'ST-DHK-01', 1, 2),

-- Swap 3: Battery VS-B-00917 was recharged and ISSUED again to driver DRV-002
('SWP-2026-003', '2026-11-16 09:15:00', 'ST-DHK-01', 'DRV-002', 'DHA-THA-11-2024',
 'VS-B-00101', 18.00, 'VS-B-00917', 'ST-DHK-01', 1, 1),

-- Swap 4: Driver DRV-002 returned VS-B-00917, took VS-B-00102
('SWP-2026-004', '2026-11-16 19:30:00', 'ST-DHK-01', 'DRV-002', 'DHA-THA-11-2024',
 'VS-B-00917', 12.00, 'VS-B-00102', 'ST-DHK-01', 1, 3),

-- Swap 5: Pay-per-swap driver DRV-003 at Station 2
('SWP-2026-005', '2026-11-17 10:00:00', 'ST-DHK-02', 'DRV-003', 'DHA-THA-12-3045',
 'VS-B-00202', 20.00, 'VS-B-00201', 'ST-DHK-02', 1, 1);

-- -----------------------------------------------------------------------------
-- 11. POPULATE PAYMENTS (Rule 12 - Settles Swap OR Subscription)
-- -----------------------------------------------------------------------------
-- DRV-001 pays monthly subscription fee (dynamically link subscription_id)
INSERT INTO payment (payment_id, amount, payment_timestamp, method, status, swap_id, subscription_id)
SELECT 'PAY-SUB-001', 4500.00, '2026-11-01 10:00:00', 'bKash', 'completed', NULL, subscription_id
FROM driver_subscription
WHERE driver_id = 'DRV-001' AND plan_code = 'PLAN-UNLIM'
LIMIT 1;

-- DRV-003 pays per swap (Swap SWP-2026-005)
INSERT INTO payment (payment_id, amount, payment_timestamp, method, status, swap_id, subscription_id) VALUES
('PAY-SWP-001', 150.00, '2026-11-17 10:02:00', 'Nagad', 'completed', 'SWP-2026-005', NULL);

-- -----------------------------------------------------------------------------
-- 12. POPULATE MAINTENANCE TICKETS (Rule 14)
-- -----------------------------------------------------------------------------
INSERT INTO maintenance_ticket (ticket_number, battery_serial, technician_id, date_opened, date_closed, fault_description, repair_cost) VALUES
('TCK-2026-01', 'VS-B-00103', 'EMP-TC-01', '2026-11-10', '2026-11-12', 'Cell imbalance and rapid voltage drop under load', 1850.00),
('TCK-2026-02', 'VS-B-00203', 'EMP-TC-01', '2026-11-14', NULL, 'BMS communication failure and thermal spike', NULL),
('TCK-2026-03', 'VS-B-00917', 'EMP-TC-02', '2026-10-05', '2026-10-06', 'Terminal contact pin corrosion cleaned', 450.00);

-- -----------------------------------------------------------------------------
-- 13. POPULATE TELEMETRY (Rule 15 - Weak Entity)
-- -----------------------------------------------------------------------------
INSERT INTO telemetry (battery_serial, reading_timestamp, voltage, temperature_c, state_of_charge_percent) VALUES
('VS-B-00917', '2026-11-18 10:00:00', 64.20, 34.50, 95.00),
('VS-B-00917', '2026-11-18 10:15:00', 64.00, 35.10, 94.00),
('VS-B-00101', '2026-11-18 10:00:00', 63.80, 36.20, 88.00),
('VS-B-00103', '2026-11-18 10:00:00', 58.10, 56.40, 42.00), -- Overheating reading (>55°C)!
('VS-B-00201', '2026-11-18 09:30:00', 76.50, 32.00, 98.00),
-- Station 3 slot battery with low charge during peak hour (35%):
('VS-B-00301', '2026-11-18 09:00:00', 59.50, 33.00, 35.00);


-- =============================================================================
-- THE 4 KEY ANALYTICAL QUERIES FROM THE ASSIGNMENT
-- =============================================================================

\echo ''
\echo '======================================================================'
\echo 'QUESTION 1: Which batteries have degraded below 80% health?'
\echo '======================================================================'
SELECT 
    b.serial_number,
    b.model_code,
    bm.manufacturer,
    bm.chemistry,
    b.manufacture_date,
    b.current_soh_percent
FROM battery b
JOIN battery_model bm ON b.model_code = bm.model_code
WHERE b.current_soh_percent < 80.00
ORDER BY b.current_soh_percent ASC;


\echo ''
\echo '======================================================================'
\echo 'QUESTION 2: Which stations run out of charged batteries at peak hours?'
\echo 'Definition: Peak hours (08:00-11:00 morning & 17:00-20:00 evening).'
\echo 'A station runs out if it has ZERO available batteries in slots with SOC >= 80%.'
\echo '======================================================================'
WITH station_inventory AS (
    SELECT 
        s.station_id,
        s.name AS station_name,
        COUNT(CASE 
            WHEN latest_soc.state_of_charge_percent >= 80.00 THEN 1 
            ELSE NULL 
        END) AS total_charged_batteries_available
    FROM station s
    LEFT JOIN slot sl ON s.station_id = sl.station_id
    LEFT JOIN battery b ON sl.station_id = b.current_station_id 
                        AND sl.cabinet_number = b.current_cabinet_number 
                        AND sl.slot_number = b.current_slot_number
    LEFT JOIN LATERAL (
        SELECT t.state_of_charge_percent
        FROM telemetry t
        WHERE t.battery_serial = b.serial_number
          AND (
              EXTRACT(HOUR FROM t.reading_timestamp) BETWEEN 8 AND 10 
              OR EXTRACT(HOUR FROM t.reading_timestamp) BETWEEN 17 AND 19
          )
        ORDER BY t.reading_timestamp DESC
        LIMIT 1
    ) latest_soc ON TRUE
    GROUP BY s.station_id, s.name
)
SELECT 
    station_id,
    station_name,
    total_charged_batteries_available
FROM station_inventory
WHERE total_charged_batteries_available = 0;


\echo ''
\echo '======================================================================'
\echo 'QUESTION 3: Which drivers referred the most new drivers?'
\echo '======================================================================'
SELECT 
    d.driver_id,
    d.first_name || ' ' || d.last_name AS driver_name,
    d.mobile_wallet_number,
    COUNT(r.driver_id) AS total_new_drivers_referred
FROM driver d
JOIN driver r ON d.driver_id = r.referred_by_driver_id
GROUP BY d.driver_id, d.first_name, d.last_name, d.mobile_wallet_number
ORDER BY total_new_drivers_referred DESC;


\echo ''
\echo '======================================================================'
\echo 'QUESTION 4: What was the full swap history of battery VS-B-00917?'
\echo '======================================================================'
SELECT 
    s.swap_id,
    s.swap_timestamp,
    st.name AS station_name,
    d.driver_id,
    d.first_name || ' ' || d.last_name AS driver_name,
    s.registration_number AS vehicle_reg_no,
    CASE 
        WHEN s.returned_battery_serial = 'VS-B-00917' THEN 'RETURNED (Depleted)'
        WHEN s.issued_battery_serial = 'VS-B-00917'   THEN 'ISSUED (Charged)'
    END AS role_of_battery_00917,
    s.returned_charge_percent,
    s.issued_from_cabinet_number,
    s.issued_from_slot_number
FROM swap s
JOIN station st ON s.station_id = st.station_id
JOIN driver d ON s.driver_id = d.driver_id
WHERE s.returned_battery_serial = 'VS-B-00917' 
   OR s.issued_battery_serial = 'VS-B-00917'
ORDER BY s.swap_timestamp ASC;
