import numpy as np

###################################################################
# Functions
###################################################################

def ensure_negative_pi_to_pi(angle_radians):
    """
    Normalization, ensuring that the output
    angle will be within [-π, π].

    Parameters
    ----------
    angle_radians : float or int
        angle in radians.

    Returns
    -------
    angle_output : float or int
        angle in radians within [-π, π].
    """

    angle_output = (angle_radians + np.pi) % (2 * np.pi) - np.pi

    return angle_output

