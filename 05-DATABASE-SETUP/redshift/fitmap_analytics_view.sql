-- ============================================================================
-- FitMap Analytics View - Body Measurement Dashboard Ready (Enhanced)
-- ============================================================================

CREATE OR REPLACE VIEW qspoc.fitmap_analytics AS
SELECT
    -- Scan Information
    ss.scan_id,
    ss.user_id,
    ss.date AS scan_date,
    TO_TIMESTAMP(ss.date, 'DD-MM-YYYY HH24:MI') AS scan_timestamp,
    ss.status,
    ss.store_num,
    ss.scanning_mode,
    CAST(ss.year AS INTEGER) AS scan_year,
    CAST(ss.month AS INTEGER) AS scan_month,
    DATE_TRUNC('month', TO_TIMESTAMP(ss.date, 'DD-MM-YYYY HH24:MI')) AS scan_month_date,
    DATE_TRUNC('week', TO_TIMESTAMP(ss.date, 'DD-MM-YYYY HH24:MI')) AS scan_week_date,
    DATE_TRUNC('day', TO_TIMESTAMP(ss.date, 'DD-MM-YYYY HH24:MI')) AS scan_day_date,
    
    -- User Demographics
    su.age,
    su.gender,
    su.height,
    su.weight,
    su.bmi,
    su.email,
    su.customer_type,
    su.scan_count,
    su.last_scan_date,
    
    -- Age Groups (Dashboard Compatible - 5 year ranges)
    CASE
        WHEN su.age < 25 THEN '20-25'
        WHEN su.age BETWEEN 25 AND 29 THEN '25-30'
        WHEN su.age BETWEEN 30 AND 34 THEN '30-35'
        WHEN su.age BETWEEN 35 AND 39 THEN '35-40'
        WHEN su.age BETWEEN 40 AND 44 THEN '40-45'
        WHEN su.age BETWEEN 45 AND 49 THEN '45-50'
        WHEN su.age BETWEEN 50 AND 54 THEN '50-55'
        WHEN su.age BETWEEN 55 AND 59 THEN '55-60'
        WHEN su.age BETWEEN 60 AND 64 THEN '60-65'
        WHEN su.age BETWEEN 65 AND 69 THEN '65-70'
        WHEN su.age BETWEEN 70 AND 74 THEN '70-75'
        ELSE '75+'
    END AS age_group,
    
    -- Body Measurements (DXL Custom) - Dashboard Ready
    sdcm.chest AS chest_circumference,
    sdcm.chest AS chest_front_circumference,  -- Alias for dashboard compatibility
    sdcm.chest AS chest_back_circumference,   -- Using same value as we don't have separate front/back
    sdcm.trouserwaist AS waist_circumference,
    sdcm.trouserwaist AS waist_front_circumference,  -- Alias for dashboard compatibility
    sdcm.trouserwaist AS waist_back_circumference,   -- Using same value
    sdcm.inseamleft AS inseam,
    sdcm.neck AS neck_circumference,
    sdcm.sleeveleft AS sleeve_length,
    sdcm.shoulderwidth AS shoulder_width,
    sdcm.seatmeasurement AS hip_circumference,
    sdcm.seatmeasurement AS crotch_point_circumference,  -- Using hip as proxy for crotch point
    
    -- Average Measurement (for KPI)
    (COALESCE(sdcm.chest, 0) + COALESCE(sdcm.trouserwaist, 0) + 
     COALESCE(sdcm.seatmeasurement, 0) + COALESCE(sdcm.neck, 0) + 
     COALESCE(sdcm.shoulderwidth, 0)) / 
    NULLIF((CASE WHEN sdcm.chest IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN sdcm.trouserwaist IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN sdcm.seatmeasurement IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN sdcm.neck IS NOT NULL THEN 1 ELSE 0 END +
            CASE WHEN sdcm.shoulderwidth IS NOT NULL THEN 1 ELSE 0 END), 0) AS avg_measurement_value,
    
    -- Garment Information (Simulated based on measurements)
    CASE
        WHEN sdcm.trouserwaist IS NOT NULL AND sdcm.inseamleft IS NOT NULL AND sdcm.inseamleft >= 32 THEN 'Dress Pants'
        WHEN sdcm.trouserwaist IS NOT NULL AND sdcm.inseamleft IS NOT NULL AND sdcm.inseamleft < 32 THEN 'Shorts'
        WHEN sdcm.trouserwaist IS NOT NULL AND sdcm.inseamleft IS NOT NULL AND sdcm.trouserwaist > 42 THEN 'Denim'
        WHEN sdcm.chest IS NOT NULL AND sdcm.sleeveleft IS NOT NULL AND sdcm.neck IS NOT NULL THEN 'Dress Shirt'
        WHEN sdcm.chest IS NOT NULL AND sdcm.sleeveleft IS NOT NULL THEN 'Casual Shirt'
        WHEN sdcm.chest IS NOT NULL AND sdcm.chest > 50 THEN 'Big & Tall Shirt'
        WHEN sdcm.chest IS NOT NULL THEN 'Polo Shirt'
        ELSE 'General Fit'
    END AS garment_type,
    
    -- Garment Size (Formatted as waist,inseam for pants or chest for shirts)
    CASE
        WHEN sdcm.trouserwaist IS NOT NULL AND sdcm.inseamleft IS NOT NULL 
        THEN CAST(ROUND(sdcm.trouserwaist) AS VARCHAR) || ',' || CAST(ROUND(sdcm.inseamleft) AS VARCHAR)
        WHEN sdcm.chest IS NOT NULL 
        THEN CAST(ROUND(sdcm.chest) AS VARCHAR)
        ELSE 'Unknown'
    END AS garment_size,
    
    -- Brand (Enhanced simulation based on measurements and body type)
    CASE
        WHEN sdcm.chest > 54 AND su.height > 74 THEN 'DXL Exclusive'
        WHEN sdcm.chest BETWEEN 50 AND 54 THEN 'Harbor Bay'
        WHEN sdcm.chest BETWEEN 46 AND 50 AND sdcm.trouserwaist > 44 THEN 'Oak Hill'
        WHEN sdcm.chest BETWEEN 42 AND 46 THEN 'Synrgy'
        WHEN sdcm.chest BETWEEN 38 AND 42 THEN 'Casual Male'
        WHEN sdcm.trouserwaist > 48 THEN 'True Nation'
        WHEN su.age < 35 AND sdcm.chest < 46 THEN 'MVP Collections'
        ELSE 'Generic Brand'
    END AS brand,
    
    -- Size Category (Calculated)
    CASE
        WHEN sdcm.chest < 38 THEN 'S'
        WHEN sdcm.chest BETWEEN 38 AND 42 THEN 'M'
        WHEN sdcm.chest BETWEEN 42 AND 46 THEN 'L'
        WHEN sdcm.chest BETWEEN 46 AND 50 THEN 'XL'
        WHEN sdcm.chest BETWEEN 50 AND 54 THEN '2XL'
        WHEN sdcm.chest BETWEEN 54 AND 58 THEN '3XL'
        WHEN sdcm.chest BETWEEN 58 AND 62 THEN '4XL'
        ELSE '5XL+'
    END AS size_category,
    
    -- Body Type Segment (Calculated)
    CASE
        WHEN su.height > 74 AND sdcm.chest > 46 THEN 'Big & Tall'
        WHEN su.height > 74 AND sdcm.chest <= 46 THEN 'Tall'
        WHEN sdcm.chest > 50 THEN 'Big'
        WHEN (sdcm.trouserwaist / NULLIF(sdcm.chest, 0)) < 0.85 THEN 'Athletic'
        WHEN (sdcm.trouserwaist / NULLIF(sdcm.chest, 0)) > 0.95 THEN 'Husky'
        ELSE 'Regular'
    END AS body_type_segment,
    
    -- Fit Score (0-100 based on measurement consistency)
    ROUND(
        100 - (
            ABS(sdcm.chest - (su.weight * 0.5)) / NULLIF(sdcm.chest, 0) * 10 +
            ABS(sdcm.trouserwaist - (su.weight * 0.4)) / NULLIF(sdcm.trouserwaist, 0) * 10
        ), 1
    ) AS fit_score,
    
    -- Calculated Metrics for Dashboard
    CASE WHEN UPPER(ss.status) = 'COMPLETE' THEN 1 ELSE 0 END AS scan_completed_flag,
    CASE WHEN su.scan_count > 1 THEN 1 ELSE 0 END AS repeat_user_flag,
    
    -- Measurement Quality Indicators
    CASE 
        WHEN sdcm.chest IS NOT NULL 
        AND sdcm.trouserwaist IS NOT NULL 
        AND sdcm.inseamleft IS NOT NULL 
        AND sdcm.shoulderwidth IS NOT NULL 
        THEN 1 ELSE 0 
    END AS complete_measurement_flag

FROM qspos.size_scans ss

INNER JOIN qspos.size_users su 
    ON ss.user_id = su.id

LEFT JOIN qspos.size_dxl_custom_measures sdcm 
    ON ss.scan_id = sdcm.scan_id;
