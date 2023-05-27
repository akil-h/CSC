"""CSC108: Fall 2022 -- Assignment 3: Hypertension and Low Income

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Jacqueline Smith and David Liu
"""
from typing import TextIO
import statistics  # Note that this requires Python 3.10

ID = "id"
HT_KEY = "hypertension"
TOTAL = "total"
LOW_INCOME = "low_income"

# Indexes in the inner lists of hypertension data in CityData
# HT is an abbreviation of hypertension, NBH is an abbreviation of neighbourhood
HT_20_44 = 0
NBH_20_44 = 1
HT_45_64 = 2
NBH_45_64 = 3
HT_65_UP = 4
NBH_65_UP = 5

# columns in input files
ID_COL = 0
NBH_NAME_COL = 1
POP_COL = 2
LI_POP_COL = 3

SAMPLE_DATA = {
    "West Humber-Clairville": {
        "id": 1,
        "hypertension": [703, 13291, 3741, 9663, 3959, 5176],
        "total": 33230,
        "low_income": 5950,
    },
    "Mount Olive-Silverstone-Jamestown": {
        "id": 2,
        "hypertension": [789, 12906, 3578, 8815, 2927, 3902],
        "total": 32940,
        "low_income": 9690,
    },
    "Thistletown-Beaumond Heights": {
        "id": 3,
        "hypertension": [220, 3631, 1047, 2829, 1349, 1767],
        "total": 10365,
        "low_income": 2005,
    },
    "Rexdale-Kipling": {
        "id": 4,
        "hypertension": [201, 3669, 1134, 3229, 1393, 1854],
        "total": 10540,
        "low_income": 2140,
    },
    "Elms-Old Rexdale": {
        "id": 5,
        "hypertension": [176, 3353, 1040, 2842, 948, 1322],
        "total": 9460,
        "low_income": 2315,
    },
}


# Task 1: Building the data dictionary


def get_hypertension_data(hypertension: dict, ht_data_file: TextIO) -> None:
    """Modify the original dictionary to include hypertension data.
    If the original hypertension file contains hypertension data,
    this function updates that information.
    """ 
    ht_data_file.readline()  # skip the first line
    
    ht_dict = {}  # Modified dictionary
    
    f = ht_data_file.readlines()  # read all lines in the opened file
    
    ht_data = []
    
    for neighbourhood in f:
        ht_data.append(neighbourhood.strip().split(','))
        
    for neighbourhood in ht_data:
        ht_dict[neighbourhood[NBH_NAME_COL]] = {
            ID: int(neighbourhood[ID_COL]), 
            HT_KEY: [int(neighbourhood[2]), int(neighbourhood[3]), 
                     int(neighbourhood[4]), int(neighbourhood[5]),
                     int(neighbourhood[6]), int(neighbourhood[7])]}

    for neighbourhood in ht_dict:
        if neighbourhood in hypertension:
            hypertension[neighbourhood][HT_KEY] = ht_dict[neighbourhood][HT_KEY]
        else:
            hypertension.update(ht_dict)

            
def get_low_income_data(low_income: dict, li_data_file: TextIO) -> None:
    """Modify the original low_income dictionary to include low income
    data. If the original low_income file contains low income data, this
    function updates that information.
    """
    li_data_file.readline()  # skip the first line
    
    low_income_dict = {} 
    
    f = li_data_file.readlines()
    
    li_list_data = []
    
    for neighbourhood in f:
        li_list_data.append(neighbourhood.strip().split(','))

    for neighbourhood in li_list_data:
        low_income_dict[neighbourhood[NBH_NAME_COL]] = {
            ID: int(neighbourhood[ID_COL]),
            TOTAL: int(neighbourhood[POP_COL]),
            LOW_INCOME: int(neighbourhood[LI_POP_COL])}

    for neighbourhood in low_income_dict:
        if neighbourhood in low_income:
            low_income[neighbourhood][TOTAL] = (low_income_dict[neighbourhood]
                                                [TOTAL])
            low_income[neighbourhood][LOW_INCOME] = (low_income_dict
                                                     [neighbourhood]
                                                     [LOW_INCOME])
        else:
            low_income.update(low_income_dict)


# Task 2: Neighbourhood-level analysis


