### SOCIOMAP: Mapping sociogenomic inequities in chronic disease risk– case study on a Nigeria cohort


#### Abstract

Chronic disease risk is shaped by complex intersections of sociodemographic, cultural, and lifestyle factors, yet most data-driven risk models do not explicitly characterize how disease burden is structured across these dimensions in an interpretable and equity-aware manner. In settings with high sociocultural heterogeneity, this limitation obscures subgroup-specific risk patterns and constrains translational impact. Here, we introduce SOCIOMAP, an interpretable, end-to-end machine learning framework designed to quantify and explain how chronic disease risk varies across sociodemographic strata in a nationally representative Nigerian cohort of approximately 45,000 individuals. We harmonize ICD-10 diagnoses, lifestyle variables, and sociodemographic features to derive binary disease phenotypes and first map stratified prevalence and multimorbidity patterns. We then assess group-wise heterogeneity across tribe, religion, income, and education using chi-squared association analyses. To move beyond association, we train gradient-boosted tree models for disease risk prediction and apply SHAP to identify transparent, subgroup-aware drivers of risk, highlighting contributions from adiposity, socioeconomic status, cultural affiliation proxies, and diet-related variables. Unsupervised embedding and clustering further reveal latent population subgroups enriched for distinct sociodemographic and lifestyle profiles, consistent with non-uniform risk architectures across the cohort. Finally, we operationalize SOCIOMAP through interactive Streamlit tool to support exploratory analysis, risk scoring, and explanation. Together, these results demonstrate that chronic disease risk in Nigeria is systematically structured by intersecting social and lifestyle dimensions and establish SOCIOMAP as a scalable, interpretable framework for equity-centered precision public health and future integration with polygenic and gene–environment interaction analyses.

#### Introduction

Understanding how genetic susceptibility intersects with social and environmental context is central to advancing equitable healthcare. Over the past decade, large-scale genomic studies have uncovered thousands of loci associated with complex diseases, and polygenic risk scores (PRS) have emerged as a promising tool for individual-level risk stratification [1,2]. However, the clinical and public health utility of these approaches remains uneven. In practice, many genome-informed risk models prioritize genetic effects while treating social, cultural, and environmental factors as secondary adjustments, resulting in limited generalizability and uneven predictive performance across populations [1,2,3,6].

Africa harbours the greatest human genetic diversity globally [3], yet remains profoundly underrepresented in genomic and health data science research [13,14]. Nigeria, the most populous country in Africa, with over 200 million inhabitants and more than 250 ethnolinguistic groups, presents a uniquely informative setting in which to examine how genetic, sociocultural, and environmental factors jointly shape chronic disease risk. At the same time, Nigeria is undergoing a rapid epidemiological transition, with a growing burden of non-communicable diseases (NCDs) such as hypertension, diabetes, and cardiovascular disease [4]. Despite this shift, there is a critical lack of scalable, interpretable analytical frameworks capable of characterizing disease burden in a manner that is population-aware, equity-centered, and actionable for public health decision-making [15,16].

Importantly, health outcomes are not determined by genetic predisposition alone. A substantial body of evidence highlights the role of social determinants, including ethnicity, religion, income, education, dietary practices, and access to healthcare, in influencing disease onset, progression, and outcomes [5,6,46,47]. In multi-ethnic and socioeconomically stratified societies such as Nigeria, these factors are deeply embedded in cultural norms and lived experience, and may mediate, modify, or even dominate biological risk pathways [23-25]. Yet systematic approaches for integrating sociodemographic structure directly into disease risk modeling, particularly in African populations, remain limited, and such variables are often treated as confounders rather than as primary explanatory dimensions [19,27,28].

Here, we present an interpretable, AI-driven framework for the discovery of polygenic-sociodemographic interactions underlying chronic disease risk in Nigeria. Using a nationally representative cohort of approximately 45,000 individuals, we integrate structured phenotypic data, ICD-10-coded diagnoses, lifestyle indicators, and sociodemographic variables into a unified analytical pipeline grounded in principles of explainable artificial intelligence (XAI) and precision public health [15,16,37,38]. Rather than prioritizing predictive performance alone, our framework is explicitly designed to generate transparent, subgroup-aware insights that can inform policy, prevention strategies, and future genomic integration.

