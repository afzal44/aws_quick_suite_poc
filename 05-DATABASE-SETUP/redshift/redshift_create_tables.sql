-- ============================================================================
-- AWS Quick Suite POC - Redshift Table Creation Script
-- Schema: qspos
-- Total Tables: 20
-- ============================================================================

-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS qspos;

-- ============================================================================
-- FITMAP/SIZESTREAM TABLES (5 tables)
-- ============================================================================

-- Table 1: size_users
DROP TABLE IF EXISTS qspos.size_users CASCADE;
CREATE TABLE qspos.size_users (
    id VARCHAR(100) PRIMARY KEY,
    source_app VARCHAR(100),
    created VARCHAR(50),
    modified VARCHAR(50),
    source_attendant VARCHAR(50),
    last_name VARCHAR(100),
    first_name VARCHAR(100),
    date_of_birth VARCHAR(50),
    email VARCHAR(200),
    phone VARCHAR(50),
    height INTEGER,
    weight INTEGER,
    process_date VARCHAR(50),
    load_filename VARCHAR(500),
    load_timestamp VARCHAR(50),
    gender VARCHAR(20),
    year INTEGER,
    age INTEGER,
    bmi DECIMAL(10,2),
    customer_type VARCHAR(50),
    scan_count INTEGER,
    last_scan_date VARCHAR(50)
)
DISTSTYLE AUTO
SORTKEY (id, created);

-- Table 2: size_scans
DROP TABLE IF EXISTS qspos.size_scans CASCADE;
CREATE TABLE qspos.size_scans (
    scan_id VARCHAR(100) PRIMARY KEY,
    user_id VARCHAR(100),
    associate_login_email VARCHAR(200),
    scanning_mode VARCHAR(50),
    store_num INTEGER,
    app VARCHAR(100),
    date VARCHAR(50),
    source_metadata VARCHAR(MAX),
    tar VARCHAR(500),
    mesh VARCHAR(500),
    measures VARCHAR(500),
    weight INTEGER,
    pose_count INTEGER,
    distance INTEGER,
    gender VARCHAR(20),
    age INTEGER,
    height INTEGER,
    type VARCHAR(100),
    date_partition INTEGER,
    process_date VARCHAR(50),
    load_filename VARCHAR(500),
    load_timestamp VARCHAR(50),
    pipeline VARCHAR(100),
    status VARCHAR(50),
    year INTEGER,
    month INTEGER,
    multiscan_num VARCHAR(10),
    pipeline_metadata VARCHAR(MAX),
    scan_quality VARCHAR(50),
    retry_count INTEGER,
    confidence_score DECIMAL(10,2)
)
DISTSTYLE AUTO
SORTKEY (scan_id, date);

-- Table 3: size_app_measures
DROP TABLE IF EXISTS qspos.size_app_measures CASCADE;
CREATE TABLE qspos.size_app_measures (
    inc_id INTEGER PRIMARY KEY,
    scan_id VARCHAR(100),
    bmctotal DECIMAL(10,2),
    bodyfat DECIMAL(10,2),
    fitness DECIMAL(10,2),
    leanbodymass DECIMAL(10,2),
    leanmassarms DECIMAL(10,2),
    leanmasslegs DECIMAL(10,2),
    shoulderwidth DECIMAL(10,2),
    visceraladiposetissue DECIMAL(10,2),
    weight DECIMAL(10,2),
    neck DECIMAL(10,2),
    chest DECIMAL(10,2),
    underbust DECIMAL(10,2),
    overarm DECIMAL(10,2),
    bicepleft DECIMAL(10,2),
    bicepright DECIMAL(10,2),
    forearmleft DECIMAL(10,2),
    forearmright DECIMAL(10,2),
    wristleft DECIMAL(10,2),
    wristright DECIMAL(10,2),
    stomach DECIMAL(10,2),
    seat DECIMAL(10,2),
    thighleft DECIMAL(10,2),
    thighright DECIMAL(10,2),
    calfleft DECIMAL(10,2),
    calfright DECIMAL(10,2),
    waist DECIMAL(10,2),
    bodysurfacearea DECIMAL(10,2),
    pantwaist DECIMAL(10,2),
    backneck2waist DECIMAL(10,2),
    sleeveleft DECIMAL(10,2),
    sleeveright DECIMAL(10,2),
    acrossshoulder DECIMAL(10,2),
    crotchlength DECIMAL(10,2),
    inseam DECIMAL(10,2),
    chestcb DECIMAL(10,2),
    hipscb DECIMAL(10,2),
    outseamleft DECIMAL(10,2),
    outseamright DECIMAL(10,2),
    process_date VARCHAR(50),
    load_filename VARCHAR(500),
    load_timestamp VARCHAR(50),
    version VARCHAR(50),
    year INTEGER,
    month INTEGER
)
DISTSTYLE AUTO
SORTKEY (scan_id, inc_id);

