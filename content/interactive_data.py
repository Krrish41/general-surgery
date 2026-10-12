# -*- coding: utf-8 -*-
"""
Interactive classification presets for Types & Subtypes explorer.
"""

CLASSIFICATION_PRESETS = {
    "chap1": {
        "title": "Interactive Shock Hemodynamic Explorer",
        "types": [
            {
                "name": "Hypovolemic Shock",
                "badge": "Most Common in Trauma",
                "hemodynamics": "CO: Markedly Decreased | SVR: Markedly Increased | CVP: Very Low | Extremities: Cold, clammy",
                "summary": "Caused by internal/external hemorrhage, third spacing (pancreatitis, obstruction), or burns. Baroreceptor reflex induces intense compensatory vasoconstriction to maintain core BP. Primary survey priority is hemorrhage control and balanced crystalloid/blood resuscitation."
            },
            {
                "name": "Cardiogenic Shock",
                "badge": "Pump Failure",
                "hemodynamics": "CO: Severely Decreased | SVR: High | CVP/JVP: Elevated | Extremities: Cold, cyanotic",
                "summary": "Caused by massive acute myocardial infarction, severe arrhythmias, or acute papillary muscle rupture. Unlike hypovolemia, jugular veins are engorged and pulmonary edema is present. Resuscitation requires inotropes (Dobutamine) and revascularization."
            },
            {
                "name": "Septic / Distributive Shock",
                "badge": "Vasodilatory Crisis",
                "hemodynamics": "CO: High initially (Hyperdynamic) | SVR: Extremely Low | CVP: Low/Normal | Extremities: Warm, flushed",
                "summary": "Bacterial endotoxins trigger massive nitric oxide (iNOS) release and cytokine storm (TNF-α, IL-1), causing uncontrolled arteriolar vasodilation and capillary leakage. Requires early source control, broad-spectrum IV antibiotics, and Noradrenaline."
            },
            {
                "name": "Neurogenic Shock",
                "badge": "Loss of Sympathetic Tone",
                "hemodynamics": "CO: Low/Normal | SVR: Very Low | HR: Paradoxical Bradycardia | Extremities: Warm, dry below lesion",
                "summary": "Occurs following acute high cervical or high thoracic spinal cord injury. Loss of sympathetic outflow causes uninhibited parasympathetic vagal tone, producing the classic triad of hypotension, bradycardia, and peripheral vasodilation."
            },
            {
                "name": "Anaphylactic Shock",
                "badge": "Type I Hypersensitivity",
                "hemodynamics": "CO: Low | SVR: Profoundly Low | Airway: Bronchospasm & Stridor",
                "summary": "IgE-mediated mast cell degranulation releasing histamine and leukotrienes. Causes sudden laryngeal edema, severe bronchospasm, urticaria, and cardiovascular collapse. Drug of choice is immediate intramuscular Adrenaline (0.5 mg 1:1,000 IM)."
            }
        ]
    },
    "chap2": {
        "title": "Interactive Blood Transfusion Reactions Explorer",
        "types": [
            {
                "name": "Acute Hemolytic Reaction (AHTR)",
                "badge": "Medical Emergency | ABO Mismatch",
                "hemodynamics": "Pathology: IgM complement lysis | Triad: Flank pain, fever, hemoglobinuria | Risk: Acute renal failure & DIC",
                "summary": "Caused by clerical bedside misidentification transfusing ABO incompatible red cells. Pre-formed IgM antibodies activate the complement cascade, causing massive intravascular hemolysis. Immediate management: stop transfusion, aggressive IV fluids, osmotic diuresis (Mannitol), and send unit back to blood bank."
            },
            {
                "name": "TRALI (Lung Injury)",
                "badge": "Non-Cardiogenic Edema",
                "hemodynamics": "Mechanism: Donor anti-HLA/HNA antibodies activate recipient lung neutrophils | CVP/PCWP: Normal / Low | BP: Hypotensive",
                "summary": "Leading cause of transfusion-related mortality. Donor leukoagglutinating antibodies trigger severe endothelial damage and capillary leak in recipient pulmonary microvasculature within 6 hours. Presents with sudden dyspnea, hypoxemia, bilateral non-cardiogenic infiltrates. Requires lung-protective mechanical ventilation; diuretics are ineffective."
            },
            {
                "name": "TACO (Circulatory Overload)",
                "badge": "Cardiogenic Edema",
                "hemodynamics": "Mechanism: Hydrostatic fluid overload | JVP: Markedly Elevated | CVP/PCWP: High | BP: Hypertensive",
                "summary": "Excessive or overly rapid transfusion of blood products in elderly, cardiac, or chronic renal patients. Elevated hydrostatic capillary pressure forces fluid into alveolar spaces. Responds dramatically to patient sitting upright, high-flow oxygen, and IV loop diuretics (Furosemide 40 mg IV)."
            },
            {
                "name": "Febrile Non-Hemolytic (FNHTR)",
                "badge": "Most Common Reaction",
                "hemodynamics": "Mechanism: Recipient antibodies against donor white cell cytokines | Temp: ≥1°C rise without hemolysis",
                "summary": "Caused by cytokines (IL-1, IL-6, TNF-α) released by donor leukocytes during storage. Presents with fever, chills, and rigors during or shortly after transfusion. Prevented by routine pre-storage leukocyte depletion (leukoreduction) filters."
            },
            {
                "name": "Anaphylactic Reaction",
                "badge": "IgA-Deficient Recipients",
                "hemodynamics": "Mechanism: Anti-IgA antibodies react with donor IgA | Airway: Laryngeal edema & bronchospasm",
                "summary": "Severe Type I hypersensitivity seen in IgA-deficient individuals who have developed anti-IgA antibodies. Can occur after only a few milliliters of blood. Requires immediate cessation, airway protection, and IM Adrenaline (0.5 mg 1:1,000)."
            }
        ]
    },
    "chap3": {
        "title": "Interactive Surgical Infections & Cellulitis Explorer",
        "types": [
            {
                "name": "Cellulitis",
                "badge": "Subcutaneous Tissue | Diffuse Borders",
                "hemodynamics": "Depth: Deep dermis & Subcutaneous fat | Organism: Group A Strep, S. aureus | Border: Ill-defined, spreading",
                "summary": "Acute diffuse non-suppurative inflammatory infection extending along subcutaneous tissue planes. Overlying skin shows dusky erythema, swelling, and classic peau d'orange (orange-peel) appearance due to cutaneous lymphatic blockage. Managed with limb elevation, analgesics, and IV Flucloxacillin or Cefazolin."
            },
            {
                "name": "Erysipelas",
                "badge": "Superficial Dermis | Raised Distinct Margin",
                "hemodynamics": "Depth: Upper dermis & superficial lymphatics | Organism: Streptococcus pyogenes | Border: Raised, sharply demarcated",
                "summary": "Acute superficial cutaneous infection characterized by fiery-red, glossy plaque with a sharply demarcated, raised edge ('milestone sign' or Milian's ear sign). High fever and severe constitutional symptoms occur abruptly. Anatomical fascia stops spread (e.g. stops at lower border of mandible). Drug of choice is high-dose IV Penicillin G."
            },
            {
                "name": "Carbuncle",
                "badge": "Confluent Multi-Follicular Gangrene",
                "hemodynamics": "Site: Nape of neck | Classical Substrate: Uncontrolled Diabetes Mellitus | Sign: Sieve-like discharging cribriform plate",
                "summary": "Extensive infective gangrene of subcutaneous fat and multiple adjacent hair follicles caused by S. aureus in diabetic patients. Thick inelastic neck skin forces pus laterally and upward through multiple hair follicles, creating a sieve-like cribriform pattern. Treated by glycemic control, broad-spectrum IV antibiotics, and surgical debridement via Cruciate Incision."
            },
            {
                "name": "Necrotizing Fasciitis",
                "badge": "Surgical Emergency | Flesh-Eating",
                "hemodynamics": "Depth: Deep fascia & subcutaneous planes | Hallmark: Severe pain out of proportion | Pus: Dishwater fluid",
                "summary": "Fulminant life-threatening bacterial necrosis spreading along deep fascial planes with secondary thrombosis of nutrient vessels. Presents with excruciating pain out of proportion to skin findings, rapidly followed by dusky skin blisters, cutaneous anesthesia, and systemic septic shock. Requires immediate radical emergent surgical debridement down to viable bleeding fascia."
            }
        ]
    },
    "chap7": {
        "title": "Interactive Neck Swellings Anatomical Explorer",
        "types": [
            {
                "name": "Midline: Thyroglossal Cyst",
                "badge": "Moves with Deglutition & Tongue Protrusion",
                "hemodynamics": "Location: Subhyoid Midline | Transillumination: Positive | Treatment: Sistrunk Operation",
                "summary": "Remnant of embryonic thyroglossal duct between foramen cecum and thyroid isthmus. Anchored to tongue base via genioglossus; moves upward on both swallowing and tongue protrusion. Cured only by resecting the central core of the hyoid bone (Sistrunk)."
            },
            {
                "name": "Midline: Ranula & Plunging Ranula",
                "badge": "Bluish Frog Belly",
                "hemodynamics": "Location: Floor of mouth / Submandibular | Transillumination: Brilliantly Positive",
                "summary": "Extravasation cyst of sublingual salivary gland. Bluish translucent swelling in floor of mouth. Plunging variety herniates through the mylohyoid muscle into the neck. Treated by marsupialization or sublingual gland excision."
            },
            {
                "name": "Midline: Sublingual Dermoid",
                "badge": "Pasty Doughy Consistency",
                "hemodynamics": "Location: Midline Floor of Mouth | Fluctuation: Positive | Transillumination: Negative",
                "summary": "Sequestration dermoid cyst occurring along lines of embryonic fusion. Contains desquamated keratin and sebum; feels doughy on palpation. Does not move with swallowing or tongue protrusion."
            },
            {
                "name": "Anterior Triangle: Branchial Cyst",
                "badge": "Upper 1/3 Anterior SCM",
                "hemodynamics": "Location: Beneath upper SCM border | Transillumination: Negative | Cholesterol Crystals",
                "summary": "Remnant of 2nd branchial cleft. Soft cystic mass emerging beneath the anterior border of the upper third of SCM. FNA reveals turbid fluid rich in rectangular notched cholesterol crystals. Treated by complete surgical excision."
            },
            {
                "name": "Anterior Triangle: Carotid Body Tumor",
                "badge": "Fontaine's Sign Positive",
                "hemodynamics": "Location: Carotid bifurcation | Pulsations: Transmitted | Mobility: Horizontal ONLY",
                "summary": "Chemodectoma / paraganglioma of neural crest chemoreceptors at carotid bifurcation. Demonstrates Fontaine's sign: mobile horizontally across the neck, but completely fixed vertically along the carotid axis."
            },
            {
                "name": "Posterior Triangle: Cystic Hygroma",
                "badge": "Brilliantly Transilluminant",
                "hemodynamics": "Location: Lower Posterior Triangle | Fluid: Clear lymph | Age: Infancy / Childhood",
                "summary": "Congenital lymphatic malformation from sequestered jugular lymph sacs. Multilocular, soft, compressible swelling that shines brilliantly like an electric bulb in a dark room. Treated by surgical excision or Bleomycin sclerotherapy."
            }
        ]
    },
    "chap11": {
        "title": "Interactive Facial Trauma Fracture Explorer",
        "types": [
            {
                "name": "Mandible Fractures",
                "badge": "Coleman's Sign",
                "hemodynamics": "Sites: Condyle (30%), Angle (25%), Body (20%), Symphysis (15%)",
                "summary": "Horseshoe biomechanical ring: fractures are frequently bilateral (body + contralateral condyle). Coleman's sign (sublingual hematoma) is pathognomonic. Managed with MMF (arch bars) or rigid internal fixation (titanium miniplates along Champy's lines)."
            },
            {
                "name": "Le Fort I (Floating Palate)",
                "badge": "Low Horizontal Fracture",
                "hemodynamics": "Separates: Tooth-bearing palate from upper maxilla | Motion: Palate moves alone",
                "summary": "Horizontal fracture running through maxillary alveolar process and pterygoid plates above the tooth roots. Grasping and rocking the upper incisors causes movement of the hard palate alone."
            },
            {
                "name": "Le Fort II (Pyramidal Fracture)",
                "badge": "Pyramid Midface",
                "hemodynamics": "Line: Nasal bridge → Orbit floor → Maxillary wall | Deformity: Dish-face",
                "summary": "Pyramidal fracture involving nasal bones, frontal process of maxilla, lacrimal bones, orbital floor, and zygomaticomaxillary buttress. Presents with bilateral periorbital ecchymosis, step deformity at infraorbital margin, and flattening of midface."
            },
            {
                "name": "Le Fort III (Craniofacial Dysjunction)",
                "badge": "CSF Rhinorrhea Risk",
                "hemodynamics": "Line: Frontonasal → Orbit → Zygoma | Involves: Ethmoid cribriform plate",
                "summary": "High transverse fracture completely separating the facial skeleton from the cranial base. Rips the cribriform plate of ethmoid bone, tearing the dura mater and causing CSF rhinorrhea (clear watery brain fluid from nostrils)."
            }
        ]
    },
    "chap15": {
        "title": "Interactive Intracranial Hemorrhage Explorer",
        "types": [
            {
                "name": "Extradural Hematoma (EDH)",
                "badge": "Biconvex / Lentiform CT",
                "hemodynamics": "Artery: Middle Meningeal Artery (MMA) | Hallmarks: Lucid Interval, Hutchinson's Pupil",
                "summary": "Fracture of temporal bone tears the MMA. Blood collects between inner skull table and dura. Classical Lucid Interval (initial concussion → recovery → rapid deterioration). CT shows biconvex hyperdense mass limited by cranial sutures. Emergency burr hole evacuation."
            },
            {
                "name": "Subdural Hematoma (SDH)",
                "badge": "Crescentic CT",
                "hemodynamics": "Vein: Bridging cortical veins | Shape: Concavo-convex crossing sutures",
                "summary": "Tearing of bridging veins traversing subdural space between brain cortex and dural sinuses. More common in elderly and alcoholics with brain atrophy. CT shows crescentic collection crossing suture lines. Managed with craniotomy or burr-hole washout."
            }
        ]
    },
    "chap23": {
        "title": "Interactive Thyroid Malignancy Explorer",
        "types": [
            {
                "name": "Papillary Thyroid Carcinoma (PTC)",
                "badge": "80% of Cases | Lymphatic Spread",
                "hemodynamics": "Histology: Psammoma bodies, Orphan Annie nuclei | 10-Yr Survival: >95%",
                "summary": "Most common thyroid cancer, seen in young females. Spreads via lymphatics to cervical nodes. Histopathology shows Orphan Annie eyes nuclei, nuclear grooving, and calcified psammoma bodies. Managed with total thyroidectomy, neck dissection, and radioactive iodine (RAI)."
            },
            {
                "name": "Follicular Thyroid Carcinoma (FTC)",
                "badge": "15% of Cases | Hematogenous Spread",
                "hemodynamics": "Histology: Capsular & vascular invasion needed | Metastases: Pulsatile bone lesions",
                "summary": "Seen in older patients in iodine-deficient areas. Spreads via bloodstream to bones and lungs. Cannot be diagnosed on FNAC (Bethesda IV requires diagnostic hemithyroidectomy). Total thyroidectomy followed by RAI ablation."
            },
            {
                "name": "Medullary Thyroid Carcinoma (MTC)",
                "badge": "5% of Cases | C-Cell APUD Origin",
                "hemodynamics": "Biomarker: Calcitonin | Stroma: Amyloid with apple-green birefringence",
                "summary": "Arises from neural crest parafollicular C-cells; secretes calcitonin. Associated with MEN 2A and 2B (RET proto-oncogene). Stains with Congo red showing apple-green birefringence. Cells do NOT take up radioactive iodine; requires radical surgery."
            },
            {
                "name": "Anaplastic Thyroid Carcinoma",
                "badge": "1-2% of Cases | Highly Lethal",
                "hemodynamics": "Age: >65 Years | Presentation: Stony hard, fixed, rapid stridor | Survival: 3-6 Months",
                "summary": "Undifferentiated, extremely aggressive cancer in the elderly. Presents as a rock-hard, rapidly enlarging mass strangling the trachea within weeks. Resistant to standard treatment; palliative airway management and chemo-radiation."
            }
        ]
    }
}