Our approach comprises four core components. First, we develop a robust preprocessing and feature engineering pipeline that harmonizes raw clinical and survey data, including the transformation of free-text and coded ICD-10 diagnoses into interpretable binary disease phenotypes [21,22]. Second, we perform comprehensive epidemiologic profiling of disease prevalence and multimorbidity, enabling fine-grained characterization of chronic disease burden across Nigeria’s sociocultural landscape [45,46]. Third, we quantify stratified disease heterogeneity across tribe, religion, income, education, and lifestyle factors using chi-squared association testing [40,41], nonlinear embedding (UMAP) [10,11], and unsupervised clustering (KMeans), revealing latent population subgroups with distinct risk architectures. Fourth, we train supervised gradient-boosted tree models (XGBoost) [8] and apply SHAP-based explanations [9,12] to identify interpretable drivers of disease risk at both the population and subgroup levels, enabling systematic risk auditing and alignment with established epidemiological patterns.

Unlike traditional genomic studies that rely primarily on genotype data, this work focuses on the sociogenomic layer of disease risk, establishing a necessary foundation for the equitable deployment of polygenic models in African settings [19,27]. To facilitate translation, we operationalize the framework through open-source, interactive dashboards built with Dash and Streamlit, enabling real-time risk scoring, subgroup comparison, and explainable model interrogation by researchers, clinicians, and policymakers [30-32].
By embedding local sociocultural context directly into the modeling pipeline, this study contributes to a new generation of equity-centered AI frameworks for health research [16,17,33-35]. More broadly, it provides a scalable blueprint for other Global South contexts facing similar challenges of health disparity, data marginalization, and limited access to interpretable analytic tools (Fig. 1).

#### Discussion

This study establishes an interpretable, equity-centered framework for characterizing chronic disease risk in a highly diverse and historically underrepresented population. By integrating structured phenotypic data with sociodemographic context and explainable machine learning, we demonstrate that chronic disease burden in Nigeria is not uniformly distributed, but instead exhibits pronounced stratification across intersecting social, cultural, and lifestyle dimensions. These findings challenge implicit assumptions in population health modeling that disease risk can be adequately summarized without explicit consideration of local social structure and lived context.

A central insight of this work is that non-genetic factors, such as income, education, religion, and dietary practices, are not merely nuisance covariates or confounders, but primary organizing axes of disease risk. Through stratified prevalence analyses, formal χ² association testing, and SHAP-based attribution, we show that these dimensions consistently shape both observed disease prevalence and model-predicted risk across multiple chronic conditions. In particular, cardiometabolic diseases such as hypertension and type 2 diabetes display strong heterogeneity across tribal and socioeconomic strata, reinforcing evidence that social determinants play a fundamental role in shaping health outcomes [5,6,46,47]. These results underscore the limitations of population-agnostic risk models and highlight the need for population-aware analytical frameworks in precision public health [15,16].

The use of explainable machine learning enables direct inspection of how social and lifestyle features contribute to disease risk at both population and subgroup levels. Rather than treating machine learning models as opaque predictors, SHAP-based explanations reveal interpretable and policy-relevant drivers, including adiposity, cooking oil type, and income tier, that align with established epidemiological mechanisms while also exposing context-specific patterns [9,12,37,38]. Importantly, group-wise aggregation of SHAP values allows identification of features that disproportionately influence predictions within particular social strata, providing a quantitative framework for auditing equity and informing targeted interventions [16,33-35].

Beyond supervised risk prediction, unsupervised embedding and clustering uncover latent population subgroups with distinct risk architectures that are not fully captured by individual sociodemographic variables alone. These data-driven clusters reflect co-occurring lifestyle behaviors, socioeconomic conditions, and disease profiles, offering a complementary lens for understanding health inequities beyond predefined administrative categories. Such subgroup discovery may be especially valuable in settings where formal classifications fail to capture lived experience or where public health interventions must address overlapping and interacting risk domains.

This work deliberately focuses on the sociogenomic layer of disease risk rather than genotype data alone. While polygenic risk scores have shown promise in some contexts, their uneven portability and performance across populations remain a major barrier to equitable clinical translation [1,19,27,28]. By establishing a rigorous and interpretable framework for modeling social and environmental structure, this study lays essential groundwork for future integration of genetic data, gene–environment interaction analyses, and ancestry-aware polygenic models [13,14]. In this sense, sociogenomic context is not ancillary but foundational to equitable genomic medicine.

