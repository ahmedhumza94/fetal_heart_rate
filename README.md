# fetalheartrate
This project explores the link between fetal heart rate time-series to their origin within the first or second stage of labor using unsupervised and supervised learning.

The project uses the open The CTU-UHB Intrapartum Cardiotocography Database. A detailed description of this dataset can be found here https://physionet.org/physiobank/database/ctu-uhb-ctgdb/.

This project also uses Physionets waveform library to help facilitate importing of this dataset. This library is labeled as wfdb within the environment .yml file. The project uses python 3.6.2.


## Project Instructions

### Instructions

1. Clone the repository and navigate to the downloaded folder.
```
cd fetalheartrate
```
2. Create (and activate) a new environment.

	- __Linux__ 
	conda env create -f requirements/fetalheartrate.yml
	source activate dog-project
	```  
	- __Mac__ 
	```
	conda env create -f requirements/fetalheartrate.yml
	source activate dog-project
	```  
	- __Windows__ 
	```
	conda env create -f requirements/fetalheartrate.yml
	activate dog-project
	```
3. Create an [IPython kernel](http://ipython.readthedocs.io/en/stable/install/kernel_install.html) for the `fetalheartrate` environment.
```
python -m ipykernel install --user --name fetalheartrate --display-name "fetalheartrate"
```
4. Open the notebook.
```
jupyter Fetal_Heart_Rate_Exploration.ipynb
```