SPOTTER_HOTSPOTS = {
    "thyroid_vessels_nerves_hd.png": [
        {"top": 12, "left": 28, "width": 22, "height": 8, "hint": "Nerve at superior pole", "label": "External Branch of Superior Laryngeal Nerve (EBSLN)"},
        {"top": 18, "left": 58, "width": 20, "height": 8, "hint": "Superior Pole Artery", "label": "Superior Thyroid Artery (Ligate close to gland)"},
        {"top": 48, "left": 62, "width": 22, "height": 9, "hint": "Posterolateral fixation", "label": "Ligament of Berry (Adherent to cricoid)"},
        {"top": 62, "left": 16, "width": 24, "height": 9, "hint": "Lower pole artery", "label": "Inferior Thyroid Artery (Ligate far from gland)"},
        {"top": 72, "left": 45, "width": 25, "height": 9, "hint": "Nerve in TE groove", "label": "Recurrent Laryngeal Nerve (RLN)"},
        {"top": 42, "left": 18, "width": 20, "height": 8, "hint": "Dorsal endocrine gland", "label": "Superior Parathyroid Gland"}
    ],
    "thyroglossal_cyst_tract_hd.png": [
        {"top": 10, "left": 35, "width": 30, "height": 9, "hint": "Origin in tongue", "label": "Foramen Cecum (Base of Tongue)"},
        {"top": 28, "left": 32, "width": 36, "height": 10, "hint": "Bone resected in Sistrunk", "label": "Body of Hyoid Bone (Central 1-2 cm Resected)"},
        {"top": 45, "left": 30, "width": 40, "height": 10, "hint": "Membrane traversed", "label": "Thyrohyoid Membrane & Duct Core"},
        {"top": 65, "left": 34, "width": 32, "height": 11, "hint": "Midline cystic mass", "label": "Thyroglossal Cyst (Moves on Tongue Protrusion)"}
    ],
    "cervical_neck_triangles.jpg": [
        {"top": 16, "left": 30, "width": 28, "height": 10, "hint": "Under mandible", "label": "Submandibular (Digastric) Triangle"},
        {"top": 32, "left": 16, "width": 24, "height": 11, "hint": "Vascular sheath area", "label": "Carotid Triangle (Carotid Artery, IJV, Vagus)"},
        {"top": 44, "left": 45, "width": 24, "height": 11, "hint": "Infrahyoid muscle area", "label": "Muscular Triangle"},
        {"top": 42, "left": 68, "width": 24, "height": 12, "hint": "Behind SCM", "label": "Posterior Triangle (Accessory Nerve CN XI)"},
        {"top": 25, "left": 52, "width": 20, "height": 10, "hint": "Dividing muscular strap", "label": "Sternocleidomastoid Muscle (SCM)"}
    ],
    "head_injury_diagram_hd.png": [
        {"top": 20, "left": 12, "width": 35, "height": 12, "hint": "Biconvex bleed", "label": "Epidural Hematoma (EDH - Middle Meningeal Artery)"},
        {"top": 20, "left": 54, "width": 35, "height": 12, "hint": "Crescentic bleed", "label": "Subdural Hematoma (SDH - Bridging Cortical Veins)"},
        {"top": 58, "left": 15, "width": 32, "height": 11, "hint": "Dural border relation", "label": "Limited by Skull Sutures (Periosteal Dura)"},
        {"top": 58, "left": 55, "width": 32, "height": 11, "hint": "Subdural spread", "label": "Crosses Suture Lines Freely"}
    ],
    "mandible_fractures_hd.png": [
        {"top": 18, "left": 18, "width": 26, "height": 11, "hint": "Most common site (~35%)", "label": "Condylar Neck Fracture"},
        {"top": 52, "left": 12, "width": 28, "height": 11, "hint": "Angle & Masseter pull", "label": "Mandibular Angle (Favorable / Unfavorable)"},
        {"top": 68, "left": 42, "width": 28, "height": 11, "hint": "Midline anterior", "label": "Parasymphysis / Symphysis Fracture"},
        {"top": 35, "left": 48, "width": 34, "height": 10, "hint": "Biomechanic fixation", "label": "Champy's Lines of Ideal Osteosynthesis"}
    ],
    "shock_cardiac_circuit_hd.png": [
        {"top": 22, "left": 16, "width": 30, "height": 12, "hint": "Venous return / Preload", "label": "Central Venous Pressure (CVP) / Right Atrial Preload"},
        {"top": 55, "left": 24, "width": 32, "height": 11, "hint": "Ventricular performance", "label": "Left Ventricle Stroke Volume (Frank-Starling)"},
        {"top": 32, "left": 62, "width": 30, "height": 11, "hint": "Arteriolar tone", "label": "Systemic Vascular Resistance (SVR / Afterload)"},
        {"top": 70, "left": 58, "width": 34, "height": 11, "hint": "Nutrient exchange zone", "label": "Capillary Microcirculation & Perfusion"}
    ],
    "hiltons_method_abscess_hd.png": [
        {"top": 15, "left": 28, "width": 44, "height": 12, "hint": "Step 1: Incision placement", "label": "Skin Incision along Langer's Cleavage Lines"},
        {"top": 40, "left": 26, "width": 48, "height": 12, "hint": "Step 2: Instrument entry", "label": "Blunt Sinus Forceps Introduced Closed into Cavity"},
        {"top": 65, "left": 24, "width": 52, "height": 12, "hint": "Step 3: Cavity opening", "label": "Forceps Jaws Opened Horizontally to Drain & Break Loculi"}
    ],
    "mallampati_airway_hd.png": [
        {"top": 25, "left": 6, "width": 20, "height": 15, "hint": "Full visualization", "label": "Mallampati Class I: Soft Palate, Uvula & Pillars visible"},
        {"top": 25, "left": 29, "width": 20, "height": 15, "hint": "Partial visualization", "label": "Mallampati Class II: Soft Palate, Fauces & Uvula visible"},
        {"top": 25, "left": 52, "width": 20, "height": 15, "hint": "Base uvula only", "label": "Mallampati Class III: Soft Palate and Base of Uvula visible"},
        {"top": 25, "left": 75, "width": 20, "height": 15, "hint": "Hard palate only", "label": "Mallampati Class IV: Hard Palate Only (Difficult Airway Risk)"}
    ],
    "scrofula_collar_stud_stages_hd.png": [
        {"top": 12, "left": 24, "width": 52, "height": 12, "hint": "Stage 1", "label": "Stage 1: Lymphadenitis (Firm discrete enlarged nodes)"},
        {"top": 32, "left": 24, "width": 52, "height": 12, "hint": "Stage 2 & 3", "label": "Stage 2 & 3: Periadenitis (Matted) -> Cold Abscess"},
        {"top": 54, "left": 20, "width": 60, "height": 13, "hint": "Stage 4: Classic sign", "label": "Stage 4: Collar-Stud Abscess (Through Deep Cervical Fascia)"},
        {"top": 76, "left": 24, "width": 52, "height": 12, "hint": "Stage 5", "label": "Stage 5: Chronic Discharging Sinus (Undermined Bluish Margins)"}
    ],
    "grafts_flaps_reconstructive_ladder_hd.png": [
        {"top": 18, "left": 15, "width": 34, "height": 14, "hint": "Thin skin graft", "label": "Split-Thickness Skin Graft (STSG: Epidermis + Partial Dermis)"},
        {"top": 18, "left": 52, "width": 34, "height": 14, "hint": "Thick skin graft", "label": "Full-Thickness Skin Graft (FTSG: Epidermis + Complete Dermis)"},
        {"top": 58, "left": 20, "width": 60, "height": 16, "hint": "Surgical hierarchy", "label": "Reconstructive Ladder: Direct Closure -> Graft -> Local Flap -> Regional Flap -> Free Microvascular Flap"}
    ],
    "cellulitis_erysipelas_depth.jpg": [
        {"top": 22, "left": 18, "width": 64, "height": 15, "hint": "Superficial dermis", "label": "Erysipelas: Superficial Dermal Lymphatics (Raised, well-demarcated margin)"},
        {"top": 58, "left": 18, "width": 64, "height": 15, "hint": "Deep subcutaneous plane", "label": "Cellulitis: Subcutaneous Fat & Deep Fascia (Diffuse, ill-defined margin)"}
    ],
    "ssi_cdc_classification_hd.png": [
        {"top": 20, "left": 25, "width": 50, "height": 14, "hint": "Skin & subcutaneous fat", "label": "Superficial Incisional SSI (Skin and subcutaneous tissue within 30 days)"},
        {"top": 48, "left": 25, "width": 50, "height": 14, "hint": "Fascia and muscle", "label": "Deep Incisional SSI (Deep fascia and muscle layers)"},
        {"top": 74, "left": 25, "width": 50, "height": 14, "hint": "Cavity or organ", "label": "Organ / Space SSI (Body cavity or operated organ)"}
    ]
}