Several limitations warrant consideration. First, disease phenotypes were derived from ICD-10 codes and self-reported diagnoses, which may introduce misclassification or underdiagnosis, particularly in low-resource settings [21]. Second, the cross-sectional nature of the data limits causal interpretation, and observed associations should be viewed as descriptive rather than mechanistic [22-25]. Third, although the cohort is nationally representative of Nigeria, findings may not generalize to other African countries with distinct sociopolitical and healthcare contexts. Nevertheless, the analytical framework itself is portable and can be readily adapted to other populations facing similar challenges of data sparsity, heterogeneity, and health inequity. In summary, this study demonstrates how interpretable AI can be used to expose latent structure in chronic disease risk across complex social landscapes. By centering equity, transparency, and population specificity, SOCIOMAP provides a scalable blueprint for precision public health in Nigeria and other Global South settings. More broadly, this work illustrates how contextualized AI can move beyond prediction toward explanation, accountability, and action in global health research.

#### References

1. Martin, A. R., Kanai, M., Kamatani, Y., Okada, Y., Neale, B. M. & Daly, M. J. Clinical use of current polygenic risk scores may exacerbate health disparities. Nat. Genet. 51, 584–591 (2019).

2. Knowles, J. W. & Ashley, E. A. Cardiovascular disease: The rise of the genetic risk score. PLoS Med. 15, e1002547 (2018).

3. The 1000 Genomes Project Consortium. A global reference for human genetic variation. Nature 526, 68–74 (2015).

4. World Health Organization. Noncommunicable Diseases Country Profiles 2021: Nigeria (WHO, 2021).

5. Marmot, M. Social determinants of health inequalities. Lancet 365, 1099–1104 (2005).

5. Braveman, P., Cubbin, C., Egerter, S., Williams, D. R. & Pamuk, E. Socioeconomic disparities in health in the United States: What the patterns tell us. Am. J. Public Health 100, S186–S196 (2010).

6. Popejoy, A. B. & Fullerton, S. M. Genomics is failing on diversity. Nature 538, 161–164 (2016).

7. Nature Editorial. How to bring more diversity into polygenic risk scores. Nature 606, 9 (2022).

8. Chen, T. & Guestrin, C. XGBoost: A scalable tree boosting system. In Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining, 785–794 (ACM, 2016).

9. Lundberg, S. M. & Lee, S.-I. A unified approach to interpreting model predictions. Adv. Neural Inf. Process. Syst. 30, 4765–4774 (2017).

10. McInnes, L., Healy, J. & Melville, J. UMAP: Uniform Manifold Approximation and Projection for dimension reduction. J. Open Source Softw. 3, 861 (2018).

11. Becht, E., McInnes, L., Healy, J., Dutertre, C.-A., Kwok, I. W. H., Ng, L. G. & Newell, E. W. Dimensionality reduction for visualizing single-cell data using UMAP. Nat. Biotechnol. 37, 38–44 (2019).

12. Lundberg, S. M., Erion, G., Chen, H. et al. From local explanations to global understanding with explainable AI for trees. Nat. Mach. Intell. 2, 56–67 (2020).

13. H3Africa Consortium. Enabling the genomic revolution in Africa. Science 344, 1346–1348 (2014).

14. Sirugo, G., Williams, S. M. & Tishkoff, S. A. The missing diversity in human genetic studies. Cell 177, 26–31 (2019).

15. Khoury, M. J., Iademarco, M. F. & Riley, W. T. Precision public health for the era of precision medicine. Am. J. Prev. Med. 50, 398–401 (2016).

16. Rajkomar, A., Hardt, M., Howell, M. D., Corrado, G. & Chin, M. H. Ensuring fairness in machine learning to advance health equity. Ann. Intern. Med. 169, 866–872 (2018).

17. Obermeyer, Z., Powers, B., Vogeli, C. & Mullainathan, S. Dissecting racial bias in an algorithm used to manage the health of populations. Science 366, 447–453 (2019).

18. Collins, F. S. & Varmus, H. A. A new initiative on precision medicine. N. Engl. J. Med. 372, 793–795 (2015).

19. Manrai, A. K. et al. Genetic misdiagnoses and the potential for health disparities. N. Engl. J. Med. 375, 655–665 (2016).

20. Popejoy, A. B. et al. Diversity in precision medicine research: a first look at U.S. initiatives. Health Aff. 37, 1749–1757 (2018).

21. Goldstein, B. A., Navar, A. M., Pencina, M. J. & Ioannidis, J. P. A. Opportunities and challenges in developing risk prediction models with electronic health records data. J. Am. Med. Inform. Assoc. 24, 198–208 (2017).

