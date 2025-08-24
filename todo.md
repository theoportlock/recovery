	Figure 1
		recovery curves, days to recovery, sustained recovery
		Plot the constrainted analysis plot RDA or ccRDA
	update to maaslin3
	Have to wait for humann download as the server is still down
	premature microbiome maturation
	Mixed model for WLZ as per https://www.science.org/doi/epdf/10.1126/scitranslmed.adn2366
	Recovery time
		Multivariable Cox proportional hazard analysis was conducted to assess the association between time to recovery and the type of therapeutic food, controlling for the confounding variables.
		https://bmcpediatr.biomedcentral.com/articles/10.1186/s12887-023-04168-x?utm_source=chatgpt.com
		The confounding variables include socio-demographic variables (age, sex, and residence of the child), the presenting symptoms, comorbid illnesses, immunization status, medications and nutritional supplements. A full examination, including the grade of edema, dehydration status, skin changes, and vital signs (respiratory rate, pulse rate, and temperature) was performed by the data collectors. Stool examination and hematocrit count were checked from the laboratory report in the medical history sheet.
	Figure 2 needs the 2yr data
		Need to sort out surveillance data to remove the days before running
	Make Figure 3
	Fix Figure 4 so it's readable
	Figure 5 needs the proper anthroplot timelines
		with the gamma waves
	newplotbar plotbar - merge
	plotrecover - simplify with polar.py
	simplecorr - consider removing
	Sort out sustainedrecovery.py and timetorecovery.py
	sigsummary
	Stuart Mcnaughton nad vincent ward - EEG and christopher Erb
	multiprediction based on baseline only, all timepoints, and deltas
	other datasets: 04 LEAP mother enromlent info, Eligibility - Language Difficulty or Delay in q8d - also depression - some flaws in this
	SHAP insensitive to model choice, check
	Use pandoc on tables to make pdf

Rerun the Nextflow pipeline with a longer Humann database download - start with download on liggins and transfer
