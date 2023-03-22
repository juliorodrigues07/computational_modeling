[![Python 3.10.6](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3106/)

# Computational Modeling

Computational modeling practical exercises, ODEs solvers and methods implementations (Evaluative exercises from Introduction to Computational Modeling Course - DCOMP - UFSJ).

# Requirements

- [pandas](https://pandas.pydata.org/) library:

      pip install pandas
       
- [numpy](https://numpy.org/) library:

      pip install numpy
       
- [Matplotlib](https://matplotlib.org/) library:
 
      pip install matplotlib
       
- To install all dependencies:

      ./install_dependencies.sh

# Execution

You can alter the ODEs solver methods (_euler_ or _runge-kutta_) and several parameters (initial population, rates, timestep...) directly in the source code before running. The instructions for simulating each model are as it follows:

- Chemical Reactions Model:

      python3 chemical_reactions.py
     
- Lotka-Volterra Model:

      python3 lotka_volterra.py
      
- Species Competition Model:

      python3 species_competition.py
