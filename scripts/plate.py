import numpy as np

class Plate(object):
    def __init__(self, x_list, y_list, z_list, fixture_z_list):
        """Base class of a plate

        Args:
            x_list (list of float): list of x coordinates of the plate
            y_list (list of float): list of y coordinates of the plate
            z_list (list of float): list of z values of the plate
            fixture_z_list (list of float): list of z values from the fixture
        """
        self.x_list = x_list
        self.y_list = y_list
        self.z_list = z_list

        self.fixture_z_list = fixture_z_list
    #_init_()

    def get_thickness(self):
        """Calculates and returns the thickness measurements of the plate by
        subtracting the plate's z value from the fixture's z value

        Returns:
            [list of float]: [difference between plate and fixture z value]
        """
        plate_thickness_list = []
        zip_list = zip(self.fixture_z_list, self.z_list)
        for fixture_i, plate_i in zip_list:
            plate_thickness_list.append(plate_i - fixture_i)
        return plate_thickness_list
    # get_thickness()

    def get_avg(self, plate_thickness_list):
        """Calculates the average thickness of the plate

        Args:
            plate_thickness_list (list of float): thickness of the plate at each
            coordinate

        Returns:
            float: the mean thickness of the current plate
        """
        return np.mean(plate_thickness_list)
    # get_avg()

    def get_stdev(self, plate_thickness_list):
        """Calculates the standard deviation of the plate thickness

        Args:
            plate_thickness_list (list of float): thickness of the plate at each
            coordinate

        Returns:
            float: the standard deviation of the plate thickness
        """
        return np.std(plate_thickness_list)
    # get_stdev()
