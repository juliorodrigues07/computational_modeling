import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from methods.rungekutta4 import rk4


def ode_system(t, y):

    # Species growth, Predation, Predators' growth and Predator mortality rates
    r1 = 0.2
    r2 = 0.1

    # Species inner competition (intraspecific)
    w11 = 0.02
    w22 = 0.03

    # Species outer competition (interspecific - distinc species)
    w12 = 0.01
    w21 = 0.02

    # Population values
    a = y[0]
    b = y[1]

    # ODEs
    dAdt = r1 * a * (1 - w11 * a - w21 * b)
    dBdt = r2 * b * (1 - w22 * b - w12 * a)
    
    return np.array([dAdt, dBdt])


def simulate():

    # Time step and ending point
    dt = 0.01  
    tfinal = 200
    time = np.arange(0, tfinal + dt, dt) 

    # Initial conditions
    y0 = np.array([10, 10]) 

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

    df = pd.DataFrame(data, columns = ['Species 1', 'Species 2'])
    df.insert(0, 'Time', time)
    df.to_csv('species_results.csv', float_format='%.5f', sep=',') 

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    ax.plot(time, data[:, 0], label='Species 1', color='blue')
    ax.plot(time, data[:, 1], label='Species 2', color='purple')
    
    ax.set(xlabel='Time (Days)', ylabel='Population', title='Species Competition (RK4)')
    ax.grid()
    fig.savefig('species.svg', format='svg')

    plt.legend(['Species 1', 'Species 2'], loc='best')
    plt.show()


def main():

    data, time = simulate()
    exp_and_plot(data, time)


if __name__ == '__main__':
    main()
