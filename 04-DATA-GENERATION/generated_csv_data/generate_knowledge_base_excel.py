"""
Generate Knowledge Base Excel Files for AWS Quick Suite
These files contain business rules, policies, and reference information
"""

import pandas as pd
from datetime import datetime
import random

# Set random seed
random.seed(42)

# ============================================================================
# 1. BUSINESS POLICIES & RULES
# ============================================================================
def create_business_policies_excel():
    print("Creating Business_Policies_Rules.xlsx...")
    
    # Sheet 1: Return Policy
    return_policy = pd.DataFrame([
        {"Policy_ID": "RET001", "Policy_Name": "Standard Return", "Category": "Returns", "Description": "Items can be returned within 60 days of purchase", "Conditions": "Original tags attached, unworn, unwashed", "Refund_Type": "Full Refund", "Processing_Days": 7, "Exceptions": "Final sale items excluded"},
        {"Policy_ID": "RET002", "Policy_Name": "FitMap Guarantee", "Category": "Returns", "Description": "Items purchased with FitMap recommendation", "Conditions": "Size doesn't fit as recommended", "Refund_Type": "Full Refund + Free Return Shipping", "Processing_Days": 3, "Exceptions": "Must have FitMap scan on file"},
        {"Policy_ID": "RET003", "Policy_Name": "Final Sale", "Category": "Returns", "Description": "Clearance items marked as final sale", "Conditions": "No returns or exchanges", "Refund_Type": "None", "Processing_Days": 0, "Exceptions": "Defective items only"},
        {"Policy_ID": "RET004", "Policy_Name": "Gift Returns", "Category": "Returns", "Description": "Items purchased as gifts", "Conditions": "Gift receipt required", "Refund_Type": "Store Credit", "Processing_Days": 7, "Exceptions": "Cannot refund to original payment method"},
        {"Policy_ID": "RET005", "Policy_Name": "Online Returns", "Category": "Returns", "Description": "Items purchased online", "Conditions": "Return label provided", "Refund_Type": "Full Refund", "Processing_Days": 10, "Exceptions": "Customer pays return shipping unless defective"},
    ])
    
    # Sheet 2: Discount Policy
    discount_policy = pd.DataFrame([
        {"Policy_ID": "DIS001", "Policy_Name": "VIP Discount", "Category": "Discounts", "Discount_Percent": 20, "Eligibility": "VIP customers (>$5000 annual spend)", "Stackable": "No", "Exclusions": "Cannot combine with other offers", "Valid_Until": "2025-12-31"},
        {"Policy_ID": "DIS002", "Policy_Name": "First Purchase", "Category": "Discounts", "Discount_Percent": 15, "Eligibility": "New customers, first order", "Stackable": "No", "Exclusions": "Minimum $75 purchase", "Valid_Until": "Ongoing"},
        {"Policy_ID": "DIS003", "Policy_Name": "Birthday Discount", "Category": "Discounts", "Discount_Percent": 25, "Eligibility": "All customers during birthday month", "Stackable": "Yes", "Exclusions": "Valid for 30 days", "Valid_Until": "Ongoing"},
        {"Policy_ID": "DIS004", "Policy_Name": "Military Discount", "Category": "Discounts", "Discount_Percent": 10, "Eligibility": "Active military and veterans", "Stackable": "Yes", "Exclusions": "ID verification required", "Valid_Until": "Ongoing"},
        {"Policy_ID": "DIS005", "Policy_Name": "Employee Discount", "Category": "Discounts", "Discount_Percent": 30, "Eligibility": "DXL employees", "Stackable": "No", "Exclusions": "Not valid on sale items", "Valid_Until": "Ongoing"},
    ])
    
    # Sheet 3: Shipping Policy
    shipping_policy = pd.DataFrame([
        {"Policy_ID": "SHIP001", "Policy_Name": "Free Standard Shipping", "Category": "Shipping", "Threshold": 75.00, "Delivery_Days": "5-7", "Cost": 0.00, "Regions": "Continental US", "Restrictions": "Excludes AK, HI"},
        {"Policy_ID": "SHIP002", "Policy_Name": "Standard Shipping", "Category": "Shipping", "Threshold": 0.00, "Delivery_Days": "5-7", "Cost": 7.99, "Regions": "Continental US", "Restrictions": "None"},
        {"Policy_ID": "SHIP003", "Policy_Name": "Express Shipping", "Category": "Shipping", "Threshold": 0.00, "Delivery_Days": "2-3", "Cost": 15.99, "Regions": "Continental US", "Restrictions": "Order by 2pm EST"},
        {"Policy_ID": "SHIP004", "Policy_Name": "Overnight Shipping", "Category": "Shipping", "Threshold": 0.00, "Delivery_Days": "1", "Cost": 29.99, "Regions": "Continental US", "Restrictions": "Order by 12pm EST"},
        {"Policy_ID": "SHIP005", "Policy_Name": "Alaska/Hawaii", "Category": "Shipping", "Threshold": 0.00, "Delivery_Days": "7-10", "Cost": 19.99, "Regions": "AK, HI", "Restrictions": "No express options"},
    ])
    
    # Sheet 4: Price Match Policy
    price_match = pd.DataFrame([
        {"Policy_ID": "PM001", "Policy_Name": "Competitor Price Match", "Category": "Price Match", "Description": "Match competitor advertised prices", "Conditions": "Identical item, in stock at competitor", "Time_Frame": "14 days from purchase", "Proof_Required": "Yes - ad or website screenshot", "Exclusions": "Online marketplaces, auction sites"},
        {"Policy_ID": "PM002", "Policy_Name": "Own Price Adjustment", "Category": "Price Match", "Description": "Adjust if our price drops", "Conditions": "Item purchased at higher price", "Time_Frame": "30 days from purchase", "Proof_Required": "No - automatic", "Exclusions": "Clearance items"},
    ])
    
    # Sheet 5: Loyalty Program Rules
    loyalty_rules = pd.DataFrame([
        {"Rule_ID": "LOY001", "Program_Name": "DXL Rewards", "Tier": "Basic", "Points_Per_Dollar": 1, "Bonus_Multiplier": 1.0, "Annual_Spend_Min": 0, "Annual_Spend_Max": 999, "Benefits": "Standard points, birthday discount"},
        {"Rule_ID": "LOY002", "Program_Name": "DXL Rewards", "Tier": "Silver", "Points_Per_Dollar": 1, "Bonus_Multiplier": 1.25, "Annual_Spend_Min": 1000, "Annual_Spend_Max": 2499, "Benefits": "25% bonus points, free alterations"},
        {"Rule_ID": "LOY003", "Program_Name": "DXL Rewards", "Tier": "Gold", "Points_Per_Dollar": 1, "Bonus_Multiplier": 1.5, "Annual_Spend_Min": 2500, "Annual_Spend_Max": 4999, "Benefits": "50% bonus points, free shipping, early access"},
        {"Rule_ID": "LOY004", "Program_Name": "DXL Rewards", "Tier": "Platinum", "Points_Per_Dollar": 1, "Bonus_Multiplier": 2.0, "Annual_Spend_Min": 5000, "Annual_Spend_Max": 999999, "Benefits": "Double points, free shipping, concierge service, exclusive events"},
    ])
    
    # Write to Excel with multiple sheets
    with pd.ExcelWriter('Business_Policies_Rules.xlsx', engine='openpyxl') as writer:
        return_policy.to_excel(writer, sheet_name='Return Policy', index=False)
        discount_policy.to_excel(writer, sheet_name='Discount Policy', index=False)
        shipping_policy.to_excel(writer, sheet_name='Shipping Policy', index=False)
        price_match.to_excel(writer, sheet_name='Price Match', index=False)
        loyalty_rules.to_excel(writer, sheet_name='Loyalty Program', index=False)
    
    return 5  # Number of sheets

