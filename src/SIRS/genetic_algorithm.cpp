#include <stdlib.h>
#include <cstdio>
#include <memory.h>
#include <time.h>
#include <vector>
#include <map>
#include <fstream>
#include <iostream>
#include <limits>
#include <cmath>
#include <boost/numeric/odeint.hpp>

template <typename T>
std::pair<T*, T*> selectIndividuals(T** population, size_t populationSize, float* fitnesses, float upperBound)
{
    std::pair<T*, T*> chosen = std::make_pair(population[rand() % populationSize], population[rand() % populationSize]);
    float probA = static_cast<float>(rand()) / RAND_MAX * upperBound;
    float probB = static_cast<float>(rand()) / RAND_MAX * upperBound;
    size_t i = 0;

    while ((probA > 0 || probB > 0) && i < populationSize)
    {
        if (probA > 0)
        {
            probA -= fitnesses[i];
            if (probA <= 0)
                chosen.first = population[i];
        }
        if (probB > 0)
        {
            probB -= fitnesses[i];
            if (probB <= 0)
                chosen.second = population[i];
        }
        i++;
    }
    return chosen;
}

template <typename T>
std::pair<T*, T*> crossover(std::pair<T*, T*> parents, size_t chromosomeSize, float crossoverRate, float mutationChance, void (*mutate)(T*, size_t))
{
    size_t sizeA = static_cast<size_t>(chromosomeSize * crossoverRate);
    size_t sizeB = chromosomeSize - sizeA;
    T* childA = new T[chromosomeSize];
    T* childB = new T[chromosomeSize];

    memcpy(childA, parents.first, sizeA * sizeof(T));
    memcpy(childB, parents.second, sizeA * sizeof(T));

    memcpy(childA + sizeA, parents.second + sizeA, sizeB * sizeof(T));
    memcpy(childB + sizeA, parents.first + sizeA, sizeB * sizeof(T));

    for (size_t i = 0; i < chromosomeSize; i++)
    {
        if (static_cast<float>(rand()) / RAND_MAX <= mutationChance)
            mutate(childA, i);
        if (static_cast<float>(rand()) / RAND_MAX <= mutationChance)
            mutate(childB, i);
    }

    return std::make_pair(childA, childB);
}

template <typename T>
float* getFitnesses(T** population, size_t populationSize, float (*getFitness)(T*), bool maximization, int *best)
{
    float* fitnesses = new float[populationSize];
    float minimum = 0x3f3f3f3f;

    for (size_t i = 0; i < populationSize; i++)
    {
        if (getFitness != nullptr)
            fitnesses[i] = getFitness(population[i]);
        else
            fitnesses[i] = 0;

        if (fitnesses[i] < minimum)
        {
            minimum = fitnesses[i];
            *best = i;
        }
    }

    if (maximization == false)
    {
        float maxFitness = std::numeric_limits<float>::min();
        for (size_t i = 0; i < populationSize; i++)
        {
            if (fitnesses[i] > maxFitness)
                maxFitness = fitnesses[i];
        }

        for (size_t i = 0; i < populationSize; i++)
            fitnesses[i] = maxFitness - fitnesses[i];
    }

    return fitnesses;
}

template <typename T>
void clear(T** population, size_t populationSize)
{
    for (size_t i = 0; i < populationSize; i++)
        delete population[i];

    delete[] population;
}

template <typename T>
T** geneticAlgorithm(size_t chromosomeSize, size_t populationSize, size_t maxNumGenerations, float crossoverRate, float mutationChance,
                     T** (*generateRandomPopulation)(size_t, size_t), float (*getFitness)(T*), void (*mutate)(T*, size_t), bool maximization)
{
    T** population = generateRandomPopulation(chromosomeSize, populationSize);
    int besti;

    for (size_t i = 0; i < maxNumGenerations; i++)
    {
        float* fitnesses = getFitnesses(population, populationSize, getFitness, maximization, &besti);

        float upperBound = 0;
        for (size_t i = 0; i < populationSize; i++)
            upperBound += fitnesses[i];

        T** newPopulation = new T*[populationSize];
        for (size_t j = 0; j < populationSize; j++)
        {
            std::pair<T*, T*> parents = selectIndividuals(population, populationSize, fitnesses, upperBound);
            std::pair<T*, T*> children = crossover(parents, chromosomeSize, crossoverRate, mutationChance, mutate);
            newPopulation[j] = children.first;

            j++;
            newPopulation[j] = children.second;
        }
        for (size_t i = 0; i < chromosomeSize; i++)
            newPopulation[0][i] = population[besti][i];

        std::cout << "Pop Error --> " << getFitness(population[besti]) << std::endl;
        delete fitnesses;
        clear(population, populationSize);
        population = newPopulation;
    }

    return population;
}

