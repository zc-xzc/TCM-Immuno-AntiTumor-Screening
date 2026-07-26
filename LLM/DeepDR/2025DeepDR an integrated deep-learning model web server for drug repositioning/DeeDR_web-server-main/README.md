# DeepDR platform
DeepDR: an intergrated deep-learning model web server for drug repositioning

DeepDR server is available at http://drpredictor.com

<img src="https://github.com/stjin-XMU/DeeDR_web-server/blob/main/platform.png" height="50%" width="50%">

# Abstract
Identifying new indications for approved drugs is a complex and time-consuming process that requires extensive knowledge of pharmacology, clinical data, and advanced computational methods. Recently, deep learning (DL) methods have shown their capability for the accurate prediction of drug repositioning. However, implementing DL-based modeling requires in-depth domain knowledge and proficient programming skills. Furthermore, to avoid making unreliable recommendations, it also is crucial to use different computational schemes to identify potential drug candidates for different scenarios. To tackle these challenges, we have developed DeepDR (Deep learning-based Drug Repositioning), the first integrated platform that combines a variety of established DL-based models or disease- and target-specific drug repositioning tasks. These deep learning models have undergone rigorous peer review and have been successfully published in prestigious journals. DeepDR leverages invaluable experience to recommend candidate drugs, which covers more than 15 networks and a comprehensive knowledge graph that includes 5.9 million edges across 107 types of relationships connecting drugs, diseases, proteins/genes, pathways, and expression from six existing databases and a large scientific corpus of 24 million PubMed publications. Extensive evaluation results demonstrate that DeepDR achieves excellent predictive performance with an average AUROC of 0.922 for drug repositioning. In addition, the web server also provides detailed descriptions of the recommended drugs, and visualizes key patterns with interpretability through a knowledge graph. DeepDR is free and open to all users without the requirement of registrationand it aims to provide an easy-to-use, systematic, highly accurate and computationally automated platform for experimental and computational scientists. DeepDR server is available at http://drpredictor.com

# python interface
This repository is prepared for the python interface of this webserver.
Now, it’s just a primary version and still need to develop related functions and interfaces.

# 1. How to run?
## 1.1 Model download
Firstly, you can find the models from "Models", or download models from relevant github repository

The "Disease-Centric DeepDR " service：
[DeepDR](https://github.com/ChengF-Lab/deepDR)
[HeTDR](https://github.com/stjin-XMU/HeTDR)
[DisKGE](https://github.com/ChengF-Lab/CoV-KGE)

The "Target-Centric DeepDR " service：
[DeepDTnet](https://github.com/ChengF-Lab/deepDTnet)
[AOPEDF](https://github.com/ChengF-Lab/AOPEDF)
[TarKGE](https://github.com/ChengF-Lab/CoV-KGE)
[KG-MTL](https://github.com/xzenglab/KG-MTL)

## 1.2 strat train
If you need a specific implementation, we recommend readers to check the relevant git repository for more detailed information.

# 2. ‘Models’ directory
We have collected more six models applied to drug repositioning. They are all in models folder and you can review it.

# 3. ‘Datasets’ directory
Contain the all node information，interaction networks and knowledge graph.