# ============================================================================
# 2. PRODUCT SPECIFICATIONS & CARE
# ============================================================================
def create_product_specifications_excel():
    print("Creating Product_Specifications_Care.xlsx...")
    
    # Sheet 1: Fabric Care Instructions
    fabric_care = pd.DataFrame([
        {"Fabric_Type": "Cotton", "Washing": "Machine wash cold", "Drying": "Tumble dry low", "Ironing": "Medium heat", "Dry_Clean": "Optional", "Special_Notes": "May shrink if dried on high heat"},
        {"Fabric_Type": "Polyester", "Washing": "Machine wash warm", "Drying": "Tumble dry low", "Ironing": "Low heat", "Dry_Clean": "Not required", "Special_Notes": "Wrinkle resistant"},
        {"Fabric_Type": "Wool", "Washing": "Hand wash cold or dry clean", "Drying": "Lay flat to dry", "Ironing": "Steam only", "Dry_Clean": "Recommended", "Special_Notes": "Do not wring or twist"},
        {"Fabric_Type": "Silk", "Washing": "Hand wash cold", "Drying": "Lay flat to dry", "Ironing": "Low heat, inside out", "Dry_Clean": "Recommended", "Special_Notes": "Use mild detergent"},
        {"Fabric_Type": "Denim", "Washing": "Machine wash cold, inside out", "Drying": "Tumble dry medium", "Ironing": "High heat", "Dry_Clean": "Not required", "Special_Notes": "Wash separately first time"},
        {"Fabric_Type": "Linen", "Washing": "Machine wash cold", "Drying": "Tumble dry low or line dry", "Ironing": "High heat while damp", "Dry_Clean": "Optional", "Special_Notes": "Wrinkles easily"},
        {"Fabric_Type": "Leather", "Washing": "Spot clean only", "Drying": "Air dry", "Ironing": "Do not iron", "Dry_Clean": "Professional only", "Special_Notes": "Condition regularly"},
    ])
    
    # Sheet 2: Size Fit Guide
    fit_guide = pd.DataFrame([
        {"Fit_Type": "Slim Fit", "Description": "Tailored close to body", "Best_For": "Athletic build", "Chest_Allowance": "2-3 inches", "Waist_Allowance": "1-2 inches", "Recommended_Sizes": "XL, 2XL"},
        {"Fit_Type": "Regular Fit", "Description": "Classic comfortable fit", "Best_For": "Most body types", "Chest_Allowance": "4-5 inches", "Waist_Allowance": "3-4 inches", "Recommended_Sizes": "All sizes"},
        {"Fit_Type": "Relaxed Fit", "Description": "Loose and comfortable", "Best_For": "Comfort preference", "Chest_Allowance": "6-7 inches", "Waist_Allowance": "5-6 inches", "Recommended_Sizes": "2XL+"},
        {"Fit_Type": "Athletic Fit", "Description": "Tapered with room in shoulders", "Best_For": "Broad shoulders, narrow waist", "Chest_Allowance": "3-4 inches", "Waist_Allowance": "2-3 inches", "Recommended_Sizes": "XL-4XL"},
        {"Fit_Type": "Big & Tall", "Description": "Extended sizing for larger frames", "Best_For": "Taller or larger builds", "Chest_Allowance": "5-6 inches", "Waist_Allowance": "4-5 inches", "Recommended_Sizes": "3XL+"},
    ])
    
    # Sheet 3: Alteration Services
    alterations = pd.DataFrame([
        {"Service": "Hem Pants", "Description": "Shorten pant length", "Price": 12.00, "Turnaround_Days": 3, "Included_For": "Gold, Platinum members", "Notes": "Original hem available for +$5"},
        {"Service": "Hem Sleeves", "Description": "Shorten shirt/jacket sleeves", "Price": 15.00, "Turnaround_Days": 3, "Included_For": "Gold, Platinum members", "Notes": "Maintain button placement"},
        {"Service": "Take In Waist", "Description": "Reduce waist size", "Price": 18.00, "Turnaround_Days": 5, "Included_For": "Platinum members", "Notes": "Up to 2 inches"},
        {"Service": "Let Out Waist", "Description": "Increase waist size", "Price": 18.00, "Turnaround_Days": 5, "Included_For": "Platinum members", "Notes": "Depends on seam allowance"},
        {"Service": "Taper Legs", "Description": "Slim pant legs", "Price": 20.00, "Turnaround_Days": 5, "Included_For": "None", "Notes": "Maintains original hem"},
        {"Service": "Shorten Jacket", "Description": "Reduce jacket length", "Price": 25.00, "Turnaround_Days": 7, "Included_For": "None", "Notes": "Maintains proportions"},
    ])
    
    # Sheet 4: Quality Standards
    quality_standards = pd.DataFrame([
        {"Category": "Shirts", "Stitch_Count_Per_Inch": "8-10", "Seam_Type": "Double-stitched", "Button_Quality": "Reinforced", "Inspection_Points": "Collar, cuffs, placket, seams", "Defect_Tolerance": "0%"},
        {"Category": "Pants", "Stitch_Count_Per_Inch": "8-10", "Seam_Type": "Flat-felled", "Button_Quality": "Metal shank", "Inspection_Points": "Waistband, fly, inseam, pockets", "Defect_Tolerance": "0%"},
        {"Category": "Outerwear", "Stitch_Count_Per_Inch": "10-12", "Seam_Type": "Double-stitched, reinforced", "Button_Quality": "Heavy-duty", "Inspection_Points": "Zippers, lining, shoulders, seams", "Defect_Tolerance": "0%"},
        {"Category": "Footwear", "Stitch_Count_Per_Inch": "N/A", "Seam_Type": "Cemented or stitched", "Button_Quality": "N/A", "Inspection_Points": "Sole attachment, stitching, laces, insole", "Defect_Tolerance": "0%"},
    ])
    
    # Write to Excel
    with pd.ExcelWriter('Product_Specifications_Care.xlsx', engine='openpyxl') as writer:
        fabric_care.to_excel(writer, sheet_name='Fabric Care', index=False)
        fit_guide.to_excel(writer, sheet_name='Fit Guide', index=False)
        alterations.to_excel(writer, sheet_name='Alteration Services', index=False)
        quality_standards.to_excel(writer, sheet_name='Quality Standards', index=False)
    
    return 4

