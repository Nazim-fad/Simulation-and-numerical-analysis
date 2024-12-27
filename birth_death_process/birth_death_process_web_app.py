import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def simulate_birth_death_process(N, lambd, mu, initial_state, T):
    # Initialize variables
    current_state = initial_state
    current_time = 0.0
    times = [current_time]
    states = [current_state]

    while current_time < T:
        birth_rate = (N - current_state) * lambd
        death_rate = current_state * mu
        total_rate = birth_rate + death_rate

        if total_rate > 0:
            # Time until next event
            time_to_next_event = np.random.exponential(1 / total_rate)
            current_time += time_to_next_event

            if current_time > T:
                break

            # Determine event type
            if np.random.rand() < (birth_rate / total_rate):
                current_state += 1  # Birth
            else:
                current_state -= 1  # Death

            # Append new state
            times.append(current_time)
            states.append(current_state)
        else:
            # Process is stuck
            break

    return pd.DataFrame({'Time': times, 'State': states})

# the theoretical expected value of the number of individuals at time T
def theoretical_expected_value(x, N, lambd, mu, t):
    term1 = x * ((lambd + mu * np.exp(-(lambd + mu) * t)) / (lambd + mu)**N) * (mu + lambd)**(x-1) * (mu + lambd)**(N-x)
    term2 = (N - x) * ((lambd + mu)**(N-x-1)) * ((mu + lambd)**x) * ((lambd - lambd * np.exp(-(lambd + mu) * t)) / (mu + lambd)**N)
    return term1 + term2

# Streamlit interface
st.title("Birth-Death Process Simulation")

# Instructions
st.markdown("""
This app simulates a birth-death process using the parameters you provide.
Adjust the parameters in the sidebar and click **Run Simulation** to see the results.

We consider a birth and death process $(X_t)_{t \in \mathbb{R}^+}$ defined on the state space $\{0, 1, \ldots, N\}$, with the following characteristics:

- **Birth Rates**: $\lambda_n = (N - n)\lambda$, for $n = 0, 1, \ldots, N$
- **Death Rates**: $\mu_n = n\mu$, for $n = 0, 1, \ldots, N$
""")

# Sidebar for parameters
st.sidebar.header("Simulation Parameters")

# Parameter inputs with validation
param1 = st.sidebar.number_input("Maximum Population Size (N)", min_value=1, value=15, step=1,
                                 help="The maximum population size. No births occur when the population reaches this size.")
param2 = st.sidebar.number_input("Birth Rate (λ)", min_value=0.0, value=2.0, step=0.1,
                                 help="Base birth rate (λ).")
param3 = st.sidebar.number_input("Death Rate (μ)", min_value=0.0, value=1.0, step=0.1,
                                 help="Base death rate (μ).")
param4 = st.sidebar.number_input("Initial State", min_value=0, max_value=param1, value=5, step=1,
                                 help="Initial number of individuals in the system.")
param5 = st.sidebar.number_input("Simulation End Time (T)", min_value=0.1, value=100.0, step=1.0,
                                 help="Time at which the simulation will stop.")
param6 = st.sidebar.number_input("Number of Simulations", min_value=1, value=1000, step=100,
                                 help="Number of simulations to run for estimating the expected state.")

# Run simulation when button is clicked
if st.sidebar.button("Run Simulation"):
    st.subheader("Simulation Results")

    # Run simulation
    data = simulate_birth_death_process(param1, param2, param3, param4, param5)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.step(data['Time'], data['State'], where='post', label='Population State')
    ax.set_title('State Transition Over Time')
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of Individuals')
    ax.set_ylim(0, param1 + 1)
    ax.grid(True)
    ax.legend()

    # Display the plot
    st.pyplot(fig)

    # Display summary statistics
    st.markdown("### Summary Statistics")
    st.write(f"**Total Events:** {len(data) - 1}")
    st.write(f"**Final State:** {int(data['State'].iloc[-1])}")

    # Option to download data
    csv = data.to_csv(index=False).encode()
    st.download_button(label="Download Data as CSV", data=csv, file_name='birth_death_simulation.csv', mime='text/csv')

# Run multiple simulations when button is clicked
if st.sidebar.button("Run Multiple Simulations"):
    st.subheader("Multiple Simulations Results")

    # Progress indicator
    progress_text = st.empty()
    progress_text.text("Running simulations...")
    progress_bar = st.progress(0)

    final_states = []
    num_simulations = int(param6)
    for i in range(num_simulations):
        Data = simulate_birth_death_process(param1, param2, param3, param4, param5)
        final_states.append(Data["State"].iloc[-1])

        # Update progress bar
        if (i + 1) % max(1, num_simulations // 100) == 0 or i == num_simulations - 1:
            progress_bar.progress((i + 1) / num_simulations)

    final_states = np.array(final_states)
    empirical_mean = np.mean(final_states)
    empirical_std = np.std(final_states) # Could set ddof=1 for an unbiased estimate of standard deviation
                                        # but we don't really care about that here since we will use the CLT    

    progress_bar.progress(100)
    progress_text.text("Simulations completed!")

    # Theoretical expected value
    theoretical_mean = theoretical_expected_value(param4, param1, param2, param3, param5)

    # We compute the 95% confidence interval for the empirical mean using the CLT
    std_error = empirical_std / np.sqrt(num_simulations)
    CI_lower = empirical_mean - 1.96 * std_error
    CI_upper = empirical_mean + 1.96 * std_error




    # Display results
    st.markdown("### Expected Number of Individuals at Time T")
    st.write(f"The expected value of the state at time T = {param5} starting from state {param4}")
    st.write(f"**Theoretical Value:** {theoretical_mean:.10f}")
    st.write("\n")
    st.write("**Monte Carlo estimator with a 95% asymptotic confidence interval**")
    st.write("CI = [{:.10f}, {:.10f}]".format(CI_lower, CI_upper))
    st.write(f"**Empirical Mean:** {empirical_mean:.10f}")
    st.write(f"**Empirical Standard Deviation:** {empirical_std:.6f}")
    # Add formula for the theoretical expected value with variable explanations
    st.latex(r"""
    \text{The theoretical expected value of the number of individuals at time } T \text{ is given by:}
    """)
    
    st.latex(r"""
    E(X_T) = x \left( \frac{\lambda + \mu e^{-(\lambda + \mu) t}}{(\lambda + \mu)^N} \right) (\mu + \lambda)^{x-1} (\mu + \lambda)^{N-x} + (N - x) \left( (\lambda + \mu)^{N-x-1} \right) (\mu + \lambda)^x \left( \frac{\lambda - \lambda e^{-(\lambda + \mu) t}}{(\mu + \lambda)^N} \right)
    """)

    st.markdown("""
    Where:
    - T: End time of the simulation
    - x: Initial state of the population 
    - N: Maximum population size
    - λ: Birth rate
    - μ: Death rate
    - t: Time at which the expected value is calculated
    """)



    # Plot histogram of final states
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.hist(final_states, bins=20, edgecolor='black', alpha=0.7)
    ax1.axvline(theoretical_mean, color='red', linestyle='--', label='Theoretical Value')
    ax1.axvline(empirical_mean, color='green', linestyle='--', label='Empirical Mean')
    ax1.set_title('Histogram of Final States')
    ax1.set_xlabel('Final State')
    ax1.set_ylabel('Frequency')
    ax1.legend()

    # Display the histogram
    st.pyplot(fig1)

    # Clear progress indicators
    progress_bar.empty()
    progress_text.empty()


























