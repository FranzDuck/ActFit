import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import scipy.optimize as opt
import os
import json
import matplotlib.widgets as mwdg
import time

#######################################################################
#                             Definitions                             #
#######################################################################
saveFilename = 'FitData.json'
matplotlib.use('TKAgg', warn=False, force=True)

#######################################################################
#                              Functions                              #
#######################################################################

class ActiveFitWindow:

    """Interactive Matplotlib figure with active fit. Requires TKAgg
    backend in matplolib"""

    
    class AxisEvent:
    
        """Defines the event of a specific slider, functor"""
    
        def __init__(self, slider, actFitWin, name):
            """Creates functor which acts on specific slider.
    
            :slider: matplotlib slider object, that triggers this event
            :actFitWin: ActiveFitWindow class that this functor is defined for
            :name: parameter name of the parameter that this slider specifies
    
            """
            self._slider = slider
            self.actFitWin = actFitWin
            self.name = name
    
        def __call__(self, val):
            # If slider changes plot the function again and change values of vars
            self.actFitWin.update_fit_func(self.name, self._slider.val)

    def __init__(self, xs, ys, func):
        """Create the active fit window. """
        # Instantiate the variables
        self.xs, self.ys, self.func = xs, ys, func
        self.fitmin, self.fitmax = np.min(xs), np.max(xs) # Default behavior: fit over all data
        self.sliders = []
        self.accept = False

        # Set the GUI 
        self.varnames = get_parameters_of_function(func)
        self.params = {var: 1 for var in self.varnames} # Create a list of the params
        self.fig, self.ax = plt.subplots()
        self.add_widgets(self.varnames)
        
        # Plot for the first time
        self.ax.plot(xs, ys, 'x')
        self.fitplot = None 
        self.plot_fit_function()
        plt.ion()
        plt.show()

    def fit(self):
        """Active fit method, if this is invoked it loops until fit is accepted
        :returns: TODO

        """
        # Have main loop and let the user change function until fitted.
        popt, pcov = 0,0
        while True:
            if self.accept:
                break
            # This is the fit loop
            plt.pause(.001)
        return self.popt, self.pcov, self.params, self.fitmin, self.fitmax

    def single_fit(self, event):
        """Perform a single fit with given slider values

        :returns: popt, pcov

        """
        # Select range of values (because range can be selected)
        xs = self.xs[np.logical_and(self.xs < self.fitmax, self.xs > self.fitmin)]
        ys = self.ys[np.logical_and(self.xs < self.fitmax, self.xs > self.fitmin)]

        self.popt, self.pcov = opt.curve_fit(self.func, xs, ys, p0=list(self.params.values()))
        for i, name in enumerate(self.params.keys()):
            self.params[name] = self.popt[i]
        self.plot_fit_function()
        plt.draw()
        return self.popt, self.pcov

    def set_accept(self, event):
        self.accept = True
        plt.close()
        del self

    def set_fitrange(self, vmin, vmax):
        self.fitmin = vmin
        self.fitmax = vmax

    def add_widgets(self, varnames):
        """This function adds the widgets expected for each fit parameter 
        to the gui

        :varnames: List of variable names 
        """
        # Create enough space to have all the sliders below the plot
        plt.subplots_adjust(bottom=0.15+len(varnames)*.05) 

        # Create sliders for the variables
        for i, var in enumerate(varnames):
            axnext = plt.axes([0.15, 0.1+i*.05, 0.65, 0.03])
            sl = mwdg.Slider(axnext, var, .1, 30)
            sl.on_changed(self.AxisEvent(sl, self, var))
            self.sliders.append(sl)
        
        # Create fit button with functionality
        ButtonPos = [.8, 0.05, .1, .04]
        axnext = plt.axes(ButtonPos)
        self.fitb = mwdg.Button(axnext, 'Fit')
        self.fitb.on_clicked(self.single_fit)
        
        # Accept button
        ButtonPos = [.6, 0.05, .1, .04]
        axnext = plt.axes(ButtonPos)
        self.accb = mwdg.Button(axnext, 'Accept')
        self.accb.on_clicked(self.set_accept)

        rectprops = dict(facecolor='blue', alpha=.5)
        self.span_sel = mwdg.SpanSelector(self.ax, self.set_fitrange, 'horizontal', rectprops=rectprops)
        
        # Draw GUI
        plt.draw()

    def plot_fit_function(self):
        """Plot the fit function. Uses the member params to get the values 
        to be used for the plot of self.func
        :returns: TODO

        """
        # Remove old plot
        if not self.fitplot == None:
            self.ax.lines.remove(self.fitplot[0])

        # Only plot in fit range:
        xs = self.xs[np.logical_and(self.xs < self.fitmax, self.xs > self.fitmin)]
        ys = self.ys[np.logical_and(self.xs < self.fitmax, self.xs > self.fitmin)]

        # Create new plot with (perhaps) updated values
        yvals = self.func(xs, *self.params.values())
        self.fitplot = self.ax.plot(xs, yvals)
        
        # Set range to include fit function and data
        allys = np.array([*yvals, *self.ys])
        left, right = np.min(allys) - 1, np.max(allys) + 1
        self.ax.set_ylim([left, right])
        plt.draw()

    def update_fit_func(self, nameOfVar, valueOfVar):
        """Update the plot of the fit function for a parameter with name and val

        :nameOfVar: name of the variable to change 
        :valueOfVar: new value for the variable

        """
        self.params[nameOfVar] = valueOfVar
        self.plot_fit_function()