# ============================================================================
# 3. FITMAP GUIDELINES & BEST PRACTICES
# ============================================================================
def create_fitmap_guidelines_excel():
    print("Creating FitMap_Guidelines_Best_Practices.xlsx...")
    
    # Sheet 1: Scanning Best Practices
    scanning_practices = pd.DataFrame([
        {"Practice_ID": "SCAN001", "Category": "Preparation", "Practice": "Wear form-fitting clothing", "Importance": "Critical", "Reason": "Loose clothing affects measurement accuracy", "Impact_On_Accuracy": "±2 inches"},
        {"Practice_ID": "SCAN002", "Category": "Preparation", "Practice": "Remove shoes", "Importance": "Required", "Reason": "Shoes affect height and posture measurements", "Impact_On_Accuracy": "±1 inch"},
        {"Practice_ID": "SCAN003", "Category": "Preparation", "Practice": "Empty pockets", "Importance": "Recommended", "Reason": "Items in pockets create measurement distortions", "Impact_On_Accuracy": "±0.5 inches"},
        {"Practice_ID": "SCAN004", "Category": "Environment", "Practice": "Good lighting", "Importance": "Critical", "Reason": "Camera needs clear view of body outline", "Impact_On_Accuracy": "Scan may fail"},
        {"Practice_ID": "SCAN005", "Category": "Environment", "Practice": "Plain background", "Importance": "Recommended", "Reason": "Busy backgrounds confuse body detection", "Impact_On_Accuracy": "±1 inch"},
        {"Practice_ID": "SCAN006", "Category": "Positioning", "Practice": "Stand 6 feet from device", "Importance": "Critical", "Reason": "Optimal distance for full body capture", "Impact_On_Accuracy": "Scan may fail"},
        {"Practice_ID": "SCAN007", "Category": "Positioning", "Practice": "Arms slightly away from body", "Importance": "Critical", "Reason": "Allows accurate torso measurement", "Impact_On_Accuracy": "±2 inches"},
        {"Practice_ID": "SCAN008", "Category": "Positioning", "Practice": "Feet shoulder-width apart", "Importance": "Required", "Reason": "Proper stance for leg measurements", "Impact_On_Accuracy": "±1 inch"},
    ])
    
    # Sheet 2: Measurement Accuracy Guidelines
    accuracy_guidelines = pd.DataFrame([
        {"Measurement": "Chest", "Expected_Accuracy": "±0.5 inches", "Confidence_Threshold": "95%", "Retry_If_Below": "90%", "Common_Issues": "Arms too close to body", "Resolution": "Rescan with arms away"},
        {"Measurement": "Waist", "Expected_Accuracy": "±0.5 inches", "Confidence_Threshold": "95%", "Retry_If_Below": "90%", "Common_Issues": "Loose clothing", "Resolution": "Wear fitted shirt"},
        {"Measurement": "Inseam", "Expected_Accuracy": "±0.75 inches", "Confidence_Threshold": "92%", "Retry_If_Below": "85%", "Common_Issues": "Baggy pants", "Resolution": "Wear fitted pants"},
        {"Measurement": "Neck", "Expected_Accuracy": "±0.25 inches", "Confidence_Threshold": "98%", "Retry_If_Below": "95%", "Common_Issues": "Collar interference", "Resolution": "Remove collar or wear crew neck"},
        {"Measurement": "Sleeve", "Expected_Accuracy": "±0.5 inches", "Confidence_Threshold": "95%", "Retry_If_Below": "90%", "Common_Issues": "Bent arms", "Resolution": "Keep arms straight"},
        {"Measurement": "Shoulder Width", "Expected_Accuracy": "±0.5 inches", "Confidence_Threshold": "96%", "Retry_If_Below": "92%", "Common_Issues": "Poor posture", "Resolution": "Stand straight, shoulders back"},
    ])
    
    # Sheet 3: Size Recommendation Logic
    recommendation_logic = pd.DataFrame([
        {"Product_Category": "Dress Shirts", "Primary_Measurement": "Neck", "Secondary_Measurement": "Sleeve", "Tertiary_Measurement": "Chest", "Fit_Preference_Impact": "High", "Recommendation_Algorithm": "Neck exact match, sleeve ±0.5, chest +2-4 inches"},
        {"Product_Category": "Casual Shirts", "Primary_Measurement": "Chest", "Secondary_Measurement": "Waist", "Tertiary_Measurement": "Sleeve", "Fit_Preference_Impact": "Medium", "Recommendation_Algorithm": "Chest +4-6 inches based on fit preference"},
        {"Product_Category": "Dress Pants", "Primary_Measurement": "Waist", "Secondary_Measurement": "Inseam", "Tertiary_Measurement": "Hip", "Fit_Preference_Impact": "Low", "Recommendation_Algorithm": "Waist exact match, inseam exact, hip +2-3 inches"},
        {"Product_Category": "Jeans", "Primary_Measurement": "Waist", "Secondary_Measurement": "Inseam", "Tertiary_Measurement": "Thigh", "Fit_Preference_Impact": "High", "Recommendation_Algorithm": "Waist -1 to +1 inch, inseam exact, fit preference determines thigh room"},
        {"Product_Category": "Suits", "Primary_Measurement": "Chest", "Secondary_Measurement": "Waist", "Tertiary_Measurement": "Sleeve", "Fit_Preference_Impact": "Medium", "Recommendation_Algorithm": "Chest +4-5 inches, waist +3-4 inches, sleeve exact"},
        {"Product_Category": "Outerwear", "Primary_Measurement": "Chest", "Secondary_Measurement": "Sleeve", "Tertiary_Measurement": "Shoulder", "Fit_Preference_Impact": "Low", "Recommendation_Algorithm": "Chest +6-8 inches for layering, sleeve +0.5 inch"},
    ])
    
    # Sheet 4: Troubleshooting Guide
    troubleshooting = pd.DataFrame([
        {"Issue": "Scan fails to complete", "Possible_Cause": "Poor lighting", "Solution": "Move to well-lit area", "Prevention": "Check lighting before starting", "Success_Rate": "95%"},
        {"Issue": "Scan fails to complete", "Possible_Cause": "Too close/far from camera", "Solution": "Adjust distance to 6 feet", "Prevention": "Use floor markers", "Success_Rate": "98%"},
        {"Issue": "Measurements seem inaccurate", "Possible_Cause": "Loose clothing", "Solution": "Rescan with fitted clothing", "Prevention": "Provide clothing guidelines upfront", "Success_Rate": "92%"},
        {"Issue": "Low confidence score", "Possible_Cause": "Movement during scan", "Solution": "Rescan, remain still", "Prevention": "Explain importance of staying still", "Success_Rate": "97%"},
        {"Issue": "Recommendation doesn't fit", "Possible_Cause": "Fit preference not captured", "Solution": "Update fit preference, rescan", "Prevention": "Ask fit preference before scanning", "Success_Rate": "90%"},
        {"Issue": "Customer refuses scan", "Possible_Cause": "Privacy concerns", "Solution": "Explain data privacy policy", "Prevention": "Proactive privacy communication", "Success_Rate": "85%"},
    ])
    
    # Write to Excel
    with pd.ExcelWriter('FitMap_Guidelines_Best_Practices.xlsx', engine='openpyxl') as writer:
        scanning_practices.to_excel(writer, sheet_name='Scanning Best Practices', index=False)
        accuracy_guidelines.to_excel(writer, sheet_name='Accuracy Guidelines', index=False)
        recommendation_logic.to_excel(writer, sheet_name='Recommendation Logic', index=False)
        troubleshooting.to_excel(writer, sheet_name='Troubleshooting', index=False)
    
    return 4