-- Table 4: size_dxl_custom_measures
DROP TABLE IF EXISTS qspos.size_dxl_custom_measures CASCADE;
CREATE TABLE qspos.size_dxl_custom_measures (
    inc_id INTEGER PRIMARY KEY,
    scan_id VARCHAR(100),
    producttype VARCHAR(100),
    details VARCHAR(500),
    chest DECIMAL(10,2),
    height DECIMAL(10,2),
    inseamleft DECIMAL(10,2),
    inseamright DECIMAL(10,2),
    neck DECIMAL(10,2),
    outseamleft DECIMAL(10,2),
    outseamright DECIMAL(10,2),
    overarmcircumference DECIMAL(10,2),
    seatmeasurement DECIMAL(10,2),
    shirtwaist DECIMAL(10,2),
    sleeveleft DECIMAL(10,2),
    sleeveright DECIMAL(10,2),
    trouserwaist DECIMAL(10,2),
    load_filename VARCHAR(500),
    process_date VARCHAR(50),
    load_timestamp VARCHAR(50),
    version VARCHAR(50),
    brand VARCHAR(100),
    year INTEGER,
    month INTEGER,
    thighleft DECIMAL(10,2),
    wristleft DECIMAL(10,2),
    shoulderwidth DECIMAL(10,2),
    wristright DECIMAL(10,2),
    thighright DECIMAL(10,2),
    overarm DECIMAL(10,2),
    chestcb DECIMAL(10,2),
    bicepleft DECIMAL(10,2),
    hipscb DECIMAL(10,2),
    bicepright DECIMAL(10,2),
    waist DECIMAL(10,2),
    stomach DECIMAL(10,2)
)
DISTSTYLE AUTO
SORTKEY (scan_id, inc_id);

-- Table 5: size_core_measures
DROP TABLE IF EXISTS qspos.size_core_measures CASCADE;
CREATE TABLE qspos.size_core_measures (
    scan_id VARCHAR(100),
    measurement_name VARCHAR(200),
    measurement_value DECIMAL(10,2),
    landmark_name VARCHAR(200),
    landmark_coordinates_x DECIMAL(18,8),
    landmark_coordinates_y DECIMAL(18,8),
    landmark_coordinates_z DECIMAL(18,8),
    process_date VARCHAR(50),
    load_filename VARCHAR(500),
    load_timestamp VARCHAR(50),
    version VARCHAR(50),
    function_type VARCHAR(100),
    year INTEGER,
    month INTEGER
)
DISTSTYLE AUTO
SORTKEY (scan_id, landmark_name);

-- ============================================================================
-- CUSTOMER/CRM TABLES (8 tables)
-- ============================================================================

