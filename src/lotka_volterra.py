import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from methods.rungekutta4 import rk4


def ode_system(t, y):

    # Preys' growth, Predation, Predators' growth and Predator mortality rates
    r = 0.01
    a = 0.02
    b = 0.02
    m = 0.5

    # Population values
    prey = y[0]
    predator = y[1]

    # ODEs
    dHdt = r * prey - a * prey * predator 
    dPdt = b * predator * prey - m * predator
    
    return np.array([dHdt, dPdt])


def simulate():

    # Time step and ending point
    dt = 0.01  
    tfinal = 100 
    time = np.arange(0, tfinal + dt, dt) 

    # Initial conditions
    y0 = np.array([20, 30]) 

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

    df = pd.DataFrame(data, columns = ['Prey', 'Predator'])
    df.insert(0, 'Time', time)
    df.to_csv('lotka-volterra_results.csv', float_format='%.5f', sep=',') 

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    ax.plot(time, data[:, 0], label='Prey', color='green')
    ax.plot(time, data[:, 1], label='Predator', color='red')
    
    ax.set(xlabel='Time (Days)', ylabel='Population', title='Lotka-Volterra Model (RK4)')
    ax.grid()
    fig.savefig('lotka-volterra.svg', format='svg')

    plt.legend(['Prey', 'Predator'], loc='best')
    plt.show()


def main():

    data, time = simulate()
    exp_and_plot(data, time)


if __name__ == '__main__':
    main()