COMPARISON_PAIRS = {
    "chap1": [
        {
            "title": "Cardiac Circuit Dynamics & Hemodynamic Pressures",
            "orig_file": "shock_cardiac_circuit.png",
            "orig_label": "Original Lecture Sketch",
            "hd_file": "shock_cardiac_circuit_hd.png",
            "hd_label": "High-Res 300 DPI Medical Schematic"
        },
        {
            "title": "Cellular Hypoxia & Lactic Acid Pathway",
            "orig_file": "shock_cellular_metabolism.png",
            "orig_label": "Original Lecture Sketch",
            "hd_file": "shock_cellular_metabolism_hd.png",
            "hd_label": "High-Res 300 DPI Medical Schematic"
        }
    ],
    "chap7": [
        {
            "title": "Thyroglossal Cyst Tract & Sistrunk Rationale",
            "orig_file": "thyroglossal_cyst_tract.png",
            "orig_label": "Original Lecture Sketch",
            "hd_file": "thyroglossal_cyst_tract_hd.png",
            "hd_label": "High-Res 300 DPI Medical Schematic"
        },
        {
            "title": "Lipoma Pathology: Encapsulated vs Diffuse Adipose",
            "orig_file": "lipoma_types.png",
            "orig_label": "Original Lecture Sketch",
            "hd_file": "lipoma_pathology_hd.png",
            "hd_label": "High-Res 300 DPI Medical Schematic"
        },
        {
            "title": "Comprehensive Diagnostic Comparison of 10 Neck Swellings",
            "orig_file": "neck_swellings_master_table.png",
            "orig_label": "Original Handwritten Table",
            "hd_file": "neck_swellings_master_matrix_hd.png",
            "hd_label": "High-Res 300 DPI Clinical Matrix"
        }
    ],
    "chap11": [
        {
            "title": "Mandible Fractures & Muscle Vectors",
            "orig_file": "mandible_fractures.png",
            "orig_label": "Original Lecture Sketch",
            "hd_file": "mandible_fractures_hd.png",
            "hd_label": "High-Res 300 DPI Medical Schematic"
        },
        {
            "title": "Le Fort Midface Fractures",
            "orig_file": "lefort_1_diagram.png",
            "orig_label": "Original Lecture Sketch",
            "hd_file": "lefort_fractures_hd.png",
            "hd_label": "High-Res 300 DPI Medical Schematic"
        }
    ],
    "chap15": [
        {
            "title": "Epidural (EDH) vs Subdural (SDH) Hematoma",
            "orig_file": "head_injury_diagram.png",
            "orig_label": "Original Lecture Sketch",
            "hd_file": "head_injury_diagram_hd.png",
            "hd_label": "High-Res 300 DPI Medical Schematic"
        }
    ],
    "chap19": [
        {
            "title": "Laser Resonant Cavity & Wavelength Absorption",
            "orig_file": "laser_cavity_diagram.png",
            "orig_label": "Original Lecture Sketch",
            "hd_file": "laser_cavity_diagram_hd.png",
            "hd_label": "High-Res 300 DPI Medical Schematic"
        }
    ],
    "chap23": [
        {
            "title": "Thyroid Vessels & Safe Ligation Rules for RLN / EBSLN",
            "orig_file": "thyroid_vessels_nerves.png",
            "orig_label": "Original Lecture Sketch",
            "hd_file": "thyroid_vessels_nerves_hd.png",
            "hd_label": "High-Res 300 DPI Medical Schematic"
        }
    ]
}

