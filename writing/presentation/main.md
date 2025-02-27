---
title: "M4EFaD Recovery"
author:
  - Theo Portlock\inst{1}
  - Justin O'Sullivan\inst{1}
institute:
  - \inst{1}UoA
date: 03-04-2024
output:
  beamer_presentation:
    theme: "Madrid"
    colortheme: "dolphin"
    fonttheme: "structurebold"
---

# Introduction
* Recovery

# SAP
* Plot recovery curves
* Use Fisher to look for recovery from baseline characteristics
* Use RF to look for recovery for each dataset
* Use SHAP to look for cross dataset interactions

# Anthropometric recovery from MAM was achieved 44% of children after refeeding
![](../../figures/timerecovery.pdf)

# Recovery is associated with...
![](../../figures/fisher.pdf)

# Recovery is difficult to predict
![](figures/examplebrowser.pdf)
onehot encoding

# An interaction predicts recovery
![](figures/examplebrowser.pdf)
