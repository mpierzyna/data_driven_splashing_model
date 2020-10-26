"""

"""
import sympy as sp
import numpy as np

from models.rg2014 import beta_expr, calc_t_e
from tools.utils import validate_input

# create symbols
U0, R0, rho_l, mu_l, sigma_l, rho_g, mu_g, lambda_g, t_e, beta, f1, f2, f3 = sp.symbols("U0 R0 rho_l mu_l sigma_l rho_g mu_g lambda_g t_e beta f1 f2 f3")
state = [U0, R0, rho_l, mu_l, sigma_l, rho_g, mu_g, lambda_g]

#####
# Implement uncertainty magnification factors for RG splashing model (???)
#####
# Time derivative functions
# update constants
f1_expr = sp.sqrt(3)/7.2 * mu_l + R0 * t_e**2 * U0 * rho_l
f2_expr = sp.sqrt(3)/3.6 * t_e * U0 * mu_l
f3_expr = 2/3.6 * t_e**(3/2) * sigma_l

# Common functions
a1 = f1 * t_e * U0 * beta**2 * sigma_l * (R0 * t_e**(3/2) + 17.4125 * lambda_g)
a2 = 3/8 * sp.sqrt(3) * R0 * t_e * U0 * mu_g
a3 = R0 * sp.sqrt(t_e) * U0**2 * rho_g * (0.0620245 * R0 * t_e**(3/2) + 1.08 * lambda_g)
a4 = -1/4 * beta**2 * sigma_l * (R0 * t_e**(3/2) + 17.4125 * lambda_g)

umf_U0 = (
    a2 * (-f2 - 2*f3) +
    a3 * (f1 * t_e * U0 - f2 - 2*f3) -
    a4 * (2*f1 * t_e * U0 + f2 + 2*f3)
) / a1


umf_R0 = (
    a2 * (2/3 * f1 * t_e * U0 - f2 - f3) +
    a3 * (f1 * t_e * U0 - f2 - f3) -
    a4 * (f2 + f3)
) / a1

umf_rho_l = - (f2 + f3) / a1 * (a2 + a3 + a4)

umf_mu_l = f2 / a1 * (
    a2 + a3 + a4
)

umf_sigma_l = (
    a2 * f3 +
    a3 * f3 +
    a4 * (2 * t_e * U0 * f1 + f3)
) / a1

umf_rho_g = (0.0620245 * R0 * sp.sqrt(t_e) * U0**2 * rho_g) / (beta**2 * sigma_l)

umf_mu_g = 0.5 - umf_rho_g

umf_lambda_g = -(sp.sqrt(3) * R0 * t_e * U0 * mu_g) / (4 * beta**2 * sigma_l * (R0 * t_e**(3/2) + 17.4125 * lambda_g))

# Substitute auxiliary functions f1, f2, f3, and RG's beta equation into UMF equations.
# Convert all UMF equations into array of python usabale functions.
umf_funcs = [
    sp.lambdify(
        state + [t_e],
        umf.subs([
            (f1, f1_expr),
            (f2, f2_expr),
            (f3, f3_expr),
            (beta, beta_expr),
        ]),
        "numpy"
    ) for umf in
    [umf_U0, umf_R0, umf_rho_l, umf_mu_l, umf_sigma_l, umf_rho_g, umf_mu_g, umf_lambda_g ]
]


def calc_umfs(impact_matrix):
    """
    Calculate UMF factors for RG splashing model (???)
    either for single impact vector or for matrix of impact vectors.

    :impact_matrix: numpy.ndarry of shape (8, ) or (n, 8) with drop impact
                    conditions (V0, R0, rho_l, mu_l, sigma_l, rho_g, mu_g, lambda_g)
    """
    # Validate input and check if matrix or vector
    _, is_matrix = validate_input(impact_matrix)

    # Calculate ejection times first
    t_e_result = calc_t_e(impact_matrix)

    if is_matrix:
        # 2D matrix
        impact_matrix = np.c_[impact_matrix, t_e_result]
    else:
        # 1D matrix, i.e. vector
        impact_matrix = np.r_[impact_matrix, t_e_result]

    return np.array([
        umf(*impact_matrix.T)
        for umf in umf_funcs
    ]).T


if __name__ == '__main__':
    """
    Calculate UMFs based on equations from ???.
    Provide drop impact condtions as vector or as matrix containing
    - V0:       Impact velocity in m/s
    - R0:       Drop radius in m
    - rho_l:    Liquid density in kg/m^3
    - mu_l:     Liquid viscosity in Pa s
    - sigma_l:  Liquid surface tension in N/m
    - rho_g:    Gas density in kg/m^3
    - mu_g:     Gas viscosity in Pa s
    - lambda_g: Gas mean free path in m
    """
    x = np.array([10, 2e-3, 1000, 1e-3, 72e-3, 1.225, 1e-5, 72e-9])
    x_matrix = np.array([
        x,
        2*x,
        3*x
    ])

    print(calc_umfs(x_matrix))
    print(calc_umfs(x))
    #t_e = calc_t_e(x_matrix)
    #print(umf_funcs[1](*np.c_[x_matrix, t_e].T))

# References
# - Riboux, Guillaume, and José Manuel Gordillo. "Experiments of drops impacting a smooth solid surface: a model of the critical impact speed for drop splashing." Physical review letters 113.2 (2014): 024507.
# - Riboux, Guillaume, and José Manuel Gordillo. "The diameters and velocities of the droplets ejected after splashing." Journal of Fluid Mechanics 772 (2015): 630-648.
# - ???