-- Table 6: customer
DROP TABLE IF EXISTS qspos.customer CASCADE;
CREATE TABLE qspos.customer (
    customer_id BIGINT PRIMARY KEY,
    language_code VARCHAR(10),
    alpha_key VARCHAR(50),
    phonetic_key VARCHAR(50),
    customer_no VARCHAR(50),
    title VARCHAR(20),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    gender VARCHAR(10),
    marital_status VARCHAR(10),
    next_address_id INTEGER,
    distribution_status INTEGER,
    landmark_date_a VARCHAR(50),
    landmark_date_b VARCHAR(50),
    segmentation_value_a VARCHAR(50),
    segmentation_value_b VARCHAR(50),
    segmentation_value_c VARCHAR(50),
    segmentation_value_d VARCHAR(50),
    segmentation_code_a VARCHAR(10),
    segmentation_code_b VARCHAR(10),
    segmentation_code_c VARCHAR(10),
    segmentation_code_d VARCHAR(10),
    segmentation_flag_a INTEGER,
    segmentation_flag_b INTEGER,
    segmentation_flag_c INTEGER,
    segmentation_flag_d INTEGER,
    segmentation_flag_e INTEGER,
    segmentation_flag_f INTEGER,
    status VARCHAR(10),
    salutation VARCHAR(200),
    head_of_household_flag INTEGER,
    timestamp VARCHAR(50),
    original_division_id INTEGER,
    company_name VARCHAR(200),
    job_title VARCHAR(100),
    birth_date VARCHAR(50),
    birth_day INTEGER,
    is_complete INTEGER,
    complete_date VARCHAR(50),
    complete_modify_date VARCHAR(50),
    system_modify_date VARCHAR(50)
)
DISTSTYLE AUTO
SORTKEY (customer_id, last_name);

-- Table 7: address
DROP TABLE IF EXISTS qspos.address CASCADE;
CREATE TABLE qspos.address (
    customer_id BIGINT,
    address_id INTEGER,
    country_code VARCHAR(10),
    address_match_key VARCHAR(100),
    address_type_code VARCHAR(20),
    mail_indicator INTEGER,
    carrier_route VARCHAR(50),
    address_ncoa_date VARCHAR(50),
    address_1 VARCHAR(200),
    address_2 VARCHAR(200),
    address_3 VARCHAR(100),
    address_4 VARCHAR(50),
    address_5 VARCHAR(100),
    address_6 VARCHAR(100),
    post_code VARCHAR(50),
    date_last_modified VARCHAR(50),
    address_error VARCHAR(50),
    address_longitude DECIMAL(18,8),
    address_latitude DECIMAL(18,8),
    timestamp VARCHAR(50),
    create_store_no INTEGER,
    modify_store_no INTEGER,
    create_user_id INTEGER,
    create_date VARCHAR(50),
    modify_user_id INTEGER,
    create_source_id INTEGER,
    create_comment VARCHAR(200),
    modify_source_id INTEGER,
    modify_comment VARCHAR(200),
    posted_date VARCHAR(50),
    old_customer_id VARCHAR(50),
    temp_old_cust_no VARCHAR(50),
    PRIMARY KEY (customer_id, address_id)
)
DISTSTYLE AUTO
SORTKEY (customer_id, address_id);

-- Table 8: email
DROP TABLE IF EXISTS qspos.email CASCADE;
CREATE TABLE qspos.email (
    customer_id BIGINT,
    email_id INTEGER,
    email_address VARCHAR(200),
    email_type VARCHAR(50),
    is_valid INTEGER,
    opt_in INTEGER,
    opt_in_date VARCHAR(50),
    bounce_count INTEGER,
    last_verified VARCHAR(50),
    create_date VARCHAR(50),
    modify_date VARCHAR(50),
    create_user_id INTEGER,
    modify_user_id INTEGER,
    PRIMARY KEY (customer_id, email_id)
)
DISTSTYLE AUTO
SORTKEY (customer_id, email_id);

-- Table 9: store
DROP TABLE IF EXISTS qspos.store CASCADE;
CREATE TABLE qspos.store (
    store_no INTEGER PRIMARY KEY,
    division_id INTEGER,
    store_short_name VARCHAR(100),
    store_name VARCHAR(200),
    next_customer_no BIGINT,
    sales_associate_no_default INTEGER,
    store_country_code VARCHAR(10),
    reward_redemption_flag INTEGER,
    real_time_rewards_flag INTEGER,
    timestamp VARCHAR(50),
    sales_channel_code VARCHAR(50),
    division_set_id INTEGER,
    eom_id VARCHAR(50)
)
DISTSTYLE AUTO
SORTKEY (store_no);