using namespace boost::numeric::odeint;

runge_kutta_cash_karp54<std::vector<double>> stepper;
double alpha, beta, gaGamma;

void odesystem(const std::vector<double> &u, std::vector<double> &dudt, const double /* t */) {
    double S = u[0];
    double I = u[1];
    double R = u[2];

    dudt[0] = - (beta * S * I) + (alpha * R);
    dudt[1] = (beta * S * I) - (gaGamma * I);
    dudt[2] = (gaGamma * I) - (alpha * R);
}

std::vector<double> advance(double t, double dt, std::vector<double> u) {
    stepper.do_step(odesystem, u, t, dt);
    return u;
}

std::vector<std::vector<double>> readCSV_to_MultidimensionalArray(std::string fname)
{
    std::ifstream f(fname);
    std::string line, val;
    std::vector<std::vector<double>> array;

    while (std::getline(f, line))
    {
        std::vector<double> v;
        std::stringstream s(line);
        while (getline(s, val, ','))
            v.push_back(std::stod(val));
        array.push_back(v);
    }

    return array;
}

float minValue;
float maxValue;
size_t populationSize;
size_t maxNumGenerations;
float mutationChance;
float crossoverRate;

float getRandomValue()
{
    float r = static_cast<float>(rand()) / static_cast<float>(RAND_MAX);
    return r * (maxValue - minValue) + minValue;
}

float** generateRandomPopulation(size_t chromosomeSize, size_t populationSize)
{
    float** population = new float*[populationSize];

    for (size_t i = 0; i < populationSize; i++)
    {
        population[i] = new float[chromosomeSize];
        population[i][0] = getRandomValue();
    }

    return population;
}

void mutate(float* chromosome, size_t index)
{
    chromosome[index] = getRandomValue();
}

float getFitness(float* chromosome)
{
    std::vector<std::vector<double>> data = readCSV_to_MultidimensionalArray("../../data/sir.csv");
    int s = data[0].size();
    std::vector<double> u;
    u.reserve(s);
    u.resize(s);

    int N = 1000;
    u[0] = 995;
    u[1] = 5;
    u[2] = 0;

    alpha = chromosome[0];
    beta = chromosome[1];
    gaGamma = chromosome[2];

    double sError = 0, iError = 0, rError = 0;
    double sSum = 0, iSum = 0, rSum = 0;

    int i = 0;
    double tfinal = 100, dt = 0.01;
    for (double t = 0; t <= tfinal; t += dt)
    {

        if (abs(t - data[i][0]) < 0.01)
        {
            double S = data[i][1];
            double I = data[i][2];
            double R = N - S - I;

            sError += (u[0] - S) * (u[0] - S);
            iError += (u[1] - I) * (u[1] - I);
            sError += (u[2] - R) * (u[2] - R);

            sSum += S * S;
            iSum += I * I;
            rSum += R * R;

            i++;
        }

        if (i >= data.size())
            break;

        u = advance(t, dt, u);
    }

    sError = sqrt(sError / sSum);
    iError = sqrt(iError / iSum);
    rError = sqrt(rError / rSum);

    return sError + iError + rError;
}

int main()
{
    int nParams = 3;
    minValue = 0.01;
    maxValue = 1;
    srand(time(0));

    float **solutions = geneticAlgorithm(nParams, 100, 30, 0.2, 0.5,
                                         &generateRandomPopulation, &getFitness, &mutate, false);

    std::map<float, float *> orderedSolutions;
    for (size_t i = 0; i < populationSize; i++)
        orderedSolutions[getFitness(solutions[i])] = solutions[i];

    int count = 0;
    for (std::map<float, float *>::iterator it = orderedSolutions.begin(); it != orderedSolutions.end(); ++it)
    {
        std::cout << "#" << count++ << " alpha = " << it->second[0] << ", beta = " << it->second[1]
                  << ", gamma = " << it->second[2] << " (fitness = " << it->first << ")" << std::endl;
    }

    // std::cout << "Best solution (min value) = " << orderedSolutions.begin()->second[0] << std::endl;
    // std::cout << "Best solution (max value) = " << orderedSolutions.rbegin()->second[0] << std::endl;

    clear(solutions, populationSize);
    return 0;
}
