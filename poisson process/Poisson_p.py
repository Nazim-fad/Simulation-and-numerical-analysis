import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def simulate_crossing(lambda_, S, total_time,arrival_time = 0):
    # Generate vehicle arrival times
    arrivals = []
    while arrival_time < total_time:
        interarrival_time = np.random.exponential(1 / lambda_)
        arrival_time += interarrival_time
        arrivals.append(arrival_time)



    # Determine the gaps
    gaps = np.diff(arrivals) # time \gammaetween each vehicle arrival
    
    # Check for gaps large enough for crossing
    safe_gaps = gaps >= S
    number_of_safe_crossings = np.sum(safe_gaps)
    
    return number_of_safe_crossings, arrivals,  gaps

def first_cross_time(lambda_, S, total_time):

    number_of_safe_crossings, arrivals, gaps = simulate_crossing(lambda_, S, total_time)
    if number_of_safe_crossings > 0:
        crossing_indices = np.where(gaps >= S)[0]
        crossing_times = np.array(arrivals[:-1])[crossing_indices]
        first_crossing_time = crossing_times[0] + S
    return first_crossing_time if number_of_safe_crossings > 0 else None


# the theoretical expected value of the first crossing time
def theoretical_expected_value(lambda_, S):
    return (np.exp(lambda_ * S) - 1 )/ lambda_

# Streamlit interface
st.title("Crossing the Road Safely")

# Instructions
st.markdown("""
This app simulates a simple model of crossing a road.
- Vehicles arrive at a constant rate.
- The pedestrian must wait for a gap of a certain size to cross.
- The pedestrian can cross when the gap is large enough.
- The simulation tracks the number of safe crossings.
""")

# Sidebar for parameters
st.sidebar.header("Simulation Parameters")

# Parameter inputs with validation
param1 = st.sidebar.number_input("vehicles per second" , value=1, step=1, format="%i")
param2 = st.sidebar.number_input("minimum gap required to cross", value=2, step=1, format="%i")
param3 = st.sidebar.number_input("total time", value=60, step=1, format="%i")
param4 = st.sidebar.number_input("number of simulations", value=1000, step=10, format="%i")


# Run simulation when button is clicked
if st.sidebar.button("Run Simulation"):
    st.subheader("Simulation Results")

    # Run simulation
    data = simulate_crossing(param1, param2, param3)
    GAP = pd.DataFrame({"Gap" : data[2]})
    nb_safe_crossings = data[0]

    # Plotting
    fig, ax = plt.subplots()
    ax.hist(GAP, bins=20, color='skyblue', edgecolor='black')
    ax.set_xlabel("Gap Size")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Display simulation results
    st.write(f"Number of safe crossings: {nb_safe_crossings} out of {param3} seconds")
    st.write(f"Average gap size: {GAP['Gap'].mean():.2f} seconds")

if st.sidebar.button("Run Multiple Simulations"):
    st.subheader("Theoretical Results")

    # Run multiple simulations
    first_cross_times = [first_cross_time(param1, param2, param3) for _ in range(param4)]


    # Display theoretical results
    st.write(f"First crossing time: {np.average(first_cross_times)}")
    st.write(f"Theoretical expected value of first crossing time: {theoretical_expected_value(param1, param2)}")
    st.write(f"The relative error: {abs(np.average(first_cross_times) - theoretical_expected_value(param1, param2)) / theoretical_expected_value(param1, param2)}")























