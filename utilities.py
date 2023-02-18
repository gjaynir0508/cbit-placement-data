import pandas as pd
import re
import os
import matplotlib.pyplot as plt
# base = "https://gjaynir0508.github.io/cbit-placement-data"
base = "."

# To read all the csv's
#
# df2009 = pd.read_csv(f"{base}/2009-10-placements.csv")
# df2010 = pd.read_csv(f"{base}/2010-11-placements.csv")
# df2011 = pd.read_csv(f"{base}/2011-12-placements.csv")
# df2012 = pd.read_csv(f"{base}/2012-13-placements.csv")
# df2013 = pd.read_csv(f"{base}/2013-14-placements.csv")
# df2014 = pd.read_csv(f"{base}/2014-15-placements.csv")
# df2015 = pd.read_csv(f"{base}/2015-16-placements.csv")
# df2016 = pd.read_csv(f"{base}/2016-17-placements.csv")
# df2017 = pd.read_csv(f"{base}/2017-18-placements.csv")
# df2018 = pd.read_csv(f"{base}/2018-19-placements.csv")
# df2019 = pd.read_csv(f"{base}/2019-20-placements.csv")
# df2020 = pd.read_csv(f"{base}/2020-21-placements.csv")
# df2021 = pd.read_csv(f"{base}/2021-22-placements.csv")
# df2022 = pd.read_csv(f"{base}/2022-23-placements.csv")

# Utility Functions

# Function to get dataframe for given starting year


def get_df(year):
    return pd.read_csv(f"{base}/{year}-{(year+1) % 100}-placements.csv")

# Function to create a list of years from given str input


def get_years_single(str_code_single):
    years = re.findall(r"\d{4}", str_code_single)
    return range(int(years[0]), int(years[1]) + 1) if len(years) == 2 else [int(years[0])]


matcher = re.compile(r",*(\d{4}-\d{4}|\d{4})", re.X)


def get_years(str_code):
    matches = matcher.finditer(str_code)
    return [year for x in matches for y in x.groups() for year in get_years_single(y)]

# Function to get df's from a given str_code


def get_df_years(str_code):
    return [get_df(year) for year in get_years(str_code)]

# Function to flatten a frequency table


def flatten(df, xi, fi):
    return pd.Series([x for freq, x in zip(df[fi], df[xi]) for _ in range(int(freq))], dtype=float)

# Function to find mean of a frequency column wrt a class mark column


def mean(df, xi, fi):
    s = sum(df[fi])
    return sum(df[fi] * df[xi]) / s if s != 0 else 0

# Function to find median of frequency table


def median(df, xi, fi):
    return flatten(df, xi, fi).median()

# Function to find mode(s) of frequency table


def mode(df, xi, fi):
    return flatten(df, xi, fi).mode()

# Function to find percentage of values more than a function output


def percent_mt_f(func):
    def _percent_more_than_f(df, xi, fi):
        val = func(df, xi, fi)
        total = df[fi].sum()
        return df[df[xi] > val][fi].sum() * 100 / total if total > 0 else 0
    return _percent_more_than_f

# Function to find percentage of values less than a function output


def percent_lt_f(func):

    def _percent_less_than_ct(df, xi, fi):
        val = func(df, xi, fi)
        total = df[fi].sum()
        return df[fi][df[xi] < val].sum() * 100 / total if total > 0 else 0
    return _percent_less_than_ct


# Function to find range of a frequency table (max - min)


def range_df_fi(df, xi, fi):
    df = df[df[fi] > 0]
    return df[xi].max() - df[xi].min()


# Year DF to functional values of each branch


def y_s_f(df: pd.DataFrame, xi, func, _slice, transform=lambda x: x, name=""):
    _slice = list(set(_slice) & set(df.columns))
    _extra = list(set(_slice) - set(df.columns))
    if _extra:
        print(f"Warning: Extra columns: {_extra}")
        for col in _extra:
            df.insert(0, col, 0)
    cols = df[_slice]
    series = pd.Series([transform(func(df, xi, key))
                       for key in cols], index=cols.columns, dtype=float, name=name)
    return series

# Function to loop over df's and create a df


def y_df_f(df_arr, xi, func, _slice, _years_slice, _years, transform=lambda x: x):
    years = df_arr[_years_slice]
    y_df = pd.DataFrame((y_s_f(year_df.fillna(0), xi, func, _slice, transform)
                        for year_df in years), index=_years)
    return y_df

# Getting transfomed row wise year


def ys_df_f(df_year_wise: pd.DataFrame, _index=None, transform=lambda x: x, name=""):
    df = df_year_wise.loc[_index] if _index is not None else df_year_wise
    series = pd.Series([transform(x) for x in df.iloc],
                       index=df.index, name=name)
    return series

# Getting tarnsformed column wise year


def ys_df_f_c(df_year_wise, _index=None, transform=lambda x: x, name=""):
    df = df_year_wise[_index] if _index is not None else df_year_wise
    series = pd.Series([transform(df[col])
                       for col in df], index=df.columns, name=name)
    return series