-- Table 10: transaction_header
DROP TABLE IF EXISTS qspos.transaction_header CASCADE;
CREATE TABLE qspos.transaction_header (
    transaction_id BIGINT PRIMARY KEY,
    sales_module_transaction_id INTEGER,
    transaction_source INTEGER,
    tender_type VARCHAR(50),
    store_no INTEGER,
    customer_id BIGINT,
    sales_associate_no INTEGER,
    transaction_type VARCHAR(10),
    transaction_date VARCHAR(50),
    pos_transaction_no INTEGER,
    register_no INTEGER,
    segmentation_flag_a INTEGER,
    segmentation_flag_b INTEGER,
    segmentation_flag_c INTEGER,
    segmentation_flag_d INTEGER,
    segmentation_flag_e INTEGER,
    segmentation_flag_f INTEGER,
    segmentation_flag_g INTEGER,
    segmentation_flag_h INTEGER,
    customer_no_flag INTEGER,
    total_net_retail DECIMAL(18,2),
    no_transaction_lines INTEGER,
    reward_points_flag INTEGER,
    total_net_retail_central DECIMAL(18,2),
    exchange_rate DECIMAL(18,6),
    currency_code VARCHAR(10),
    posted_date VARCHAR(50),
    transaction_time VARCHAR(50),
    tender_amount_total DECIMAL(18,2),
    tender_amount_total_central DECIMAL(18,2),
    no_tender_lines INTEGER
)
DISTSTYLE AUTO
SORTKEY (transaction_id, transaction_date);

-- Table 11: transaction_detail
DROP TABLE IF EXISTS qspos.transaction_detail CASCADE;
CREATE TABLE qspos.transaction_detail (
    transaction_id BIGINT,
    transaction_line_no INTEGER,
    sale_or_return_indicator VARCHAR(10),
    sales_associate_no INTEGER,
    style_id INTEGER,
    color_code INTEGER,
    size_description VARCHAR(50),
    quantity INTEGER,
    net_retail DECIMAL(18,2),
    cost DECIMAL(18,2),
    markdown_percent DECIMAL(10,2),
    comments VARCHAR(200),
    promotion_flag INTEGER,
    class_code BIGINT,
    net_retail_central DECIMAL(18,2),
    cost_central DECIMAL(18,2),
    markdown_amount DECIMAL(18,2),
    markdown_amount_central DECIMAL(18,2),
    PRIMARY KEY (transaction_id, transaction_line_no)
)
DISTSTYLE AUTO
SORTKEY (transaction_id, transaction_line_no);

-- Table 12: reward_detail
DROP TABLE IF EXISTS qspos.reward_detail CASCADE;
CREATE TABLE qspos.reward_detail (
    reward_transaction_id BIGINT,
    line_no INTEGER,
    class_code BIGINT,
    style_id INTEGER,
    quantity INTEGER,
    net_retail DECIMAL(18,2),
    markdown_percent DECIMAL(10,2),
    coupon_code VARCHAR(50),
    regular_points INTEGER,
    bonus_points INTEGER,
    net_retail_central DECIMAL(18,2),
    header_bonus_points INTEGER,
    tender_bonus_points INTEGER,
    return_flag INTEGER,
    original_reward_tran_id VARCHAR(50),
    original_reward_line_no VARCHAR(50),
    returned_quantity INTEGER,
    exchange_for_line_no VARCHAR(50),
    PRIMARY KEY (reward_transaction_id, line_no)
)
DISTSTYLE AUTO
SORTKEY (reward_transaction_id, line_no);

-- Table 13: household
DROP TABLE IF EXISTS qspos.household CASCADE;
CREATE TABLE qspos.household (
    household_id INTEGER PRIMARY KEY,
    household_match_key VARCHAR(100)
)
DISTSTYLE AUTO
SORTKEY (household_id);

-- ============================================================================
-- ORDER/E-COMMERCE TABLES (7 tables)
-- ============================================================================