def get_bigger_neighbourhood(ndata: 'CityData', 
                             nbhd_1: str, nbhd_2: str) -> str:
    """Return nbhd_1 or nbhd_2 depending on which neighbourhood has a
    higher population according to the low income data in ndata. If a
    neighbourhood is not in the CityData, it will be assigned a population
    of 0. If the two neighbourhoods are the same size, the first
    neighbourhood in the list is returned.
    
    Precondition: nbhd_1 != nbhd_2
    
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'Rexdale-Kipling', \
    'Elms-Old Rexdale')
    'Rexdale-Kipling'
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'Imaginary neighbourhood', \
    'Rexdale-Kipling')
    'Rexdale-Kipling'
    """
    # Test to see if neighbourhood_1 returns a key error
    if nbhd_1 in ndata:
        neighbourhood_1 = ndata[nbhd_1][TOTAL]
    else:
        neighbourhood_1 = 0
    # Test to see if neighbourhood_2 returns a key error
    if nbhd_2 in ndata:
        neighbourhood_2 = ndata[nbhd_2][TOTAL]
    else: 
        neighbourhood_2 = 0
    # Return statements
    if neighbourhood_1 > neighbourhood_2:
        return nbhd_1
    return nbhd_2


def get_high_hypertension_rate(ndata: 'CityData',
                               threshold: float) -> list[tuple[str, float]]:
    """Return a list of tuples with all neighbourhoods with a hypertension
    rate above the threshold from ndata. Each returned value will contain
    the neighbourhood name followed by the associated hypertension rate.
    
    Precondition: 0.0 <= threshold <= 1.0

    >>> get_high_hypertension_rate(SAMPLE_DATA, 0.316)
    [('Thistletown-Beaumond Heights', 0.31797739151574084)]
    >>> get_high_hypertension_rate(SAMPLE_DATA, 0.29)
    [('West Humber-Clairville', 0.2987202275151084), ('Thistletown-Beaumond \
Heights', 0.31797739151574084), ('Rexdale-Kipling', 0.3117001828153565)]
    """
    nbhd_ht_list = []  # contains all the final neighbourhoods
    
    # calculate the ratio of each nbhd
    for nbhd in ndata:  # nbhd refers to the str name of each neighbourhood
        values = ndata[nbhd][HT_KEY]
        # total population with hypertension
        ht_pop = []
        for i in range(len(values)):
            if i % 2 == 0:
                ht_pop.append(values[i])
        # total adultpopulation 
        adult_pop = []
        for i in range(len(values)):
            if i % 2 == 1:
                adult_pop.append(values[i])
        # calculation of hypertension rate
        ratio = sum(ht_pop) / sum(adult_pop)

        if ratio >= threshold:
            nbhd_ht_list.append((nbhd, ratio))

    return nbhd_ht_list


def get_li_rate(ndata: 'CityData', neighbourhood: str) -> float:
    """ Return the low income rate pulled of a given neighbourhood from ndata.

    >>> get_li_rate(SAMPLE_DATA, 'West Humber-Clairville')
    0.1790550707192296
    >>> get_li_rate(SAMPLE_DATA, "Mount Olive-Silverstone-Jamestown")
    0.2941712204007286
    """
    return ndata[neighbourhood][LOW_INCOME] / ndata[neighbourhood][TOTAL]


def get_ht_to_low_income_ratios(ndata: 'CityData') -> dict[str, float]:
    """Return a dictionary including the name of the neighbourhood as the key 
    value and each value as the ratio of the hypertension rate to the low income
    rate for that neighbourhood.

    >>> get_ht_to_low_income_ratios(SAMPLE_DATA)
    {'West Humber-Clairville': 1.6683148168616895, 'Mount \
Olive-Silverstone-Jamestown': 0.9676885451091314, 'Thistletown-Beaumond \
Heights': 1.6438083107534431, 'Rexdale-Kipling': 1.5351962275111484, 'Elms-Old \
Rexdale': 1.1763941257986577}
    >>> new_sample_data = {"West Humber-Clairville": {"id": 1, "hypertension":\
 [703, 13291, 3741, 9663, 3959, 5176], "total": 33230, "low_income": 5950,}}
    >>> get_ht_to_low_income_ratios(new_sample_data)
    {'West Humber-Clairville': 1.6683148168616895}
    """
    new_d = {}
    ht_list = get_high_hypertension_rate(ndata, 0)
    
    for neighbourhood in ht_list:
        # Low income rate:
        low_income_rate = ndata[neighbourhood[0]][LOW_INCOME] / (ndata
                                                                 [neighbourhood
                                                                  [0]][TOTAL])
        # Adding the neighbourhood to new_d
        new_d[neighbourhood[0]] = neighbourhood[1] / low_income_rate
        
    return new_d