ug_brnch = ['ece', 'cse', 'eee', 'it', 'mech', 'prod', 'civil', 'chem', 'bio']
ug_core_brnch = ['eee', 'mech', 'civil', 'chem']
ug_noncore_brnch = ['it', 'prod', 'bio', 'cse', 'ece']
ug_circuit_brnch = ['eee', 'ece', 'cse', 'it']
ug_noncircuit_brnch = ['mech', 'civil', 'chem', 'prod']
pg_brnch = ['mca', 'mcse', 'mcnis', 'maid', 'mece', 'mvs',
            'mpp', 'meee', 'mcad', 'mciv', 'mth', 'mstr', 'mba']
pg_engg_brnch = ['mcse', 'mcnis', 'maid', 'mece',
                 'mvs', 'mpp', 'meee', 'mcad', 'mciv', 'mth', 'mstr']
pg_nonengg_brnch = ['mca', 'mba']
all_brnch = ug_brnch + pg_brnch

# Dictionary of branch codes
branches = {
    "all": all_brnch,
    "ug": ug_brnch,
    "ug_core": ug_core_brnch,
    "ug_noncore": ug_noncore_brnch,
    "ug_circuit": ug_circuit_brnch,
    "ug_noncircuit": ug_noncircuit_brnch,
    "pg": pg_brnch,
    "pg_engg": pg_engg_brnch,
    "pg_nonengg": pg_nonengg_brnch,
}

# Dictionary of neat Branch names
ug_branch_names = {"cse": "CSE", "ece": "ECE", "eee": "EEE", "it": "IT",
                   "mech": "Mechanical", "prod": "Production", "civil": "CIVIL", "chem": "Chemical", "bio": "Bio-Tech"}
pg_branch_names = {"mca": "MCA", "mcse": "ME / CSE", "mcnis": "ME / CNIS", "maid": "ME / AI&DS", "mece": "ME / ECE", "mvs": "MVS",
                   "mpp": "MPP", "meee": "MEEE", "mcad": "MCAD", "mciv": "MCIV", "mth": "MTH", "mstr": "MSTR", "mba": "MBA"}
branch_names = {"all": "All Branches", "ug": "UG", "ug_core": "UG Core", "ug_noncore": "UG Non-Core", "ug_circuit": "UG Circuit", "ug_noncircuit": "UG Non-Circuit", "pg": "PG", "pg_engg": "PG Engg", "pg_nonengg": "PG Non-Engg", **ug_branch_names, **pg_branch_names
                }


# Plotting Functions
base_save_path = os.path.join(os.getcwd(), "plots")


def save_fig(filepath_list):
    if filepath_list is not None:
        if not os.path.exists(os.path.join(base_save_path, *filepath_list[:-1])):
            os.makedirs(os.path.join(base_save_path, *filepath_list[:-1]))
        plt.savefig(os.path.join(base_save_path, *filepath_list))

# Function to plot branches


def plot_branches(ys_df, rows, cols, title, xlabel, ylabel, figsize=(10, 5), filepath_list=None, show=True, _legend=None, **kwargs):
    not _legend and plt.figure(figsize=figsize)
    ys_df = ys_df.loc[rows][cols]
    legend = _legend if _legend is not None else []
    for col in ys_df:
        plt.plot(ys_df.index, ys_df[col], label=col, **kwargs)
        legend.append(branch_names[col])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(legend)
    plt.grid(True)
    if show:
        save_fig(filepath_list)
        plt.show()
        plt.close()
    return legend

# Function to plot categories


def plot_categories(ys_df, rows, categories, func, title, xlabel, ylabel, figsize=(10, 5), filepath_list=None, show=True, _legend=None, **kwargs):
    not _legend and (plt.figure(figsize=figsize))
    ys_df = ys_df.loc[rows]
    legend = _legend if _legend is not None else []
    for category in categories:
        cat_df = ys_df[branches[category]]
        plt.plot(cat_df.index, func(cat_df), label=category, **kwargs)
        legend.append(branch_names[category])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(legend)
    plt.grid(True)
    if show:
        save_fig(filepath_list)
        plt.show()
        plt.close()
    return legend


# Function to plot branches and categories


def plot_b_and_c(ys_df, rows, cols, categories, func, title, xlabel, ylabel, figsize=(10, 5), filepath_list=None, show=True, **kwargs):
    b_plots_legend = plot_branches(ys_df, rows, cols, title, xlabel, ylabel,
                                   figsize, filepath_list, False, **kwargs)
    plot_categories(ys_df, rows, categories, func, title, xlabel,
                    ylabel, figsize, filepath_list, show, _legend=b_plots_legend, **kwargs)

# Function to plot total placements


def plot_total(ys_df, rows, cols, title, filepath_list, figsize=(10, 5), show=True, transform=lambda x: x, **kwargs):
    comparison_data = transform(ys_df.loc[rows][cols])
    comparison_data.plot(kind="bar", grid=True,
                         title=title, figsize=figsize, **kwargs)
    if show:
        save_fig(filepath_list)
        plt.show()
        plt.close()
