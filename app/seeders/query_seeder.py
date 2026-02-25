from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.query import Query
from app.models.user import User
from datetime import datetime, timedelta
import random


async def seed_queries(db: AsyncSession) -> list[Query]:
    """Seed queries table with sample data"""
    
    # Check if queries already exist
    result = await db.execute(select(Query).limit(1))
    if result.scalar_one_or_none():
        print("Queries already seeded, skipping...")
        return []
    
    # Get all users
    result = await db.execute(select(User))
    users = result.scalars().all()
    
    if not users:
        print("⚠ No users found. Please seed users first.")
        return []
    
    queries_data = [
        {
            "question": "How do I calibrate the X-Ray machine model RX-2000?",
            "response": "To calibrate the RX-2000 X-Ray machine: 1) Access the service menu using code *#2000. 2) Navigate to 'Calibration Settings'. 3) Run the automatic calibration sequence. 4) Verify the output readings match the reference values in the manual (page 45)."
        },
        {
            "question": "What are the maintenance steps for the MRI scanner?",
            "response": "Regular MRI maintenance includes: 1) Weekly: Check cooling system levels and filters. 2) Monthly: Inspect RF coils for damage. 3) Quarterly: Test emergency shutdown systems. 4) Annually: Complete magnet ramp-down and full system diagnostics. Always follow manufacturer's safety protocols."
        },
        {
            "question": "How to troubleshoot error code E401 on the ultrasound machine?",
            "response": "Error E401 indicates a probe communication failure. Steps: 1) Power off the device. 2) Disconnect and inspect the probe cable for damage. 3) Clean the connector pins. 4) Reconnect firmly. 5) Power on. If error persists, the probe may need replacement. Contact support with serial number."
        },
        {
            "question": "What is the recommended cleaning procedure for surgical instruments?",
            "response": "Surgical instrument cleaning protocol: 1) Pre-rinse immediately after use with cold water. 2) Use enzymatic detergent solution at 40-45°C. 3) Manual or ultrasonic cleaning for 10-15 minutes. 4) Rinse with distilled water. 5) Dry thoroughly. 6) Inspect for damage. 7) Sterilize using autoclave at 134°C for 3 minutes."
        },
        {
            "question": "How often should the defibrillator batteries be replaced?",
            "response": "Defibrillator battery replacement schedule: 1) Check battery status indicator monthly. 2) Standard batteries: Replace every 4-5 years or after 200 discharges. 3) Always keep a spare battery. 4) After replacement, run full diagnostic test. 5) Document replacement date in maintenance log."
        },
        {
            "question": "What are the steps to perform preventive maintenance on ventilators?",
            "response": "Ventilator preventive maintenance: Daily: Check alarm functions, inspect tubing. Weekly: Clean/replace filters, check oxygen concentration. Monthly: Calibrate pressure sensors, test backup battery. Every 6 months: Replace internal filters, inspect valves. Annual: Complete system overhaul by certified technician."
        },
        {
            "question": "How to resolve low suction pressure in the suction pump?",
            "response": "Low suction pressure troubleshooting: 1) Check for air leaks in tubing connections. 2) Inspect and clean the suction canister. 3) Replace the vacuum filter if clogged. 4) Verify pump motor operation. 5) Check vacuum gauge calibration. 6) If issue persists, inspect the pump diaphragm for wear."
        },
        {
            "question": "What safety checks are required before using the surgical laser?",
            "response": "Pre-operative laser safety checklist: 1) Verify laser is in proper working mode. 2) Check fiber optic integrity. 3) Test emergency stop button. 4) Ensure proper ventilation in OR. 5) Verify all personnel have appropriate eyewear. 6) Confirm fire extinguisher is accessible. 7) Post warning signs on all entry points."
        },
        {
            "question": "How to change the lamp in the operating room light?",
            "response": "OR light lamp replacement: 1) Power off the light circuit. 2) Allow cooling period of 15 minutes. 3) Wear clean gloves. 4) Remove protective cover using tool provided. 5) Carefully extract old lamp, avoid touching new lamp with bare hands. 6) Install new lamp firmly. 7) Replace cover. 8) Test operation and intensity."
        },
        {
            "question": "What is the protocol for sterilizing endoscopes?",
            "response": "Endoscope sterilization protocol: 1) Pre-clean immediately post-procedure. 2) Leak test at correct pressure. 3) Manual cleaning with enzymatic detergent. 4) Flush all channels thoroughly. 5) High-level disinfection using approved solution (Cidex OPA or similar) for minimum 12 minutes. 6) Final rinse with sterile water. 7) Dry with filtered air. 8) Store in proper cabinet."
        },
        {
            "question": "How to reset the CT scanner after a power failure?",
            "response": "CT scanner power failure recovery: 1) Ensure stable power supply before restart. 2) Wait 5 minutes after power restoration. 3) Power on in sequence: console, gantry, then system. 4) Run system initialization diagnostics. 5) Perform phantom scan to verify image quality. 6) Check all safety interlocks. 7) If errors persist, contact technical support."
        },
        {
            "question": "What are the indicators that the autoclave needs servicing?",
            "response": "Autoclave service indicators: 1) Temperature or pressure doesn't reach set points. 2) Longer than normal cycle times. 3) Door seal leakage. 4) Unusual noises during operation. 5) Failed Bowie-Dick test. 6) Chamber not drying properly. 7) Error codes on display. Schedule service immediately if any indicator is present."
        }
    ]
    
    queries = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i, query_data in enumerate(queries_data):
        # Randomly assign to users
        user = random.choice(users)
        
        # Create timestamps spread over the last 30 days
        created_at = base_date + timedelta(days=random.randint(0, 30), 
                                          hours=random.randint(0, 23))
        
        query = Query(
            user_id=user.id,
            question=query_data["question"],
            response=query_data["response"],
            created_at=created_at
        )
        db.add(query)
        queries.append(query)
    
    await db.commit()
    
    print(f"✓ Seeded {len(queries)} queries")
    return queries
