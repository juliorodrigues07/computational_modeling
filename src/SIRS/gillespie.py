import matplotlib.pyplot as plt
import numpy as np
import random


def simulate(initials, propensities, stoichiometry, duration):

    times = [0.0]
    counts = [initials]

    while times[-1] < duration:

        state = counts[-1]
        rates = [prop(*state) for prop in propensities]

        if all(r == 0 for r in rates):
            break

        transition = random.choices(stoichiometry, weights=rates)[0]
        next_state = [a + b for a, b in zip(state, transition)]

        dt = random.expovariate(sum(rates))

        times.append(times[-1] + dt)
        counts.append(next_state)

    return times, counts


def main(initials, propensities, stoichiometry):

    fig1 = plt.figure(figsize=(12, 8))
    plt.title('Susceptible (SIRS Model)')
    plt.xlabel('Time')
    plt.ylabel('Population')
    ax1 = fig1.gca()

    fig2 = plt.figure(figsize=(12, 8))
    plt.title('Infected (SIRS Model)')
    plt.xlabel('Time')
    plt.ylabel('Population')
    ax2 = fig2.gca()

    fig3 = plt.figure(figsize=(12, 8))
    plt.title('Recovered (SIRS Model)')
    plt.xlabel('Time')
    plt.ylabel('Population')
    ax3 = fig3.gca()

    nRuns = 5
    k = 0
    colorindex = 0.2

    while k < nRuns:

        t = 15
        t, sir = simulate(initials, propensities, stoichiometry, t)
        S, I, R = zip(*sir)

        if k == 0:
            timing = t
            s_sum = S
            i_sum = I
            r_sum = R
        else:
            s_sum = tuple(map(sum, zip(s_sum, S)))
            i_sum = tuple(map(sum, zip(i_sum, I)))
            r_sum = tuple(map(sum, zip(r_sum, R)))

            if len(t) < len(timing):
                timing = t

        ax1.plot(t, S, color=(colorindex / 4, colorindex, colorindex - 0.2), label="S")
        ax2.plot(t, I, color=(colorindex, colorindex / 4, colorindex - 0.2), label="I")
        ax3.plot(t, R, color=(colorindex - 0.2, colorindex, colorindex / 4), label="R")

        k += 1
        colorindex += 0.2

    s_mean = tuple(map(lambda x: x / nRuns, s_sum))
    i_mean = tuple(map(lambda x: x / nRuns, i_sum))
    r_mean = tuple(map(lambda x: x / nRuns, r_sum))

    s_std = np.std(s_mean)
    i_std = np.std(i_mean)
    r_std = np.std(r_mean)

    ax1.plot(timing, s_mean, color='red', label="S Mean")
    ax2.plot(timing, i_mean, color='red', label="I Mean")
    ax3.plot(timing, r_mean, color='red', label="R Mean")

    ax1.fill_between(timing, s_mean - s_std, s_mean + s_std, color='gray', alpha=0.2)
    ax2.fill_between(timing, i_mean - i_std, i_mean + i_std, color='gray', alpha=0.2)
    ax3.fill_between(timing, r_mean - r_std, r_mean + r_std, color='gray', alpha=0.2)

    s_var = np.var(s_mean)
    i_var = np.var(i_mean)
    r_var = np.var(r_mean)

    print('REPORT:\n')
    print(f'S |\t Mean: {np.mean(s_mean)}\t Variance: {s_var}')
    print(f'I |\t Mean: {np.mean(i_mean)}\t Variance: {i_var}')
    print(f'R |\t Mean: {np.mean(r_mean)}\t Variance: {r_var}')

    plt.show()


if __name__ == '__main__':

    # Populations (Susceptible, Infected, Recovered)
    s = 995
    i = 5
    r = 0
    n = s + i + r

    # Rates (Susceptibility, Transmission, Recovering, Birth, Mortality)
    alpha = 0.03
    beta = 1
    gamma = 0.5
    p = 0.08
    d = 0.02

    # With or without vaccination
    vaccine = 0.4
    v = s * vaccine
    s -= v

    initials = [s, i, r]

    propensities = [
        lambda s, i, r: beta * s * i / n,
        lambda s, i, r: gamma * i,
        lambda s, i, r: p * (s + i + r + v),
        lambda s, i, r: d * i,
        lambda s, i, r: alpha * r
    ]

    stoichiometry = [
        [-1,  1,  0],
        [0, -1,  1],
        [1,  0,  0],
        [0, -1,  0],
        [1,  0, -1],
    ]

    main(initials, propensities, stoichiometry)
