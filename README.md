# fetal_heart_rate
This project explores the link between fetal heart rate time-series to their origin within the first or second stage of labor using unsupervised and supervised learning.

Thia project uses the open The CTU-UHB Intrapartum Cardiotocography Database. A detailed description of this dataset can be found here https://physionet.org/physiobank/database/ctu-uhb-ctgdb/.

This project also uses Physionet's waveform library to help facilitate importing of this dataset. This library is labeled as wfdb within the environment .yml file. Main project code is written in python 3.6.2.

A detailed project report can be found as a pdf titled Capstone_Report.pdf. 

The Following instructions can be used to run the code used to produce results within the technical report.

## Project Instructions

### Instructions

1. Clone the repository and navigate to the downloaded folder.
```
cd fetalheartrate
```
2. Create (and activate) a new environment.

	- __Linux__ 
	```
	conda env create -f requirements/fetalheartrate.yml
	source activate fetalheartrate
	```  
	- __Mac__ 
	```
	conda env create -f requirements/fetalheartrate.yml
	source activate fetalheartrate
	```  
	- __Windows__ 
	```
	conda env create -f requirements/fetalheartrate.yml
	activate fetalheartrate
	```
3. Create an [IPython kernel](http://ipython.readthedocs.io/en/stable/install/kernel_install.html) for the `fetalheartrate` environment.
```
python -m ipykernel install --user --name fetalheartrate --display-name "fetalheartrate"
```
4. Open the notebook.
```
jupyter Fetal_Heart_Rate_Exploration.ipynb
```
