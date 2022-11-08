# Seattle Housing: EDA

## Introduction
This repository explores the King County Housing Dataset (years 2014 and 2015).
### Exploratory Data Analysis
You can find the EDA in the jupyter notebook **EDA.ipynb**. The dataset can be downloaded from kaggle.com [here](https://www.kaggle.com/datasets/doesnotcompile/nf-kc-house-data). There you can also find more information on the dataset. For the notebook to work, it should be stored in ```./data/kc_house_data.csv``` relative to the notebook.

Note: since the notebook uses plotly for interactive maps, they will not show if you look at the notebook here on github. Instead, fork/clone the repository and compile it again in your IDE of choice.
### Streamlit App
I've also build a simple recommendation tool that filters data according to user input. It uses the [streamlit](https://streamlit.io) framework and can be found in the **app** folder. To run the app, simply execute the following command in your CLI:

```sh
streamlit run 'PATH_TO_APP/frontend.py'
```

The app will show in your internet browser. To stop the app, press <kbd>ctrl</kbd> + <kbd>c</kbd> while in your terminal.

## Requirements

To automatically creat a local python environment and install the requirements, you can run the following code in your CLI after navigating to the folder containing this repository:

```sh
pyenv local 3.9.8
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