# ============================================================================
# 4. EMPLOYEE TRAINING & PROCEDURES
# ============================================================================
def create_employee_training_excel():
    print("Creating Employee_Training_Procedures.xlsx...")
    
    # Sheet 1: Customer Service Scripts
    service_scripts = pd.DataFrame([
        {"Scenario": "Greeting Customer", "Script": "Welcome to DXL! My name is [Name]. How can I help you find the perfect fit today?", "Key_Points": "Smile, make eye contact, mention fit", "Do": "Be warm and welcoming", "Don't": "Rush the greeting"},
        {"Scenario": "Introducing FitMap", "Script": "Have you tried our FitMap body scanning? It takes 30 seconds and ensures perfect fit every time.", "Key_Points": "Emphasize speed and accuracy", "Do": "Offer demonstration", "Don't": "Pressure if declined"},
        {"Scenario": "Handling Returns", "Script": "I'd be happy to help with that return. Do you have your receipt? Let me check our return policy for you.", "Key_Points": "Stay positive, check policy", "Do": "Process efficiently", "Don't": "Make customer feel bad"},
        {"Scenario": "Size Not Available", "Script": "I don't have that size in store, but I can order it for you with free shipping to your home or this store.", "Key_Points": "Offer alternatives immediately", "Do": "Check online inventory", "Don't": "Just say no"},
        {"Scenario": "Price Match Request", "Script": "We do offer price matching! Let me verify the competitor's price and process that for you.", "Key_Points": "Know policy, verify proof", "Do": "Honor valid requests", "Don't": "Argue about policy"},
    ])
    
    # Sheet 2: Sales Techniques
    sales_techniques = pd.DataFrame([
        {"Technique": "Upselling", "Description": "Suggest premium version of selected item", "When_To_Use": "Customer shows interest in product", "Example": "This shirt also comes in our premium cotton blend", "Success_Rate": "35%", "Training_Required": "Basic"},
        {"Technique": "Cross-Selling", "Description": "Suggest complementary items", "When_To_Use": "Customer selects main item", "Example": "These pants pair perfectly with this belt", "Success_Rate": "45%", "Training_Required": "Basic"},
        {"Technique": "Bundle Selling", "Description": "Offer package deals", "When_To_Use": "Customer buying multiple items", "Example": "Buy 2 shirts, get 1 at 50% off", "Success_Rate": "55%", "Training_Required": "Intermediate"},
        {"Technique": "FitMap Conversion", "Description": "Convert browser to FitMap user", "When_To_Use": "Customer unsure about size", "Example": "Let's do a quick scan to find your perfect size", "Success_Rate": "65%", "Training_Required": "Advanced"},
        {"Technique": "Loyalty Enrollment", "Description": "Sign up for rewards program", "When_To_Use": "At checkout", "Example": "Join our rewards program and earn points today", "Success_Rate": "40%", "Training_Required": "Basic"},
    ])
    
    # Sheet 3: Store Opening/Closing Procedures
    procedures = pd.DataFrame([
        {"Procedure": "Store Opening", "Step": 1, "Task": "Arrive 30 minutes before opening", "Responsible": "Manager", "Time_Required": "5 min", "Critical": "Yes"},
        {"Procedure": "Store Opening", "Step": 2, "Task": "Unlock doors and disable alarm", "Responsible": "Manager", "Time_Required": "2 min", "Critical": "Yes"},
        {"Procedure": "Store Opening", "Step": 3, "Task": "Turn on lights and music", "Responsible": "Any associate", "Time_Required": "3 min", "Critical": "No"},
        {"Procedure": "Store Opening", "Step": 4, "Task": "Boot up POS systems", "Responsible": "Any associate", "Time_Required": "5 min", "Critical": "Yes"},
        {"Procedure": "Store Opening", "Step": 5, "Task": "Count cash drawer", "Responsible": "Manager", "Time_Required": "10 min", "Critical": "Yes"},
        {"Procedure": "Store Opening", "Step": 6, "Task": "Check FitMap devices", "Responsible": "Tech associate", "Time_Required": "5 min", "Critical": "Yes"},
        {"Procedure": "Store Closing", "Step": 1, "Task": "Lock front doors", "Responsible": "Manager", "Time_Required": "1 min", "Critical": "Yes"},
        {"Procedure": "Store Closing", "Step": 2, "Task": "Count cash drawer", "Responsible": "Manager", "Time_Required": "15 min", "Critical": "Yes"},
        {"Procedure": "Store Closing", "Step": 3, "Task": "Prepare bank deposit", "Responsible": "Manager", "Time_Required": "10 min", "Critical": "Yes"},
        {"Procedure": "Store Closing", "Step": 4, "Task": "Shut down POS systems", "Responsible": "Any associate", "Time_Required": "5 min", "Critical": "Yes"},
        {"Procedure": "Store Closing", "Step": 5, "Task": "Turn off lights and music", "Responsible": "Any associate", "Time_Required": "3 min", "Critical": "No"},
        {"Procedure": "Store Closing", "Step": 6, "Task": "Set alarm and lock doors", "Responsible": "Manager", "Time_Required": "2 min", "Critical": "Yes"},
    ])
    
    # Write to Excel
    with pd.ExcelWriter('Employee_Training_Procedures.xlsx', engine='openpyxl') as writer:
        service_scripts.to_excel(writer, sheet_name='Customer Service Scripts', index=False)
        sales_techniques.to_excel(writer, sheet_name='Sales Techniques', index=False)
        procedures.to_excel(writer, sheet_name='Store Procedures', index=False)
    
    return 3

