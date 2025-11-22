import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

def exp_decay(t, N0, k, c):
    return N0 * np.exp(-k * t) + c

angles = pd.Series([
    72.64421345861292,
    53.928019844366226,
    41.796844252357275,
    24.811486526119843,
    18.338936051615075
])

popt, _ = curve_fit(exp_decay, angles.index, angles, p0=[72.64421345861292, 0.01, 18.338936051615075])
print(popt)

idx_fit = np.linspace(0, 10, 100)
fit = exp_decay(idx_fit, *popt)

plt.scatter(angles.index, angles)
plt.plot(idx_fit, fit)
#plt.scatter(4, 18.338936051615075)

plt.show()