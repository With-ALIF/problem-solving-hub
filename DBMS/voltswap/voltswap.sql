-- Silence notices and command outputs for clean terminal display
\set QUIET on
SET client_min_messages = WARNING;

-- Drop tables if they exist in reverse dependency order

DROP VIEW IF EXISTS v_battery_cycle_count CASCADE;
DROP VIEW IF EXISTS v_driver_details CASCADE;
DROP TABLE IF EXISTS telemetry CASCADE;
DROP TABLE IF EXISTS maintenance_ticket CASCADE;
DROP TABLE IF EXISTS payment CASCADE;
DROP TABLE IF EXISTS swap CASCADE;
DROP TABLE IF EXISTS station_operator CASCADE;
DROP TABLE IF EXISTS technician_certification CASCADE;
DROP TABLE IF EXISTS technician CASCADE;
DROP TABLE IF EXISTS employee CASCADE;
DROP TABLE IF EXISTS driver_subscription CASCADE;
DROP TABLE IF EXISTS subscription_plan CASCADE;
DROP TABLE IF EXISTS driver_vehicle_assignment CASCADE;
DROP TABLE IF EXISTS driver_phone CASCADE;
DROP TABLE IF EXISTS driver CASCADE;
DROP TABLE IF EXISTS vehicle_battery_compatibility CASCADE;
DROP TABLE IF EXISTS emotorbike CASCADE;
DROP TABLE IF EXISTS erickshaw CASCADE;
DROP TABLE IF EXISTS vehicle CASCADE;
DROP TABLE IF EXISTS battery CASCADE;
DROP TABLE IF EXISTS battery_model CASCADE;
DROP TABLE IF EXISTS slot CASCADE;
DROP TABLE IF EXISTS cabinet CASCADE;
DROP TABLE IF EXISTS station_phone CASCADE;
DROP TABLE IF EXISTS station CASCADE;

-- -----------------------------------------------------------------------------
-- 1. STATION & MULTIVALUED PHONES
-- -----------------------------------------------------------------------------
CREATE TABLE station (
    station_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    road VARCHAR(100) NOT NULL,
    area VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    latitude NUMERIC(9, 6) NOT NULL,
    longitude NUMERIC(9, 6) NOT NULL,
    opening_time TIME NOT NULL,
    closing_time TIME NOT NULL,
    CONSTRAINT chk_station_hours CHECK (opening_time < closing_time)
);

