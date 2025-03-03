CREATE TABLE meta (
    subjectID TEXT PRIMARY KEY,
    Sex TEXT,
    Ethnicity TEXT,
    Condition TEXT,
    Feed TEXT,
    Recovery TEXT,
    Delivery_Mode TEXT,
    Supplementation TEXT,
    BF REAL,
    PoB TEXT
);

CREATE TABLE aa (
    subjectID TEXT,
    timepoint INTEGER,
    amino_acid INTEGER,
    concentration REAL,
    PRIMARY KEY (subjectID, timepoint, amino_acid),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE anthro (
    subjectID TEXT,
    timepoint INTEGER,
    Weight REAL,
    Length REAL,
    MUAC REAL,
    HC REAL,
    WLZ_WHZ REAL,
    PRIMARY KEY (subjectID, timepoint),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE bayley (
    subjectID TEXT,
    timepoint INTEGER,
    cognitive_score INTEGER,
    receptive_communication_score INTEGER,
    expressive_communication_score INTEGER,
    fine_motor_score INTEGER,
    gross_motor_score INTEGER,
    PRIMARY KEY (subjectID, timepoint),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE fcis (
    subjectID TEXT,
    timepoint INTEGER,
    Total_FCIS INTEGER,
    PRIMARY KEY (subjectID, timepoint),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE fnirs (
    subjectID TEXT,
    timepoint INTEGER,
    connection TEXT,
    connectivity REAL,
    PRIMARY KEY (subjectID, timepoint, connection),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE genetics (
    subjectID TEXT PRIMARY KEY,
    ADHD_PRS REAL,
    BMI_PRS REAL,
    EA_PRS REAL,
    EF_PRS REAL,
    Height_PRS REAL,
    IBD_CD_PRS REAL,
    IBD_UC_PRS REAL,
    Intelligent_PRS REAL,
    NAFLD_PRS REAL,
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE glitter (
    subjectID TEXT,
    timepoint INTEGER,
    glitter_seconds REAL,
    PRIMARY KEY (subjectID, timepoint),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE head (
    subjectID TEXT,
    timepoint INTEGER,
    head_circumference_cm REAL,
    ear_to_ear_measurement_top_head_cm REAL,
    ear_to_ear_measurement_front_cm REAL,
    ear_to_ear_measurement_back_cm REAL,
    nasion_to_inion_measurement_cm REAL,
    PRIMARY KEY (subjectID, timepoint),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE lipids (
    subjectID TEXT,
    timepoint INTEGER,
    lipid TEXT,
    abundance REAL,
    PRIMARY KEY (subjectID, timepoint, lipid),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE micro (
    subjectID TEXT,
    timepoint INTEGER,
    Occurence_Microstates_A REAL,
    Occurence_Microstates_B REAL,
    Occurence_Microstates_C REAL,
    Occurence_Microstates_D REAL,
    Occurence_Microstates_E REAL,
    Occurence_Microstates_F REAL,
    Occurence_Microstates_G REAL,
    Duration_Microstates_A REAL,
    Duration_Microstates_B REAL,
    Duration_Microstates_C REAL,
    Duration_Microstates_D REAL,
    Duration_Microstates_E REAL,
    Duration_Microstates_F REAL,
    Duration_Microstates_G REAL,
    PRIMARY KEY (subjectID, timepoint),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE pathwaysstrat (
    subjectID TEXT,
    timepoint INTEGER,
    stratified_pathway TEXT,
    relative_abundance REAL,
    PRIMARY KEY (subjectID, timepoint, stratified_pathway),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE pathways (
    subjectID TEXT,
    timepoint INTEGER,
    pathway TEXT,
    relative_abundance REAL,
    PRIMARY KEY (subjectID, timepoint, pathway),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE pci (
    subjectID TEXT,
    timepoint INTEGER,
    NO_TOY_PLAY REAL,
    BOOK_AND_TOY_FREE_PLAY REAL,
    DIVIDED_ATTENTION_TASK REAL,
    SNACK_TIME REAL,
    PRIMARY KEY (subjectID, timepoint),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE pots (
    subjectID TEXT,
    timepoint INTEGER,
    Total_stickers_found INTEGER,
    Perseveration_score INTEGER,
    Correction_score INTEGER,
    PRIMARY KEY (subjectID, timepoint),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE psd (
    subjectID TEXT,
    timepoint INTEGER,
    measurement TEXT,
    power REAL,
    PRIMARY KEY (subjectID, timepoint, measurement),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE pss (
    subjectID TEXT,
    timepoint INTEGER,
    Unexpectedly_upset INTEGER,
    Lack_control INTEGER,
    Anxious_or_stressed INTEGER,
    Confident_handling_problems INTEGER,
    Everything_going_well INTEGER,
    Struggling_to_cope INTEGER,
    Handling_upsets INTEGER,
    Handling_everything_successfully INTEGER,
    Angry_at_setbacks INTEGER,
    Overwhelmed_by_problems INTEGER,
    PRIMARY KEY (subjectID, timepoint),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE quality (
    subjectID TEXT,
    timepoint INTEGER,
    hq_read_depth_million_reads REAL,
    PRIMARY KEY (subjectID, timepoint),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE sleep (
    subjectID TEXT,
    timepoint INTEGER,
    Bedtime_difficulty INTEGER,
    Fall_asleep_time REAL,
    Times_woken_up INTEGER,
    Night_sleep INTEGER,
    Day_sleep REAL,
    Sleep_problematic INTEGER,
    PRIMARY KEY (subjectID, timepoint),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE species (
    subjectID TEXT,
    timepoint INTEGER,
    species TEXT,
    relative_abundance REAL,
    PRIMARY KEY (subjectID, timepoint, species),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE surveillance (
    subjectID TEXT,
    timepoint INTEGER,
    Day REAL,
    Feeding1 REAL,
    Feeding2 REAL,
    Capsule REAL,
    BF TEXT,
    Complemt REAL,
    Vomiting REAL,
    DS REAL,
    Temp REAL,
    Cough TEXT,
    Rash TEXT,
    Antibio TEXT,
    ORS TEXT,
    Zinc TEXT,
    Feeding TEXT,
    Fever TEXT,
    PRIMARY KEY (subjectID, timepoint, Day),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE vep (
    subjectID TEXT,
    timepoint INTEGER,
    vep_feature TEXT,
    vep_value REAL,
    PRIMARY KEY (subjectID, timepoint, vep_feature),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE vitamin (
    subjectID TEXT,
    timepoint INTEGER,
    vitamin TEXT,
    abundance REAL,
    PRIMARY KEY (subjectID, timepoint, vitamin),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE wolkes (
    subjectID TEXT,
    timepoint INTEGER,
    wolkes_category TEXT,
    score REAL,
    PRIMARY KEY (subjectID, timepoint, wolkes_category),
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE media_consumption (
    subjectID TEXT PRIMARY KEY,
    Number_of_mobile_phone_users_in_household INTEGER,
    Reads_the_newspaper TEXT,
    Listens_to_or_watches_Radio_or_TV TEXT,
    Uses_social_media TEXT,
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE education (
    subjectID TEXT PRIMARY KEY,
    Fathers_Educational_attainment INTEGER,
    Years_of_fathers_education INTEGER,
    Mothers_Educational_attainment INTEGER,
    Years_of_mothers_education INTEGER,
    Fathers_occupation TEXT,
    Mothers_occupation TEXT,
    Other_fathers_occupation TEXT,
    Family_owns_the_home_they_live_in TEXT,
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE economics (
    subjectID TEXT PRIMARY KEY,
    Household_heads_income REAL,
    Mothers_income REAL,
    Other_members_income REAL,
    Other_sources_income REAL,
    Total_monthly_income REAL,
    Family_expenditure_food_clothes_utilities REAL,
    Other_expenditure_festivals_medical_education_gifts REAL,
    Monthly_total_expenditure REAL,
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE family (
    subjectID TEXT PRIMARY KEY,
    Number_of_living_children INTEGER,
    Birth_order_of_enrolled_child_among_live_births INTEGER,
    Number_of_siblings_under_five_years INTEGER,
    Family_type TEXT,
    Language TEXT,
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE household (
    subjectID TEXT PRIMARY KEY,
    Principal_type_of_flooring TEXT,
    Principal_wall_material TEXT,
    Principal_roofing_material TEXT,
    Cooking_gas TEXT,
    Telephone_mobile TEXT,
    Almeria TEXT,
    Tabletop TEXT,
    Chair TEXT,
    Bench TEXT,
    Watch_or_clock TEXT,
    Cot_or_bed TEXT,
    Working_Radio TEXT,
    Working_TV TEXT,
    Bicycle TEXT,
    Motorcycle TEXT,
    Sewing_machine TEXT,
    Members_in_household INTEGER,
    Number_of_years_lived_in_current_household INTEGER,
    Number_of_rooms_in_current_household INTEGER,
    Number_of_people_usually_sleeping_in_household INTEGER,
    Maid_working_in_household TEXT,
    Household_food_availability TEXT,
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);

CREATE TABLE sanitation (
    subjectID TEXT PRIMARY KEY,
    Agent_used_before_feeding_child TEXT,
    Method_used_before_feeding_child TEXT,
    Source_of_water_used_before_feeding_child TEXT,
    Agent_used_before_eating TEXT,
    Method_used_before_eating TEXT,
    Source_of_water_used_before_eating TEXT,
    Agent_used_after_defecating TEXT,
    Method_used_after_defecating TEXT,
    Source_of_water_used_after_defecating TEXT,
    Agent_used_before_cleaning_childs_dishes TEXT,
    Method_used_before_cleaning_childs_dishes TEXT,
    Source_of_water_used_before_cleaning_childs_dishes TEXT,
    Agent_used_after_cleaning_childs_anus TEXT,
    Method_used_after_cleaning_childs_anus TEXT,
    Source_of_water_used_after_cleaning_childs_anus TEXT,
    Open_drain_beside_house TEXT,
    Type_of_cooking_fuel TEXT,
    Place_for_cooking_for_household TEXT,
    Frequency_of_nail_cutting_of_mother TEXT,
    Toilet_facility_shared_with_other_households TEXT,
    Water_treatment_method TEXT,
    Principal_type_of_toilet_facility_used_by_household_members TEXT,
    Principal_source_of_household_drinking_water TEXT,
    FOREIGN KEY (subjectID) REFERENCES meta(subjectID)
);
