# Web App

## Overview

This is a notebook and a web app that simulates a simple Poisson process that models the number of vehicles passing a crossing at the instants of a Poisson process of intensity $\gamma>0$; you need a gap of time length at least S in order to cross.

### Model Presentation

Vehicles pass a crossing at the instants of a Poisson process of intensity $\gamma>0$; you need a gap of time 
length at least S in order to cross.

We introduce $(X_{t})_{t \geqslant 0}$ the jump process such that, for every $t\geqslant 0$, $X_{t}=n$, the number of vehicles.

## Requirements

To use the web app, you need to run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Then you can run the web app with the following command (make sure you are in the same directory as the `Poisson_p.py` file):

```bash
streamlit run Poisson_p.py
```

This should open the web app in your default browser. If it doesn't, you have a link in the terminal that you can copy and paste into your browser.

## TODO List

- [ ] Complexify the model
- [ ] Add a nice visualization of the process (possibly using a real front-end framework like React)





