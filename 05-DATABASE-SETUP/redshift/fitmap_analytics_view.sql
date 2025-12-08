-- ============================================================================
-- FitMap Analytics View - Dashboard Ready
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
    
    -- Order Information (joined via email within 30 days)
    o.orderid,
    o.createdtimestamp AS purchase_date,
    o.ordertypeid,
    o.order_source,
    o.device_type,
    o.customeremail,
    
    -- Order Line Details
    ol.orderlineid,
    ol.isreturn,
    ol.orderlinetotal,
    ol.quantity,
    ol.unitprice,
    ol.totaldiscounts,
    
    -- Item Details
    oli.itemid,
    oli.itemsize,
    oli.itembrand,
    oli.itemdepartmentname,
    oli.itemdescription,
    
    -- Calculated Metrics for Dashboard
    CASE WHEN ss.status = 'COMPLETED' THEN 1 ELSE 0 END AS scan_completed_flag,
    CASE WHEN o.orderid IS NOT NULL THEN 1 ELSE 0 END AS purchase_made_flag,
    CASE WHEN ol.isreturn = TRUE THEN 1 ELSE 0 END AS return_flag,
    
    -- Days between scan and purchase
    CASE 
        WHEN o.createdtimestamp IS NOT NULL 
        THEN DATEDIFF(day, CAST(ss.date AS TIMESTAMP), CAST(o.createdtimestamp AS TIMESTAMP))
        ELSE NULL 
    END AS days_to_purchase

FROM qspos.size_scans ss

LEFT JOIN qspos.size_users su 
    ON ss.user_id = su.id

LEFT JOIN qspos.size_dxl_custom_measures sdcm 
    ON ss.scan_id = sdcm.scan_id

LEFT JOIN qspos.orderheader o 
    ON LOWER(TRIM(su.email)) = LOWER(TRIM(o.customeremail))
    AND CAST(o.createdtimestamp AS TIMESTAMP) >= CAST(ss.date AS TIMESTAMP)
    AND CAST(o.createdtimestamp AS TIMESTAMP) <= DATEADD(day, 30, CAST(ss.date AS TIMESTAMP))

LEFT JOIN qspos.orderline ol 
    ON o.orderid = ol.orderid

LEFT JOIN qspos.orderline_items oli
    ON ol.itemid = oli.itemid;