22. Hernán, M. A. & Robins, J. M. Using big data to emulate a target trial when a randomized trial is not available. Am. J. Epidemiol. 183, 758–764 (2016).

23. VanderWeele, T. J. & Robinson, W. R. On the causal interpretation of race in regressions adjusting for confounding and mediating variables. Epidemiology 25, 473–484 (2014).

24. Williamson, E. J., Aitken, Z., Lawrie, J., Dharmage, S. C. & Burgess, J. A. Introduction to causal diagrams for confounder selection. Respirology 19, 303–311 (2014).

25. Richiardi, L., Bellocco, R. & Zugna, D. Mediation analysis in epidemiology: methods, interpretation and bias. Int. J. Epidemiol. 42, 1511–1519 (2013).

26. Khera, A. V. et al. Genetic risk, adherence to a healthy lifestyle, and coronary disease. N. Engl. J. Med. 375, 2349–2358 (2016).

27. Duncan, L. et al. Analysis of polygenic risk score usage and performance in diverse human populations. Nat. Commun. 10, 3328 (2019).

28. Carlson, C. S. et al. Generalization and dilution of association results from European GWAS in non-European populations. PLoS Genet. 9, e1003607 (2013).

29. Tiffin, P. A., Shah, S., Støvring, H. & Chan, K. Machine learning in clinical medicine: a practical guide. BMC Med. 18, 44 (2020).

30. Obermeyer, Z. & Emanuel, E. J. Predicting the future—big data, machine learning, and clinical medicine. N. Engl. J. Med. 375, 1216–1219 (2016).

31. Riley, W. T., Glasgow, R. E., Etheredge, L. & Abernethy, A. P. Rapid, responsive, relevant (R3) research: a call for a rapid learning health research enterprise. Clin. Transl. Sci. 6, 114–119 (2013).

32. Beam, A. L. & Kohane, I. S. Big data and machine learning in health care. JAMA 319, 1317–1318 (2018).

33. Chouldechova, A. & Roth, A. A snapshot of the frontiers of fairness in machine learning. Commun. ACM 63, 82–89 (2020).

34. Barocas, S., Hardt, M. & Narayanan, A. Fairness and Machine Learning. (fairmlbook.org, 2019).

35. Kleinberg, J., Mullainathan, S. & Raghavan, M. Inherent trade-offs in the fair determination of risk scores. Proc. ITCS 2017, 43:1–43:23.

36. Ribeiro, M. T., Singh, S. & Guestrin, C. “Why should I trust you?” Explaining the predictions of any classifier. Proc. KDD 2016, 1135–1144.

37. Molnar, C. Interpretable Machine Learning. (Lulu.com, 2020).

38. Doshi-Velez, F. & Kim, B. Towards a rigorous science of interpretable machine learning. arXiv 1702.08608 (2017).

39. Stuart, E. A. Matching methods for causal inference: a review and a look forward. Stat. Sci. 25, 1–21 (2010).

40. Benjamini, Y. & Hochberg, Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. J. R. Stat. Soc. B 57, 289–300 (1995).

41. Efron, B. Large-scale simultaneous hypothesis testing. J. Am. Stat. Assoc. 99, 96–104 (2004).

42. Gelman, A., Hill, J. & Vehtari, A. Regression and other stories. (Cambridge Univ. Press, 2020).

43. Spiegelhalter, D. J. Probabilistic prediction in patient management and clinical trials. Stat. Med. 5, 421–433 (1986).

44. Steyerberg, E. W. Clinical Prediction Models. (Springer, 2019).

45. Subramanian, S. V., Jones, K., Kaddour, A. & Krieger, N. Revisiting Robinson: the perils of individualistic and ecologic fallacy. Int. J. Epidemiol. 38, 342–360 (2009).

46. Diez Roux, A. V. Investigating neighborhood and area effects on health. Am. J. Public Health 91, 1783–1789 (2001).

47. Glass, T. A. & McAtee, M. J. Behavioral science at the crossroads in public health. Soc. Sci. Med. 62, 1650–1671 (2006).

48. Boulle, A. et al. Data centre profile: the provincial health data centre of the Western Cape Province, South Africa. Int. J. Popul. Data Sci. 4, 1143 (2019).

49. Kahn, R. et al. Precision public health and structural racism in the United States. Lancet Digit. Health 4, e697–e706 (2022).

50. Dowd, J. B. & Hamoudi, A. Is life expectancy really falling for groups of low socioeconomic status? Proc. Natl Acad. Sci. USA 111, 193–198 (2014).


