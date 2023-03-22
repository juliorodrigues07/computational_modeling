import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from methods.rungekutta4 import rk4


def ode_system(t, y):

    # Reaction rates
    k1 = 0.1
    k2 = 0.05

    # Population values
    a = y[0]
    b = y[1]
    c = y[2]

    # ODEs
    dAdt = -k1 * a * b + k2 * c
    dBdt = -k1 * a * b + k2 * c
    dCdt = k1 * a * b - k2 * c
    
    return np.array([dAdt, dBdt, dCdt])


def simulate():

    # Time step and ending point
    dt = 0.01  
    tfinal = 100 
    time = np.arange(0, tfinal + dt, dt) 

    # Initial conditions
    y0 = np.array([2, 1, 0]) 

    yk = y0
    state_history = list()

    # Simulation (time series loop)
    t = 0
    for t in time:
        state_history.append(yk)
        yk = rk4(ode_system, t, yk, dt)

    state_history = np.array(state_history)
    print(f'y evaluated at time t = {t} seconds: {yk[0]}')

    return state_history, time


def exp_and_plot(data, time):

    df = pd.DataFrame(data, columns = ['A', 'B', 'C'])
    df.insert(0, 'Time', time)
    df.to_csv('chemical_results.csv', float_format='%.5f', sep=',') 

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    ax.plot(time, data[:, 0], label='A', color='green')
    ax.plot(time, data[:, 1], label='B', color='red')
    ax.plot(time, data[:, 2], label='C', color='yellow')
    
    ax.set(xlabel='Time (Days)', ylabel='Population', title='Chemical Reactions Model (RK4)')
    ax.grid()
    fig.savefig('chemical.svg', format='svg')

    plt.legend(['A', 'B', 'C'], loc='best')
    plt.show()


def main():

    data, time = simulate()
    exp_and_plot(data, time)


if __name__ == '__main__':
    main()
