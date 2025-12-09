-- ============================================================================
-- FitMap Analytics View - Dashboard Ready (FitMap Data Only)
-- ============================================================================

CREATE OR REPLACE VIEW qspos.fitmap_analytics AS
SELECT
    -- Scan Information
    ss.scan_id,
    ss.user_id,
    ss.date AS scan_date,
    ss.status,
    ss.store_num,
    ss.scanning_mode,
    CAST(ss.year AS INTEGER) AS scan_year,
    CAST(ss.month AS INTEGER) AS scan_month,
    DATE_TRUNC('month', TO_TIMESTAMP(ss.date, 'DD-MM-YYYY HH24:MI')) AS scan_month_date,
    DATE_TRUNC('week', TO_TIMESTAMP(ss.date, 'DD-MM-YYYY HH24:MI')) AS scan_week_date,
    
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
    
    -- Age Group (for dashboard filtering)
    CASE
        WHEN su.age < 25 THEN '18-24'
        WHEN su.age BETWEEN 25 AND 34 THEN '25-34'
        WHEN su.age BETWEEN 35 AND 44 THEN '35-44'
        WHEN su.age BETWEEN 45 AND 54 THEN '45-54'
        WHEN su.age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END AS age_group,
    
    -- Body Measurements (DXL Custom)
    sdcm.chest AS chest_circumference,
    sdcm.trouserwaist AS waist_circumference,
    sdcm.inseamleft AS inseam,
    sdcm.neck AS neck_circumference,
    sdcm.sleeveleft AS sleeve_length,
    sdcm.shoulderwidth AS shoulder_width,
    sdcm.seatmeasurement AS hip_circumference,
    
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
