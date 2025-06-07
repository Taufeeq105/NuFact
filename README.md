# NuFact

NuFact: Validating Numerical Assertions for Knowledge Graphs
______________________________________________________

NuFact is a framework that incorporates quantity-sensitive features with text-based validation, enabling reasoning over quantitative information from assertions.
________________________________________________________________

We briefly describe here the folders added to the repository.

Demo: It contains all the codes to create the complete pipeline for NuFact and a web service. 

HybridFC_text_approach: Here we reimplemented HYbridFC to adopt with numeric assertions, specifically, evidence retrieval is updated. 

Query_proof_Generation: It contains the method to extract evidence sentences from the Web using Google API.

Experiments: It contains the codes for different machine learning models that are used to create NuFact. It also contains the code for preparing the ablation study. 

models: It contains all saved models that are created using different sets of features as discussed in the paper

Data: It contains the training data, negative data created using different perturbations. 
