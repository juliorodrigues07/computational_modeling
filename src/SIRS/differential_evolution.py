from scipy.optimize import differential_evolution
from scipy.integrate import solve_ivp
from warnings import filterwarnings
from math import sqrt
from os import getcwd
from os import chdir
import matplotlib.pyplot as plt
import numpy as np


filterwarnings('ignore')
path = 'data/'


def ode_system(t, u, alpha, beta, gamma):

    s = u[0]
    i = u[1]
    r = u[2]

    dsdt = - (beta * s * i) + (alpha * r)
    didt = (beta * s * i) - (gamma * i)
    drdt = (gamma * i) - (alpha * r)

    return [dsdt, didt, drdt]


def is_reference_time(times, ct):

    for t in times:
        if (abs(ct - t) <= 10 ** (-5)):
            return True

    return False


def solve(x):

    global data, reference_times
    dt = 0.01
    final_t = 50
    times = np.arange(0, final_t + dt, dt)

    n = 1000
    s = n * 0.995
    i = n * 0.005
    r = n - s - i
    u = [s, i, r]

    alpha = x[0]
    beta = x[1]
    gama = x[2]
    params = (alpha, beta, gama)

    def solve_ode(t, y):
        return ode_system(t, y, *params)

    results = solve_ivp(solve_ode, (0, final_t), u, t_eval=times, method='Radau')
    u = results.y[:3, :]

    i, j = 0, 0
    s_error, i_error, r_error = 0, 0, 0
    s_sum, i_sum, r_sum = 0, 0, 0

    for t in times:

        if is_reference_time(reference_times, t):

            s_data = data[i][1]
            i_data = data[i][2]
            r_data = n - s_data - i_data

            s_error += (u[0][j] - s_data) * (u[0][j] - s_data)
            i_error += (u[1][j] - i_data) * (u[1][j] - i_data)
            r_error += (u[2][j] - r_data) * (u[2][j] - r_data)

            s_sum += s_data * s_data
            i_sum += i_data * i_data
            r_sum += r_data * r_data

            i += 1
        j += 1

    s_error = sqrt(s_error / s_sum)
    i_error = sqrt(i_error / i_sum)
    r_error = sqrt(r_error / r_sum)

    return s_error + i_error + r_error


def test_error(x, convergence):

    global error_list
    error_list.append(solve(x))


if __name__ == "__main__":

    chdir('..')
    chdir('..')

    global data, reference_times, error_list
    data = np.loadtxt(f'{getcwd()}/{path}sir.csv', delimiter=',')
    reference_times = data[:, 0]

    error_list = list()
    bounds = [
        (0.01, 1), (0.01, 1), (0.01, 1)
    ]

    solution = differential_evolution(solve, bounds,
                                      strategy='best1bin',
                                      maxiter=30,
                                      popsize=100,
                                      atol=10 ** (-3),
                                      tol=10 ** (-3),
                                      mutation=0.2,
                                      recombination=0.5,
                                      disp=True,
                                      workers=-1,
                                      callback=test_error)

    print(solution.x)
    print(solution.success)

    best = solution.x
    error = solve(best)

    print(f'Error: {error}')

    fig, ax = plt.subplots()
    fig.set_size_inches(12, 8)

    ax.set(xlabel='Time', ylabel='Error', title='Error Evolution')
    ax.plot(range(len(error_list)), error_list)
    ax.grid()
    plt.show()

    # np.savetxt('adjust_solution.txt', solution.x, fmt='%.2f')
    # fig.savefig('error.png', format='png')