# ============================================================================
# MAIN EXECUTION
# ============================================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("GENERATING KNOWLEDGE BASE EXCEL FILES")
    print("="*70)
    print("\nThese files will be uploaded to Quick Suite Knowledge Base")
    print("to provide business context and answer policy questions.\n")
    
    results = {}
    
    results['Business_Policies_Rules.xlsx'] = create_business_policies_excel()
    results['Product_Specifications_Care.xlsx'] = create_product_specifications_excel()
    results['FitMap_Guidelines_Best_Practices.xlsx'] = create_fitmap_guidelines_excel()
    results['Employee_Training_Procedures.xlsx'] = create_employee_training_excel()
    
    print("\n" + "="*70)
    print("KNOWLEDGE BASE EXCEL GENERATION COMPLETE")
    print("="*70)
    
    for filename, sheet_count in results.items():
        print(f"[OK] {filename}: {sheet_count} sheets")
    
    print("="*70)
    print(f"\nTotal files: {len(results)}")
    print(f"Total sheets: {sum(results.values())}")
    print("\nThese Excel files contain:")
    print("  • Business policies and rules")
    print("  • Product specifications and care instructions")
    print("  • FitMap guidelines and best practices")
    print("  • Employee training and procedures")
    print("\nUpload these to Quick Suite Knowledge Base to enable")
    print("policy-aware responses and business rule enforcement.")
    print("="*70 + "\n")
