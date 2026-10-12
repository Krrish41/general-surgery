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