def calculate_ht_rates_by_age_group(ndata: 'CityData',
                                    neighbourhood: str) -> tuple[float,
                                                                 float, float]:
    """ Return a tuple with values representing hypertension rates for all three
    age groups in the neighbourhood as a percentage. 
    
    Precondition: neighbourhood in ndata.
    
    ht_20_44 represents the hypertension rate in percent for individuals aged \
    20-44.
    ht_45_64 represents the hypertension rate in percent for individuals aged \
    45-64.
    ht_65_up represents the hypertension rate in percent for individuals above \
    the age of 65 inclusive. 
    
    >>> calculate_ht_rates_by_age_group(SAMPLE_DATA, 'Elms-Old Rexdale')
    (5.24903071875932, 36.593947923997185, 71.70953101361573)
    >>> calculate_ht_rates_by_age_group(SAMPLE_DATA, 'West Humber-Clairville')
    (5.289293506884358, 38.71468488047191, 76.48763523956723)
    """
    ht_20_44 = (ndata[neighbourhood][HT_KEY][0] / (ndata[neighbourhood]
                                                   [HT_KEY][1])) * 100
    ht_45_64 = (ndata[neighbourhood][HT_KEY][2] / (ndata[neighbourhood]
                                                   [HT_KEY][3])) * 100
    ht_65_up = (ndata[neighbourhood][HT_KEY][4] / (ndata[neighbourhood]
                                                   [HT_KEY][5])) * 100
    return (ht_20_44, ht_45_64, ht_65_up)


# This function is provided for use in Tasks 3 and 4. You should not change it.
def get_age_standardized_ht_rate(ndata: 'CityData', name: str) -> float:
    """Return the age standardized hypertension rate from the neighbourhood in
    ndata matching the given name.

    Precondition: name is in ndata.

    >>> get_age_standardized_ht_rate(SAMPLE_DATA, 'Elms-Old Rexdale')
    24.44627521389894
    >>> get_age_standardized_ht_rate(SAMPLE_DATA, 'Rexdale-Kipling')
    24.72562462246556
    """
    rates = calculate_ht_rates_by_age_group(ndata, name)

    # These rates are normalized for only 20+ ages, using the census data
    # that our datasets are based on.
    canada_20_44 = 11_199_830 / 19_735_665  # Number of 20-44 / Number of 20+
    canada_45_64 = 5_365_865 / 19_735_665  # Number of 45-64 / Number of 20+
    canada_65_plus = 3_169_970 / 19_735_665  # Number of 65+ / Number of 20+

    return (rates[0] * canada_20_44
            + rates[1] * canada_45_64
            + rates[2] * canada_65_plus)


# Task 3: Finding the correlation


def get_stats_summary(ndata: 'CityData') -> float:
    """Return the correlation between hypertension rates standardized for age
    and low income rates across all neighbourhoods. 
    """
    
    ht_rates = []
    li_rates = []
    for neighbourhood in ndata:
        ht_rates.append(get_age_standardized_ht_rate(ndata, neighbourhood))
        li_rates.append(get_li_rate(ndata, neighbourhood))
    return statistics.correlation(ht_rates, li_rates)


# Task 4: Order by ratio


def order_by_ht_rate(ndata: 'CityData') -> list[str]:
    """Return a list of the names of the neighbourhoods in order from lowest to
    highest age-standardized hypertension rate.
    
    >>> order_by_ht_rate(SAMPLE_DATA)
    ['Elms-Old Rexdale', 'Rexdale-Kipling', 'Thistletown-Beaumond Heights', \
'West Humber-Clairville', 'Mount Olive-Silverstone-Jamestown']
    >>> new_sample_data = {"West Humber-Clairville": {"id": 1, "hypertension": \
[703, 13291, 3741, 9663, 3959, 5176], "total": 33230, "low_income": 5950,}, \
"Mount Olive-Silverstone-Jamestown": {"id": 2, "hypertension": [789, 12906, \
3578, 8815, 2927, 3902], "total": 32940, "low_income": 9690,},} 
    >>> order_by_ht_rate(new_sample_data)
    ['West Humber-Clairville', 'Mount Olive-Silverstone-Jamestown']
    """
    ht_rate_list = []
    sorted_dict = {}
    
    for neighbourhood in ndata:
        sorted_dict[neighbourhood] = (get_age_standardized_ht_rate
                                      (ndata, neighbourhood))
    sorted_dict = dict(sorted(sorted_dict.items(), key=lambda item: item[1]))

    for neighbourhood in sorted_dict:
        ht_rate_list.append(neighbourhood)
    
    return ht_rate_list


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # Using the small data files
    small_data = {}

    # Add hypertension data
    ht_file = open("hypertension_data_small.csv")
    get_hypertension_data(small_data, ht_file)
    ht_file.close()

    # Add low income data
    li_file = open("low_income_small.csv")
    get_low_income_data(small_data, li_file)
    li_file.close()

    # Created dictionary should be the same as SAMPLE_DATA
    print(small_data == SAMPLE_DATA)
