import sqlite3

def create_database():
    conn = sqlite3.connect('../results/m4efad.db')
    c = conn.cursor()

    # Create aa table
    c.execute('''
        CREATE TABLE aa (
            subjectID TEXT,
            timepoint INTEGER,
            Total_FCIS INTEGER,
            PRIMARY KEY (subjectID, timepoint)
        )''')

    # Create anthro table
    c.execute('''
        CREATE TABLE anthro (
            subjectID TEXT,
            timepoint INTEGER,
            Weight REAL,
            Length REAL,
            MUAC REAL,
            HC REAL,
            WLZ_WHZ REAL,
            PRIMARY KEY (subjectID, timepoint)
        )''')

    # Create bayley table
    c.execute('''
        CREATE TABLE bayley (
            subjectID TEXT,
            timepoint INTEGER,
            cognitive_score INTEGER,
            receptive_communication_score INTEGER,
            expressive_communication_score INTEGER,
            fine_motor_score INTEGER,
            gross_motor_score INTEGER,
            PRIMARY KEY (subjectID, timepoint)
        )''')

    # Create fcis table
    c.execute('''
        CREATE TABLE fcis (
            subjectID TEXT,
            timepoint INTEGER,
            Total_FCIS INTEGER,
            PRIMARY KEY (subjectID, timepoint)
        )''')

    # Create fnirs table
    c.execute('''
        CREATE TABLE fnirs (
            subjectID TEXT,
            timepoint INTEGER,
            connection TEXT,
            connectivity REAL,
            PRIMARY KEY (subjectID, timepoint, connection)
        )''')

    # Create genetics table
    c.execute('''
        CREATE TABLE genetics (
            ID TEXT PRIMARY KEY,
            ADHD_PRS REAL,
            BMI_PRS REAL,
            EA_PRS REAL,
            EF_PRS REAL,
            Height_PRS REAL,
            IBD_CD_PRS REAL,
            IBD_UC_PRS REAL,
            Intelligent_PRS REAL,
            NAFLD_PRS REAL
        )''')

    # Create glitter table
    c.execute('''
        CREATE TABLE glitter (
            subjectID TEXT,
            timepoint INTEGER,
            glitter_seconds REAL,
            PRIMARY KEY (subjectID, timepoint)
        )''')

    # Create head table
    c.execute('''
        CREATE TABLE head (
            subjectID TEXT,
            timepoint INTEGER,
            head_circumference_cm REAL,
            ear_to_ear_measurement_top_head_cm REAL,
            ear_to_ear_measurement_front_cm REAL,
            ear_to_ear_measurement_back_cm REAL,
            nasion_to_inion_measurement_cm REAL,
            PRIMARY KEY (subjectID, timepoint)
        )''')

    # Create lipids table
    c.execute('''
        CREATE TABLE lipids (
            subjectID TEXT,
            timepoint INTEGER,
            lipid TEXT,
            abundance REAL,
            PRIMARY KEY (subjectID, timepoint, lipid)
        )''')

    # Create micro table
    c.execute('''
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
            PRIMARY KEY (subjectID, timepoint)
        )''')

    # Create pathwaysstrat table
    c.execute('''
        CREATE TABLE pathwaysstrat (
            sampleID TEXT,
            timepoint INTEGER,
            stratified_pathway TEXT,
            relative_abundance REAL,
            PRIMARY KEY (sampleID, timepoint, stratified_pathway)
        )''')

    # Create pathways table
    c.execute('''
        CREATE TABLE pathways (
            sampleID TEXT,
            timepoint INTEGER,
            pathway TEXT,
            relative_abundance REAL,
            PRIMARY KEY (sampleID, timepoint, pathway)
        )''')

    # Create pci table
    c.execute('''
        CREATE TABLE pci (
            subjectID TEXT,
            timepoint INTEGER,
            NO_TOY_PLAY REAL,
            BOOK_AND_TOY_FREE_PLAY REAL,
            DIVIDED_ATTENTION_TASK REAL,
            SNACK_TIME REAL,
            PRIMARY KEY (subjectID, timepoint)
        )''')

    # Create pots table
    c.execute('''
        CREATE TABLE pots (
            subjectID TEXT,
            timepoint INTEGER,
            Total_stickers_found INTEGER,
            Perseveration_score INTEGER,
            Correction_score INTEGER,
            PRIMARY KEY (subjectID, timepoint)
        )''')

    # Create psd table
    c.execute('''
        CREATE TABLE psd (
            subjectID TEXT,
            timepoint INTEGER,
            measurement TEXT,
            power REAL,
            PRIMARY KEY (subjectID, timepoint, measurement)
        )''')

    # Create pss table
    c.execute('''
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
            PRIMARY KEY (subjectID, timepoint)
        )''')

    # Create quality table
    c.execute('''
        CREATE TABLE quality (
            sampleID TEXT,
            timepoint INTEGER,
            hq_read_depth_million_reads REAL,
            PRIMARY KEY (sampleID, timepoint)
        )''')

    # Create sleep table
    c.execute('''
        CREATE TABLE sleep (
            subjectID TEXT,
            timepoint INTEGER,
            Bedtime_difficulty INTEGER,
            Fall_asleep_time REAL,
            Times_woken_up INTEGER,
            Night_sleep INTEGER,
            Day_sleep REAL,
            Sleep_problematic INTEGER,
            PRIMARY KEY (subjectID, timepoint)
        )''')

    # Create species table
    c.execute('''
        CREATE TABLE species (
            sampleID TEXT,
            timepoint INTEGER,
            species TEXT,
            relative_abundance REAL,
            PRIMARY KEY (sampleID, timepoint, species)
        )''')

    # Create surveillance table
    c.execute('''
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
            PRIMARY KEY (subjectID, timepoint, Day)
        )''')

    # Create vep table
    c.execute('''
        CREATE TABLE vep (
            subjectID TEXT,
            timepoint INTEGER,
            vep_feature TEXT,
            vep_value REAL,
            PRIMARY KEY (subjectID, timepoint, vep_feature)
        )''')

    # Create vitamin table
    c.execute('''
        CREATE TABLE vitamin (
            subjectID TEXT,
            timepoint INTEGER,
            vitamin TEXT,
            abundance REAL,
            PRIMARY KEY (subjectID, timepoint, vitamin)
        )''')

    # Create wolkes table
    c.execute('''
        CREATE TABLE wolkes (
            subjectID TEXT,
            timepoint INTEGER,
            approach REAL,
            geneemotone REAL,
            activity REAL,
            cooperation REAL,
            vocalisation REAL,
            PRIMARY KEY (subjectID, timepoint)
        )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