-- Table 14: orderheader
DROP TABLE IF EXISTS qspos.orderheader CASCADE;
CREATE TABLE qspos.orderheader (
    orderid BIGINT PRIMARY KEY,
    createdtimestamp VARCHAR(50),
    iscancelled BOOLEAN,
    isconfirmed BOOLEAN,
    maxfulfillmentstatusid INTEGER,
    minfulfillmentstatusid INTEGER,
    ordertypeid VARCHAR(50),
    orgid VARCHAR(50),
    sellinglocationid VARCHAR(50),
    messageid VARCHAR(100),
    utmcampaign VARCHAR(100),
    utmmedium VARCHAR(50),
    utmsource VARCHAR(50),
    customeremail VARCHAR(200),
    fulfillmentstatus VARCHAR(50),
    alternateorderid VARCHAR(50),
    order_source VARCHAR(50),
    payment_method VARCHAR(50),
    shipping_method VARCHAR(50),
    customer_type VARCHAR(50),
    device_type VARCHAR(50),
    browser VARCHAR(50)
)
DISTSTYLE AUTO
SORTKEY (orderid, createdtimestamp);

-- Table 15: orderline
DROP TABLE IF EXISTS qspos.orderline CASCADE;
CREATE TABLE qspos.orderline (
    orderlineid INTEGER,
    orderid BIGINT,
    itemid INTEGER,
    cancelledtotaldiscounts DECIMAL(18,2),
    maxappeasementamount DECIMAL(18,2),
    orderlinesubtotal DECIMAL(18,2),
    orderlinetotal DECIMAL(18,2),
    quantity INTEGER,
    refundprice DECIMAL(18,2),
    returnlinetotalwithoutfees DECIMAL(18,2),
    returnablelinetotal DECIMAL(18,2),
    returnablequantity INTEGER,
    taxoverridevalue DECIMAL(18,2),
    taxableamount DECIMAL(18,2),
    totalcharges DECIMAL(18,2),
    totaldiscountonitem DECIMAL(18,2),
    totaldiscounts DECIMAL(18,2),
    totaltaxes DECIMAL(18,2),
    unitprice DECIMAL(18,2),
    messageid VARCHAR(100),
    maxfulfillmentstatusid INTEGER,
    minfulfillmentstatusid INTEGER,
    fulfillmentstatus VARCHAR(50),
    isonhold BOOLEAN,
    isreturn BOOLEAN,
    isevenexchange BOOLEAN,
    iscancelled BOOLEAN,
    parentorderlineid VARCHAR(50),
    parentorderid VARCHAR(50),
    createdtimestamp VARCHAR(50),
    orderline_pk VARCHAR(50),
    PRIMARY KEY (orderid, orderlineid)
)
DISTSTYLE AUTO
SORTKEY (orderid, orderlineid);

-- Table 16: orderline_items
DROP TABLE IF EXISTS qspos.orderline_items CASCADE;
CREATE TABLE qspos.orderline_items (
    itemid INTEGER PRIMARY KEY,
    itembarcode VARCHAR(100),
    itembrand VARCHAR(100),
    itemcolordescription VARCHAR(100),
    itemdepartmentname VARCHAR(100),
    itemdepartmentnumber VARCHAR(50),
    itemdescription VARCHAR(MAX),
    itemseason VARCHAR(50),
    itemsize VARCHAR(50),
    itemstyle VARCHAR(50),
    itemtaxcode VARCHAR(50),
    originalunitprice DECIMAL(18,2),
    itemshortdescription VARCHAR(500)
)
DISTSTYLE AUTO
SORTKEY (itemid);

-- Table 17: orderchargedetail
DROP TABLE IF EXISTS qspos.orderchargedetail CASCADE;
CREATE TABLE qspos.orderchargedetail (
    orderid BIGINT,
    taxcode VARCHAR(50),
    chargetotal DECIMAL(18,2),
    istaxincluded BOOLEAN,
    isoverridden BOOLEAN,
    originalchargeamount DECIMAL(18,2),
    isinformational BOOLEAN,
    isprorated BOOLEAN,
    fulfillmentgroupid VARCHAR(50),
    isorderdiscount BOOLEAN,
    isreturncharge BOOLEAN,
    isproratedatsamelevel BOOLEAN,
    chargetypeid VARCHAR(50),
    chargedisplayname VARCHAR(100)
)
DISTSTYLE AUTO
SORTKEY (orderid);

