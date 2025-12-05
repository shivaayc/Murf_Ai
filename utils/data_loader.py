"""
Utility module for loading and managing medicine data from CSV files
"""

import csv
import os
from pathlib import Path
from typing import Dict, List, Optional, Set
import pandas as pd

class MedicineDataLoader:
    """Loads and manages medicine data from CSV files"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.medicines = {}
        self.interactions = {}
        self.brands = {}
        self._load_data()
    
    def _load_data(self):
        """Load all CSV data files"""
        self._load_medicines()
        self._load_interactions()
        self._load_brands()
    
    def _load_medicines(self):
        """Load medicines from CSV"""
        med_file = self.data_dir / "medicines.csv"
        
        if not med_file.exists():
            print(f"Warning: {med_file} not found. Creating sample data...")
            self._create_sample_medicines()
            return
        
        try:
            df = pd.read_csv(med_file)
            
            for _, row in df.iterrows():
                medicine_name = row['name'].lower().strip()
                
                # Parse uses as list
                uses = []
                if 'uses' in df.columns and pd.notna(row['uses']):
                    uses = [u.strip() for u in str(row['uses']).split(';') if u.strip()]
                
                # Parse side effects as list
                side_effects = []
                if 'side_effects' in df.columns and pd.notna(row['side_effects']):
                    side_effects = [se.strip() for se in str(row['side_effects']).split(';') if se.strip()]
                
                # Parse contraindications as list
                contraindications = []
                if 'contraindications' in df.columns and pd.notna(row['contraindications']):
                    contraindications = [c.strip() for c in str(row['contraindications']).split(';') if c.strip()]
                
                # Parse interactions as list
                interactions = []
                if 'interactions' in df.columns and pd.notna(row['interactions']):
                    interactions = [i.strip() for i in str(row['interactions']).split(';') if i.strip()]
                
                # Parse brand names as list
                brand_names = []
                if 'brand_names' in df.columns and pd.notna(row['brand_names']):
                    brand_names = [b.strip() for b in str(row['brand_names']).split(';') if b.strip()]
                
                self.medicines[medicine_name] = {
                    'name': row['name'],
                    'generic_name': row.get('generic_name', row['name']),
                    'class': row.get('class', 'Unknown'),
                    'uses': uses,
                    'dosage_adults': row.get('dosage_adults', 'Not specified'),
                    'dosage_children': row.get('dosage_children', 'Not specified'),
                    'side_effects': side_effects,
                    'contraindications': contraindications,
                    'interactions': interactions,
                    'pregnancy': row.get('pregnancy', 'Not specified'),
                    'storage': row.get('storage', 'Room temperature'),
                    'brand_names': brand_names,
                    'mechanism': row.get('mechanism', 'Not specified'),
                    'onset': row.get('onset', 'Not specified'),
                    'duration': row.get('duration', 'Not specified')
                }
            
            print(f"✓ Loaded {len(self.medicines)} medicines from CSV")
            
        except Exception as e:
            print(f"Error loading medicines CSV: {e}")
            self._create_sample_medicines()
    
    def _load_interactions(self):
        """Load medicine interactions from CSV"""
        int_file = self.data_dir / "interactions.csv"
        
        if not int_file.exists():
            print(f"Warning: {int_file} not found. Creating sample interactions...")
            self._create_sample_interactions()
            return
        
        try:
            df = pd.read_csv(int_file)
            
            for _, row in df.iterrows():
                med1 = row['medicine1'].lower().strip()
                med2 = row['medicine2'].lower().strip()
                
                # Store in both directions
                key1 = (med1, med2)
                key2 = (med2, med1)
                
                interaction_data = {
                    'severity': row.get('severity', 'Unknown'),
                    'effect': row.get('effect', 'Interaction present'),
                    'recommendation': row.get('recommendation', 'Consult doctor'),
                    'mechanism': row.get('mechanism', 'Not specified')
                }
                
                self.interactions[key1] = interaction_data
                self.interactions[key2] = interaction_data
            
            print(f"✓ Loaded {len(df)} interactions from CSV")
            
        except Exception as e:
            print(f"Error loading interactions CSV: {e}")
            self._create_sample_interactions()
    
    def _load_brands(self):
        """Load brand names from CSV"""
        brand_file = self.data_dir / "brands.csv"
        
        if not brand_file.exists():
            print(f"Warning: {brand_file} not found. Skipping brands.")
            return
        
        try:
            df = pd.read_csv(brand_file)
            
            for _, row in df.iterrows():
                generic = row['generic_name'].lower().strip()
                brand = row['brand_name'].strip()
                
                if generic not in self.brands:
                    self.brands[generic] = []
                
                self.brands[generic].append({
                    'brand_name': brand,
                    'company': row.get('company', 'Unknown'),
                    'form': row.get('form', 'Tablet'),
                    'strength': row.get('strength', ''),
                    'price_range': row.get('price_range', 'Medium')
                })
            
            print(f"✓ Loaded {len(df)} brand entries from CSV")
            
        except Exception as e:
            print(f"Error loading brands CSV: {e}")
    
    def _create_sample_medicines(self):
        """Create sample medicine data if CSV not found"""
        sample_medicines = {
            'paracetamol': {
                'name': 'Paracetamol',
                'generic_name': 'Acetaminophen',
                'class': 'Analgesic/Antipyretic',
                'uses': ['Fever', 'Mild to moderate pain'],
                'dosage_adults': '500-1000mg every 4-6 hours, max 4000mg/day',
                'dosage_children': '10-15mg/kg every 4-6 hours',
                'side_effects': ['Nausea', 'Rash', 'Liver damage (overdose)'],
                'contraindications': ['Severe liver disease'],
                'interactions': ['Alcohol', 'Warfarin'],
                'pregnancy': 'Category B - generally safe',
                'storage': 'Room temperature, away from moisture',
                'brand_names': ['Crocin', 'Calpol', 'Tylenol'],
                'mechanism': 'Inhibits prostaglandin synthesis',
                'onset': '30 minutes',
                'duration': '4-6 hours'
            }
        }
        self.medicines = sample_medicines
        print("⚠ Using sample medicine data (create data/medicines.csv for full database)")
    
    def _create_sample_interactions(self):
        """Create sample interaction data if CSV not found"""
        self.interactions = {
            ('paracetamol', 'alcohol'): {
                'severity': 'High',
                'effect': 'Increased risk of liver damage',
                'recommendation': 'Avoid or limit alcohol consumption',
                'mechanism': 'Induces CYP2E1 leading to toxic metabolite'
            }
        }
        print("⚠ Using sample interaction data (create data/interactions.csv for full database)")
    
    def search_medicine(self, query: str) -> Optional[Dict]:
        """
        Search for medicine by name (case-insensitive, partial match)
        Returns the best matching medicine or None
        """
        query = query.lower().strip()
        
        # 1. Exact match
        if query in self.medicines:
            return self.medicines[query]
        
        # 2. Check in medicine names
        for med_name, med_data in self.medicines.items():
            if query in med_name or med_name in query:
                return med_data
        
        # 3. Check in generic names
        for med_data in self.medicines.values():
            generic_lower = med_data['generic_name'].lower()
            if query in generic_lower:
                return med_data
        
        # 4. Check in brand names
        for med_data in self.medicines.values():
            for brand in med_data.get('brand_names', []):
                if query in brand.lower():
                    return med_data
        
        return None
    
    def search_all_medicines(self, query: str) -> List[Dict]:
        """Search for all medicines matching query"""
        query = query.lower().strip()
        results = []
        
        for med_name, med_data in self.medicines.items():
            # Check name
            if query in med_name:
                results.append(med_data)
                continue
            
            # Check generic name
            if query in med_data['generic_name'].lower():
                results.append(med_data)
                continue
            
            # Check brand names
            for brand in med_data.get('brand_names', []):
                if query in brand.lower():
                    results.append(med_data)
                    break
        
        return results
    
    def check_interaction(self, med1: str, med2: str) -> Optional[Dict]:
        """
        Check interaction between two medicines
        Returns interaction data or None if no interaction found
        """
        med1_lower = med1.lower().strip()
        med2_lower = med2.lower().strip()
        
        # Try direct key
        key = (med1_lower, med2_lower)
        if key in self.interactions:
            return self.interactions[key]
        
        # Try reverse key
        key_rev = (med2_lower, med1_lower)
        if key_rev in self.interactions:
            return self.interactions[key_rev]
        
        return None
    
    def get_brands(self, medicine_name: str) -> List[Dict]:
        """Get brand names for a medicine"""
        med_data = self.search_medicine(medicine_name)
        if not med_data:
            return []
        
        generic_name = med_data['generic_name'].lower()
        return self.brands.get(generic_name, [])
    
    def get_all_medicines(self) -> List[Dict]:
        """Get all medicines in the database"""
        return list(self.medicines.values())
    
    def get_medicine_by_class(self, medicine_class: str) -> List[Dict]:
        """Get all medicines in a specific class"""
        medicine_class = medicine_class.lower()
        return [
            med for med in self.medicines.values()
            if medicine_class in med['class'].lower()
        ]