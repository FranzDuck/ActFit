# ActFit

This project is aimed at providing a graphical user interface for performing fits on scientific data.
Often times getting a fit function to converge on experimental data is quite painful, because inital values have to be picked carefully.
Using the method active_fit() provided by this library is essentially the same as invoking scipy.optimize.cure_fit() but prompts the user to choose - if needed - a graphical fit interface, where changes in the variables are instantly visible in the fit, which allows for better control of the initial values.

## How to use
1. install python 3.7
2. install [pipenv](https://docs.pipenv.org/en/latest/)
3. run `pipenv install` (to build the virtualenv)
4. run `pipenv shell` (to swith into the virtualenv)
5. run `ActFit`