CREATE TABLE station_phone (
    station_id VARCHAR(20) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    CONSTRAINT pk_station_phone PRIMARY KEY (station_id, phone_number),
    CONSTRAINT fk_station_phone_station FOREIGN KEY (station_id)
        REFERENCES station(station_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 2. CABINET (Weak Entity on Station)
-- -----------------------------------------------------------------------------
CREATE TABLE cabinet (
    station_id VARCHAR(20) NOT NULL,
    cabinet_number INT NOT NULL,
    installation_date DATE NOT NULL,
    total_slots INT NOT NULL,
    CONSTRAINT pk_cabinet PRIMARY KEY (station_id, cabinet_number),
    CONSTRAINT fk_cabinet_station FOREIGN KEY (station_id)
        REFERENCES station(station_id) ON DELETE CASCADE,
    CONSTRAINT chk_cabinet_number CHECK (cabinet_number > 0),
    CONSTRAINT chk_total_slots CHECK (total_slots > 0)
);

-- -----------------------------------------------------------------------------
-- 3. SLOT (Weak Entity on Cabinet)
-- -----------------------------------------------------------------------------
CREATE TABLE slot (
    station_id VARCHAR(20) NOT NULL,
    cabinet_number INT NOT NULL,
    slot_number INT NOT NULL,
    CONSTRAINT pk_slot PRIMARY KEY (station_id, cabinet_number, slot_number),
    CONSTRAINT fk_slot_cabinet FOREIGN KEY (station_id, cabinet_number)
        REFERENCES cabinet(station_id, cabinet_number) ON DELETE CASCADE,
    CONSTRAINT chk_slot_number CHECK (slot_number > 0)
);

-- -----------------------------------------------------------------------------
-- 4. BATTERY MODEL
-- -----------------------------------------------------------------------------
CREATE TABLE battery_model (
    model_code VARCHAR(30) PRIMARY KEY,
    manufacturer VARCHAR(100) NOT NULL,
    chemistry VARCHAR(10) NOT NULL,
    nominal_voltage NUMERIC(5, 2) NOT NULL,
    rated_capacity_kwh NUMERIC(5, 2) NOT NULL,
    CONSTRAINT chk_chemistry CHECK (chemistry IN ('LFP', 'NMC')),
    CONSTRAINT chk_voltage CHECK (nominal_voltage > 0),
    CONSTRAINT chk_capacity CHECK (rated_capacity_kwh > 0)
);

-- -----------------------------------------------------------------------------
-- 5. BATTERY
-- -----------------------------------------------------------------------------
CREATE TABLE battery (
    serial_number VARCHAR(50) PRIMARY KEY,
    manufacture_date DATE NOT NULL,
    current_soh_percent NUMERIC(5, 2) NOT NULL,
    model_code VARCHAR(30) NOT NULL,
    -- Current location tracking (Exclusive placement: Slot, Vehicle, or Maintenance)
    current_station_id VARCHAR(20),
    current_cabinet_number INT,
    current_slot_number INT,
    current_vehicle_reg_no VARCHAR(20),
    is_in_maintenance BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_battery_model FOREIGN KEY (model_code)
        REFERENCES battery_model(model_code) ON DELETE RESTRICT,
    CONSTRAINT fk_battery_slot FOREIGN KEY (current_station_id, current_cabinet_number, current_slot_number)
        REFERENCES slot(station_id, cabinet_number, slot_number) ON DELETE SET NULL,
    -- At most one battery can sit in a specific slot
    CONSTRAINT uq_battery_slot UNIQUE (current_station_id, current_cabinet_number, current_slot_number),
    CONSTRAINT chk_soh CHECK (current_soh_percent BETWEEN 0 AND 100),
    -- Mutual exclusivity constraint for battery state
    CONSTRAINT chk_battery_location_state CHECK (
        (current_slot_number IS NOT NULL AND current_vehicle_reg_no IS NULL AND NOT is_in_maintenance) OR
        (current_slot_number IS NULL AND current_vehicle_reg_no IS NOT NULL AND NOT is_in_maintenance) OR
        (current_slot_number IS NULL AND current_vehicle_reg_no IS NULL AND is_in_maintenance) OR
        (current_slot_number IS NULL AND current_vehicle_reg_no IS NULL AND NOT is_in_maintenance)
    )
);

-- -----------------------------------------------------------------------------
-- 6. VEHICLE (Superclass) & SUBCLASSES (E-Rickshaw, E-Motorbike)
-- -----------------------------------------------------------------------------
CREATE TABLE vehicle (
    registration_number VARCHAR(20) PRIMARY KEY,
    make VARCHAR(50) NOT NULL,
    year INT NOT NULL,
    vehicle_type VARCHAR(20) NOT NULL,
    CONSTRAINT chk_vehicle_year CHECK (year BETWEEN 2000 AND 2100),
    CONSTRAINT chk_vehicle_type CHECK (vehicle_type IN ('E_RICKSHAW', 'E_MOTORBIKE'))
);

-- Add deferred foreign key from battery to vehicle
ALTER TABLE battery
    ADD CONSTRAINT fk_battery_vehicle FOREIGN KEY (current_vehicle_reg_no)
        REFERENCES vehicle(registration_number) ON DELETE SET NULL;

CREATE TABLE erickshaw (
    registration_number VARCHAR(20) PRIMARY KEY,
    passenger_capacity INT NOT NULL,
    route_permit_number VARCHAR(50) NOT NULL UNIQUE,
    CONSTRAINT fk_erickshaw_vehicle FOREIGN KEY (registration_number)
        REFERENCES vehicle(registration_number) ON DELETE CASCADE,
    CONSTRAINT chk_passenger_capacity CHECK (passenger_capacity > 0)
);

CREATE TABLE emotorbike (
    registration_number VARCHAR(20) PRIMARY KEY,
    top_speed NUMERIC(5, 2) NOT NULL,
    is_delivery BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_emotorbike_vehicle FOREIGN KEY (registration_number)
        REFERENCES vehicle(registration_number) ON DELETE CASCADE,
    CONSTRAINT chk_top_speed CHECK (top_speed > 0)
);

CREATE TABLE vehicle_battery_compatibility (
    registration_number VARCHAR(20) NOT NULL,
    model_code VARCHAR(30) NOT NULL,
    CONSTRAINT pk_vehicle_battery_comp PRIMARY KEY (registration_number, model_code),
    CONSTRAINT fk_vbc_vehicle FOREIGN KEY (registration_number)
        REFERENCES vehicle(registration_number) ON DELETE CASCADE,
    CONSTRAINT fk_vbc_model FOREIGN KEY (model_code)
        REFERENCES battery_model(model_code) ON DELETE RESTRICT
);

-- -----------------------------------------------------------------------------
-- 7. DRIVER & MULTIVALUED PHONES & REFERRAL (Recursive)
-- -----------------------------------------------------------------------------
CREATE TABLE driver (
    driver_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    mobile_wallet_number VARCHAR(20) NOT NULL,
    referred_by_driver_id VARCHAR(20),
    CONSTRAINT fk_driver_referral FOREIGN KEY (referred_by_driver_id)
        REFERENCES driver(driver_id) ON DELETE SET NULL,
    CONSTRAINT chk_no_self_referral CHECK (referred_by_driver_id <> driver_id)
);

CREATE TABLE driver_phone (
    driver_id VARCHAR(20) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    CONSTRAINT pk_driver_phone PRIMARY KEY (driver_id, phone_number),
    CONSTRAINT fk_driver_phone_driver FOREIGN KEY (driver_id)
        REFERENCES driver(driver_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 8. DRIVER-VEHICLE ASSIGNMENT (Historical M:N)
-- -----------------------------------------------------------------------------
CREATE TABLE driver_vehicle_assignment (
    assignment_id SERIAL PRIMARY KEY,
    driver_id VARCHAR(20) NOT NULL,
    registration_number VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    CONSTRAINT fk_dva_driver FOREIGN KEY (driver_id)
        REFERENCES driver(driver_id) ON DELETE RESTRICT,
    CONSTRAINT fk_dva_vehicle FOREIGN KEY (registration_number)
        REFERENCES vehicle(registration_number) ON DELETE RESTRICT,
    CONSTRAINT chk_assignment_dates CHECK (end_date IS NULL OR end_date >= start_date)
);

-- -----------------------------------------------------------------------------
-- 9. SUBSCRIPTION PLAN & DRIVER-SUBSCRIPTION HISTORY
-- -----------------------------------------------------------------------------
CREATE TABLE subscription_plan (
    plan_code VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    monthly_fee NUMERIC(10, 2) NOT NULL,
    swaps_per_month INT NOT NULL,
    CONSTRAINT chk_monthly_fee CHECK (monthly_fee >= 0),
    CONSTRAINT chk_swaps_per_month CHECK (swaps_per_month > 0)
);

CREATE TABLE driver_subscription (
    subscription_id SERIAL PRIMARY KEY,
    driver_id VARCHAR(20) NOT NULL,
    plan_code VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    CONSTRAINT fk_ds_driver FOREIGN KEY (driver_id)
        REFERENCES driver(driver_id) ON DELETE RESTRICT,
    CONSTRAINT fk_ds_plan FOREIGN KEY (plan_code)
        REFERENCES subscription_plan(plan_code) ON DELETE RESTRICT,
    CONSTRAINT chk_subscription_dates CHECK (end_date IS NULL OR end_date >= start_date)
);

-- Rule 10: A driver can hold at most one active plan at a time (end_date IS NULL)
CREATE UNIQUE INDEX uq_driver_active_plan
    ON driver_subscription (driver_id)
    WHERE end_date IS NULL;

-- -----------------------------------------------------------------------------
-- 10. EMPLOYEE & SPECIALIZATION (Technician, Station Operator)
-- -----------------------------------------------------------------------------
CREATE TABLE employee (
    employee_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    hire_date DATE NOT NULL,
    role_type VARCHAR(20) NOT NULL,
    CONSTRAINT chk_employee_role CHECK (role_type IN ('TECHNICIAN', 'STATION_OPERATOR'))
);

CREATE TABLE technician (
    employee_id VARCHAR(20) PRIMARY KEY,
    certification_level VARCHAR(30) NOT NULL,
    CONSTRAINT fk_technician_employee FOREIGN KEY (employee_id)
        REFERENCES employee(employee_id) ON DELETE CASCADE
);

CREATE TABLE technician_certification (
    employee_id VARCHAR(20) NOT NULL,
    model_code VARCHAR(30) NOT NULL,
    CONSTRAINT pk_tech_cert PRIMARY KEY (employee_id, model_code),
    CONSTRAINT fk_tc_technician FOREIGN KEY (employee_id)
        REFERENCES technician(employee_id) ON DELETE CASCADE,
    CONSTRAINT fk_tc_model FOREIGN KEY (model_code)
        REFERENCES battery_model(model_code) ON DELETE RESTRICT
);

-- Rule 13: Every station is managed by exactly one operator; each operator works at exactly one station (1:1)
CREATE TABLE station_operator (
    employee_id VARCHAR(20) PRIMARY KEY,
    shift VARCHAR(20) NOT NULL,
    assigned_station_id VARCHAR(20) NOT NULL UNIQUE,
    CONSTRAINT fk_operator_employee FOREIGN KEY (employee_id)
        REFERENCES employee(employee_id) ON DELETE CASCADE,
    CONSTRAINT fk_operator_station FOREIGN KEY (assigned_station_id)
        REFERENCES station(station_id) ON DELETE RESTRICT,
    CONSTRAINT chk_shift CHECK (shift IN ('morning', 'evening', 'night'))
);

-- -----------------------------------------------------------------------------
-- 11. SWAP (Involves Station, Driver, Vehicle, Slot, Returned Battery, Issued Battery)
-- -----------------------------------------------------------------------------
CREATE TABLE swap (
    swap_id VARCHAR(30) PRIMARY KEY,
    swap_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    station_id VARCHAR(20) NOT NULL,
    driver_id VARCHAR(20) NOT NULL,
    registration_number VARCHAR(20) NOT NULL,
    returned_battery_serial VARCHAR(50) NOT NULL,
    returned_charge_percent NUMERIC(5, 2) NOT NULL,
    issued_battery_serial VARCHAR(50) NOT NULL,
    issued_from_station_id VARCHAR(20) NOT NULL,
    issued_from_cabinet_number INT NOT NULL,
    issued_from_slot_number INT NOT NULL,
    CONSTRAINT fk_swap_station FOREIGN KEY (station_id)
        REFERENCES station(station_id) ON DELETE RESTRICT,
    CONSTRAINT fk_swap_driver FOREIGN KEY (driver_id)
        REFERENCES driver(driver_id) ON DELETE RESTRICT,
    CONSTRAINT fk_swap_vehicle FOREIGN KEY (registration_number)
        REFERENCES vehicle(registration_number) ON DELETE RESTRICT,
    -- Two separate relationships for the two batteries in a swap (Role names: returned vs issued)
    CONSTRAINT fk_swap_returned_battery FOREIGN KEY (returned_battery_serial)
        REFERENCES battery(serial_number) ON DELETE RESTRICT,
    CONSTRAINT fk_swap_issued_battery FOREIGN KEY (issued_battery_serial)
        REFERENCES battery(serial_number) ON DELETE RESTRICT,
    -- Slot the issued battery came from
    CONSTRAINT fk_swap_issued_slot FOREIGN KEY (issued_from_station_id, issued_from_cabinet_number, issued_from_slot_number)
        REFERENCES slot(station_id, cabinet_number, slot_number) ON DELETE RESTRICT,
    CONSTRAINT chk_returned_charge CHECK (returned_charge_percent BETWEEN 0 AND 100),
    CONSTRAINT chk_distinct_batteries CHECK (returned_battery_serial <> issued_battery_serial),
    CONSTRAINT chk_swap_station_slot_match CHECK (station_id = issued_from_station_id)
);

-- -----------------------------------------------------------------------------
-- 12. PAYMENT (Settles Pay-per-swap OR Subscription, Mutually Exclusive)
-- -----------------------------------------------------------------------------
CREATE TABLE payment (
    payment_id VARCHAR(30) PRIMARY KEY,
    amount NUMERIC(10, 2) NOT NULL,
    payment_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    method VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,
    swap_id VARCHAR(30) UNIQUE,
    subscription_id INT,
    CONSTRAINT fk_payment_swap FOREIGN KEY (swap_id)
        REFERENCES swap(swap_id) ON DELETE RESTRICT,
    CONSTRAINT fk_payment_subscription FOREIGN KEY (subscription_id)
        REFERENCES driver_subscription(subscription_id) ON DELETE RESTRICT,
    CONSTRAINT chk_payment_amount CHECK (amount >= 0),
    CONSTRAINT chk_payment_method CHECK (method IN ('bKash', 'Nagad', 'card', 'cash')),
    CONSTRAINT chk_payment_status CHECK (status IN ('pending', 'completed', 'failed', 'refunded')),
    -- Exclusive-OR check: Payment settles EITHER one pay-per-swap swap OR one month subscription
    CONSTRAINT chk_payment_settlement_type CHECK (
        (swap_id IS NOT NULL AND subscription_id IS NULL) OR
        (swap_id IS NULL AND subscription_id IS NOT NULL)
    )
);

-- -----------------------------------------------------------------------------
-- 13. MAINTENANCE TICKET
-- -----------------------------------------------------------------------------
CREATE TABLE maintenance_ticket (
    ticket_number VARCHAR(30) PRIMARY KEY,
    battery_serial VARCHAR(50) NOT NULL,
    technician_id VARCHAR(20) NOT NULL,
    date_opened DATE NOT NULL,
    date_closed DATE,
    fault_description TEXT NOT NULL,
    repair_cost NUMERIC(10, 2),
    CONSTRAINT fk_ticket_battery FOREIGN KEY (battery_serial)
        REFERENCES battery(serial_number) ON DELETE RESTRICT,
    CONSTRAINT fk_ticket_technician FOREIGN KEY (technician_id)
        REFERENCES technician(employee_id) ON DELETE RESTRICT,
    CONSTRAINT chk_repair_cost CHECK (repair_cost IS NULL OR repair_cost >= 0),
    CONSTRAINT chk_ticket_dates CHECK (date_closed IS NULL OR date_closed >= date_opened)
);

-- -----------------------------------------------------------------------------
-- 14. TELEMETRY (Weak Entity on Battery)
-- -----------------------------------------------------------------------------
CREATE TABLE telemetry (
    battery_serial VARCHAR(50) NOT NULL,
    reading_timestamp TIMESTAMP NOT NULL,
    voltage NUMERIC(6, 2) NOT NULL,
    temperature_c NUMERIC(5, 2) NOT NULL,
    state_of_charge_percent NUMERIC(5, 2) NOT NULL,
    CONSTRAINT pk_telemetry PRIMARY KEY (battery_serial, reading_timestamp),
    CONSTRAINT fk_telemetry_battery FOREIGN KEY (battery_serial)
        REFERENCES battery(serial_number) ON DELETE CASCADE,
    CONSTRAINT chk_telemetry_voltage CHECK (voltage > 0),
    CONSTRAINT chk_telemetry_soc CHECK (state_of_charge_percent BETWEEN 0 AND 100)
);

-- -----------------------------------------------------------------------------
-- 15. VIEWS FOR DERIVED ATTRIBUTES (Age and Cycle Count)
-- -----------------------------------------------------------------------------

-- Derived attribute: Driver Age (Calculated from date_of_birth)
CREATE OR REPLACE VIEW v_driver_details AS
SELECT 
    driver_id,
    first_name,
    last_name,
    date_of_birth,
    mobile_wallet_number,
    referred_by_driver_id,
    EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth))::INT AS calculated_age
FROM driver;

-- Derived attribute: Battery Total Cycle Count (Obtained from swap history)
CREATE OR REPLACE VIEW v_battery_cycle_count AS
SELECT 
    b.serial_number,
    b.model_code,
    b.current_soh_percent,
    COUNT(s.swap_id) AS total_cycle_count
FROM battery b
LEFT JOIN swap s ON b.serial_number = s.returned_battery_serial
GROUP BY b.serial_number, b.model_code, b.current_soh_percent;