def get_parameters_of_function(func):
    """This returns the parameter names of function of the form f(x, *params)

    :func: TODO
    :returns: TODO

    """
    varnames = func.__code__.co_varnames
    return varnames[1:]

def load_fits(filename=saveFilename):
    """Loads old fit values if existing.

    :filename: Filename of the fit data file you want to load 
    :returns: popt, pcov, names : of the last saved fit with associated
        variable names 
    """
    data = json.load(open(filename, 'r'))
    popts, pcovs = [], []
    for key, (popt, pcov) in data.items():
        popts.append(popt)
        pcovs.append(pcov)
        data[key] = popt
    return np.array(popts), np.array(pcovs), data

def save_fits(params, pcov, filename=saveFilename):
    """This functions saves the fit parameters to the disc.

    :params: dictionary of variable name, and value pairs
    :filename: filename, where data is saved

    """
    for i, (key, val) in enumerate(params.items()):
        params[key] = (val, list(pcov[i]))
    json.dump(params, open(filename, 'w'))

def active_fit(xs, ys, func):
    """Main function for active fit.

    :xs: x values of the data 
    :ys: y values of the data
    :func: function one wants to fit
    :returns: popt, pcov, params, (fitmin, fitmax)

    """
    # Load old fit if existing
    if os.path.exists(saveFilename):
        popt, pcov, params = load_fits(saveFilename)
        # If fit data exists, query new fit
        if input('Do you want to fit new? (no for "no fit", else new) ') == 'no':
            return popt, pcov, params

    # Active fit menu in fit window fw
    fw = ActiveFitWindow(xs, ys, func)
    popt, pcov, params, fitmin, fitmax = fw.fit()

    # Save fit parameters
    save_fits(params, pcov)

    # return fit
    return popt, pcov, params, (fitmin, fitmax)

#######################################################################
#                           Test functions                            #
#######################################################################

def func(xs, m, b, c):
    """Test fit function
    """
    return m*np.sin(b*xs) + c

def main():
    """Function for testing the code in this library
    """
    # Create test data
    xs = np.linspace(0,np.pi*2, 100)
    ys = np.sin(xs)
    ys += np.random.rand(100)*.3
    
    fig, ax = plt.subplots()
    ax.plot(xs, ys, 'x', label='Data')
    plt.ion()
    popt, pcov, _, (xmin, xmax) = active_fit(xs, ys, func)
    
    plt.ioff()
    xs = xs[np.logical_and(xs>xmin, xs<xmax)]
    ax.plot(xs, func(xs, *popt), label='Fit')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
