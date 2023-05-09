[![Python 3.10.6](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3106/)
[![C++](https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white)](https://devdocs.io/cpp/)

# Computational Modeling

Computational modeling practical exercises, ODEs solvers and methods implementations (Evaluative exercises from Introduction to Computational Modeling Course - DCOMP - UFSJ).

# Requirements

- [Python3](https://python.org) and [pip](https://pip.pypa.io/en/stable/installation/) package manager:

      sudo apt install python3 python3-pip build-essential python3-dev

- [pandas](https://pandas.pydata.org/) library:

      pip install pandas
       
- [numpy](https://numpy.org/) library:

      pip install numpy
      
- [SciPy](https://docs.scipy.org/doc/scipy/) library:

      pip install scipy
       
- [Matplotlib](https://matplotlib.org/) library:
 
      pip install matplotlib
      
- [G++](https://gcc.gnu.org/onlinedocs/gcc-12.2.0/gcc/) compiler:

      sudo apt install build-essential
       
- To install all dependencies:

      ./install_dependencies.sh
      
- [Boost](https://www.boost.org/) library
      
# Compilation

- Genetic Algorithm:

      make

# Execution

You can alter the ODEs solver methods and several parameters (initial population, rates, timestep...) directly in the source code before running. The instructions for simulating each model are as it follows:

- Chemical Reactions Model:

      python3 chemical_reactions.py
     
- Lotka-Volterra Model:

      python3 lotka_volterra.py
      
- Species Competition Model:

      python3 species_competition.py
      
- Inhibiting Competition:

      python3 inhibitng_competition.py
      
## SIRS Model

- Differential Evolution:

      python3 differential_evolution.py
      
- Genetic Algorithm (*):

      make run
      
- Gillespie:

      python3 gillespie.py
      
(*) Running the genetic algorithm requires the [download](https://www.boost.org/users/download/) of Boost library. After downloading, extract it inside _src_ directory and change the path in the _Makefile_.
