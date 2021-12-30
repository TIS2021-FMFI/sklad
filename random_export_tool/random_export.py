import openpyxl as op
import pandas as pd
import random
import string
import time 

input_path = 'template.xlsx'
output_path = 'export.xlsx'


def randomly_occupy(df : pd.DataFrame, p : float=0.66):
    """Function iterates over DataFrame, setting column 'Materiál'
        of each row to either value: '<< prázdny >>' or random numerical
        string of 12 digits based on probability p, where p is the likelihood
        that row is occupied."""
    for i, row in df.iterrows():
        value = '<< prázdny >>' if random.random() > p else ''.join(random.choices(string.digits, k=12))
        df.at[i, 'Materiál'] = value
    
def add_random_unit(df : pd.DataFrame) -> pd.DataFrame:
    """Function creates new shelving unit of random name and random dimensions.
        Said shelving unit is unique and cannot be found in input dataframe."""
    shelf_count = random.randint(1, 10)
    cells_count = random.randint(1, 30)
    name = random_name(df)

    for i in range(shelf_count):
        for j in range(cells_count):
            place = f"{name}-{chr(ord('A') + i)}-{j:02}"
            df2 = pd.DataFrame({'Skladové miesto' : [place],
                       'Materiál' : ['<< prázdny >>']})
            df = df.append(df2, ignore_index = True)
    return df

def shelving_unit_name(storing_place : str) -> str:
    """Function retrieves name of shelving unit from name of storing place
        in format <shelingUnitName-shelfName-cellName>."""
    return storing_place.split('-', 2)[0]
    
        
def list_units(df : pd.DataFrame) -> set:
    """Function returns set of all shelving unit names in dataframe."""
    names = set()
    for i, row in df.iterrows():
        name = shelving_unit_name(df.at[i, 'Skladové miesto'])
        names.add(name)
    return names

def random_name(df : pd.DataFrame) -> str:
    """Function returns random shelving unit name which
        is not already in dataframe."""
    name = "00"
    names = list_units(df)
    i = 0
    while name in names:
        name = f"{i:02}"
        i += 1
    return name


def remove_random_unit(df : pd.DataFrame) -> pd.DataFrame:
    """Function selects random shelving unit name and
        removes all storing places of said shelving unit."""
    name0 = random.choice(list(list_units(df)))
    indexes = []

    for i, row in df.iterrows():
        name1 = shelving_unit_name(df.at[i, 'Skladové miesto'])
        if name1 == name0:
            indexes.append(i)
    df = df.drop(indexes)
    return df

def simulate(input_path : str, output_path : str, period : int=300, n : int=-1, m : int=-1):
    """Function takes template file and produces export files peridically.
        Each cycle takes previous export file and modifies it.

        Parameters
        ----------
        input_path : str
            The path of template file.

        output_path : str
            The path of export file.

        period : int, optional
            Seconds of one period, time taken between two different
            exports are created (Default is 300 seconds, which is 5 minutes).

        n : int, optional
            Number states how many cycles are needed to be taken in order
            for the function to create random shelving unit of random dimensions
            in export (Default is -1).

        m : int, optional
            Number states how many cycles are needed to be taken in order
            for the function to remove random shelving unit in export
            (Default is -1).
        """
    df = pd.read_excel(input_path)
    i = 0
    j = 0
    while True:
        try:                
            if i == n:
                i = 0
                df = add_random_unit(df)
            if j == m:
                j = 0
                df = remove_random_unit(df)
            randomly_occupy(df)   
            df.to_excel(output_path)  
            time.sleep(period)
            i += 1
            j += 1
        except PermissionError:
            print('Other app is using output file')
            time.sleep(20)
            
        

if __name__ == '__main__':
    """df = pd.read_excel(input_path)
    randomly_occupy(df)
    df.to_excel(output_path)"""
    simulate(input_path, output_path)

    