EXAM_RUBRIC_CRITERIA = [
    {"num": 1, "title": "Definition, Classification & Epidemiology", "marks": 1.5, "desc": "Formal clinical definition, subtypes, incidence & peak demographics"},
    {"num": 2, "title": "Surgical Anatomy & Applied Embryology", "marks": 2.0, "desc": "Fascial compartments, landmarks, triangle boundaries & embryonic remnants"},
    {"num": 3, "title": "Etiopathogenesis & Microbiology", "marks": 1.5, "desc": "Cellular injury mechanism, causative organisms, toxins & molecular triggers"},
    {"num": 4, "title": "Clinical Presentation & Named Physical Signs", "marks": 2.0, "desc": "Chronological symptoms, inspection, palpation (temperature, transillumination, movement)"},
    {"num": 5, "title": "Structured Differential Diagnosis Table", "marks": 1.0, "desc": "Structured comparative table contrasting close surgical conditions"},
    {"num": 6, "title": "Diagnostic Workup & Staging Protocols", "marks": 1.5, "desc": "Gold-standard investigations (Biopsy/FNAC, CT/MRI, ultrasound & staging classifications)"},
    {"num": 7, "title": "Resuscitation & Preoperative Optimization Bundle", "marks": 1.0, "desc": "ATLS ABCDE, fluid resuscitation, cross-matching, prophylactic antibiotics & glycemic control"},
    {"num": 8, "title": "Surgical Technique & Dissection Landmarks", "marks": 2.5, "desc": "Position, incision, exposure steps, neurovascular preservation & anatomical closure"},
    {"num": 9, "title": "Complications Management (Immediate, Early, Late)", "marks": 1.0, "desc": "Post-op hemorrhage, airway compromise, wound infection, nerve palsy & definitive remedies"},
    {"num": 10, "title": "Viva Pearls & Must-Draw Schematics", "marks": 1.0, "desc": "Examiner cross-examination points, high-yield numbers & clear labeled diagram outlines"}
]

