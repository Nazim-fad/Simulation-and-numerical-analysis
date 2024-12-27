# Birth-Death Process Web App

## Overview

This is a notebook and a web app that simulates a birth-death process, and Computes the theoretical and empirical expected values of the population size at a specified time.

### Model Presentation

The **birth-death process** is a Markov jump process used to model systems with random transitions between states over time. It is widely applied in fields like population dynamics and epidemiology. The model simulates and predicts the behavior of systems where the number of entities (population size, queue length, or infected individuals) changes due to random events. The goal is to estimate the expected state of the system at a future time \( T \).



We consider a birth and death process $(X_t)_{t \in \mathbb{R}^+}$ defined on the state space $\{0, 1, \ldots, N\}$, with the following characteristics:

- **Semigroup**: $(P(t))_{t \in \mathbb{R}}$
- **Birth Rates**: $\lambda_n = (N - n)\lambda$, for $n = 0, 1, \ldots, N$
- **Death Rates**: $\mu_n = n\mu$, for $n = 0, 1, \ldots, N$

## Requirements

To use the web app, you need to run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Then you can run the web app with the following command (make sure you are in the same directory as the `birth_death_process.py` file):

```bash
streamlit run birth_death_process.py
```

This should open the web app in your default browser. If it doesn't, you have a link in the terminal that you can copy and paste into your browser.

## TODO List

- [ ] Non-Homogeneous Rates, in our model the rates are constant, but in real-world applications, the rates can change over time.

- [ ] Spatially Distributed Populations, the location of the agents can affect the rates of birth and death.

- [ ] Continuous State Spaces, in our model, the state space is discrete we take values for the population in the integers from 0 to N.