-- Table 18: invoice
DROP TABLE IF EXISTS qspos.invoice CASCADE;
CREATE TABLE qspos.invoice (
    invoiceid BIGINT PRIMARY KEY,
    invoice_pk VARCHAR(50),
    orderid BIGINT,
    orderpk VARCHAR(50),
    createdtimestamp VARCHAR(50),
    cleanuptaskid VARCHAR(50),
    errordescription VARCHAR(200),
    iserror BOOLEAN,
    publishcount INTEGER,
    process VARCHAR(50),
    failedamount DECIMAL(18,2),
    fulfillmentdate VARCHAR(50),
    sellinglocationid VARCHAR(50),
    updatedby VARCHAR(200),
    amountprocessed DECIMAL(18,2),
    totalcharges DECIMAL(18,2),
    invoicesubtotal DECIMAL(18,2),
    parentorderid VARCHAR(50),
    taxexemptid VARCHAR(50),
    totaltaxes DECIMAL(18,2),
    totaldiscounts DECIMAL(18,2),
    publishstatusid INTEGER,
    statusid INTEGER,
    updatedtimestamp VARCHAR(50),
    createdby VARCHAR(200),
    invoicetypeid VARCHAR(50),
    customerid VARCHAR(50),
    orgid VARCHAR(50),
    contextid VARCHAR(100),
    packageid VARCHAR(50),
    invoicetotal DECIMAL(18,2),
    unique_identifier VARCHAR(100),
    invoiceadditional VARCHAR(MAX),
    messageid VARCHAR(100),
    load_date VARCHAR(50),
    update_date VARCHAR(50)
)
DISTSTYLE AUTO
SORTKEY (invoiceid, orderid);

-- Table 19: payment
DROP TABLE IF EXISTS qspos.payment CASCADE;
CREATE TABLE qspos.payment (
    payment_pk VARCHAR(50) PRIMARY KEY,
    orderid BIGINT,
    orderpk VARCHAR(50),
    createdby VARCHAR(200),
    createdtimestamp VARCHAR(50),
    updatedby VARCHAR(200),
    updatedtimestamp VARCHAR(50),
    messages VARCHAR(MAX),
    orgid VARCHAR(50),
    paymentgroupid VARCHAR(100),
    customerid VARCHAR(50),
    iscancelled BOOLEAN,
    statusid INTEGER,
    messageid VARCHAR(100),
    load_date VARCHAR(50),
    update_date VARCHAR(50)
)
DISTSTYLE AUTO
SORTKEY (payment_pk, orderid);

-- Table 20: quantitydetail
DROP TABLE IF EXISTS qspos.quantitydetail CASCADE;
CREATE TABLE qspos.quantitydetail (
    quantitydetail_pk VARCHAR(50) PRIMARY KEY,
    quantitydetailid VARCHAR(50),
    orderid BIGINT,
    orderline_pk VARCHAR(50),
    statusid INTEGER,
    updatedtimestamp VARCHAR(50),
    createdby VARCHAR(200),
    createdtimestamp VARCHAR(50),
    quantity INTEGER,
    itemid INTEGER,
    orgid VARCHAR(50),
    updatedby VARCHAR(200),
    uom VARCHAR(10),
    contextid VARCHAR(100),
    messageid VARCHAR(100),
    load_date VARCHAR(50),
    update_date VARCHAR(50)
)
DISTSTYLE AUTO
SORTKEY (quantitydetail_pk, orderid);

-- ============================================================================
-- GRANT PERMISSIONS (Optional - adjust as needed)
-- ============================================================================

-- Grant SELECT to all users (adjust as needed)
-- GRANT SELECT ON ALL TABLES IN SCHEMA qspos TO PUBLIC;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Verify all tables were created
SELECT 
    schemaname,
    tablename,
    tableowner
FROM pg_tables
WHERE schemaname = 'qspos'
ORDER BY tablename;

-- Count tables in schema
SELECT COUNT(*) as table_count
FROM pg_tables
WHERE schemaname = 'qspos';

-- ============================================================================
-- END OF SCRIPT
-- ============================================================================
