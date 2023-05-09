import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from methods.rungekutta4 import rk4


def ode_system(t, y):

    # Reaction rates
    k1 = 0.0
    k2 = 0.1
    k3 = 0.1
    k4 = 0.01
    k5 = 0.4

    # Population values
    i = y[1]
    s = y[2]
    es = y[3]
    ei = y[4]
    e = y[5]

    # ODEs
    dpdt = k3 * es
    didt = - (k4 * e * i) + (k5 * ei)
    dsdt = - (k1 * s * e) + (k2 * es)
    desdt = (k1 * e * s) - (es * (k2 + k3))
    deidt = (k4 * e * i) - (k5 * ei)
    dedt = (es * (k2 + k3)) + (k5 * ei) - (k1 * s * e) - (k4 * e * i)

    return np.array([dpdt, didt, dsdt, desdt, deidt, dedt])


def simulate():

    # Time step and ending point
    dt = 0.1
    tfinal = 100
    time = np.arange(0, tfinal + dt, dt)

    # Initial conditions [P, I, S, ES, EI, E]
    y0 = np.array([0, 15, 5, 20, 15, 15])

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

    df = pd.DataFrame(data, columns=['P', 'I', 'S', 'ES', 'EI', 'E'])
    df.insert(0, 'Time', time)
    df.to_csv('inhib_results.csv', float_format='%.5f', sep=',')

    fig, ax = plt.subplots()
    fig.set_size_inches(8, 6)
    ax.plot(time, data[:, 0], label='P', color='green')
    ax.plot(time, data[:, 1], label='I', color='red')
    ax.plot(time, data[:, 2], label='S', color='yellow')
    ax.plot(time, data[:, 3], label='ES', color='blue')
    ax.plot(time, data[:, 4], label='EI', color='purple')
    ax.plot(time, data[:, 5], label='E', color='orange')

    ax.set(xlabel='Time (Days)', ylabel='Population', title='Inhibit Competition Model (RK4)')
    ax.grid()
    fig.savefig('inhib_compt.svg', format='svg')

    plt.legend(['P', 'I', 'S', 'ES', 'EI', 'E'], loc='best')
    plt.show()


def main():
    data, time = simulate()
    exp_and_plot(data, time)


if __name__ == '__main__':
    main()
