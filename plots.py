import matplotlib.pyplot as plt
from utilities import get_years, mean, median, mode, range_df_fi, percent_mt_f, percent_lt_f, get_df_years
from utilities import y_df_f, y_s_f, ys_df_f_c, ys_df_f
from utilities import branches, branch_names
from utilities import plot_branches, plot_categories, plot_b_and_c, plot_total, save_fig

str_code = "2009-2022"
branches_to_get_data = branches["all"]
years_dfs = get_df_years(str_code)
_years = get_years(str_code)

name_format = "Year wise {type} of branches - {branches}"
mean_name = name_format.format(
    type="Mean", branches=", ".join(branches_to_get_data))
median_name = name_format.format(
    type="Median", branches=", ".join(branches_to_get_data))
mode_name = name_format.format(
    type="Mode", branches=", ".join(branches_to_get_data))
max_name = name_format.format(
    type="Max", branches=", ".join(branches_to_get_data))
min_name = name_format.format(
    type="Min", branches=", ".join(branches_to_get_data))


df_year_wise_mean = y_df_f(years_dfs, "ctc", mean,
                           branches_to_get_data, slice(len(years_dfs)), _years)
df_year_wise_median = y_df_f(years_dfs, "ctc", median,
                             branches_to_get_data, slice(len(years_dfs)), _years)
df_year_wise_mode = y_df_f(years_dfs, "ctc", mode,
                           branches_to_get_data, slice(len(years_dfs)), _years, transform=lambda x: x.count() > 0 and x.iloc[0] or 0)

df_year_wise_max = y_df_f(years_dfs, "ctc", lambda x, y, z: x[x[z] > 0][y].max(),
                          branches_to_get_data, slice(len(years_dfs)), _years)

df_year_wise_min = y_df_f(years_dfs, "ctc", lambda x, y, z: x[x[z] > 0][y].min(),
                          branches_to_get_data, slice(len(years_dfs)), _years)

df_year_wise_total = y_df_f(years_dfs, "ctc", lambda x, y, z: x[z].sum(
), branches_to_get_data, slice(len(years_dfs)), _years)

df_year_wise_range = y_df_f(years_dfs, "ctc", range_df_fi,
                            branches_to_get_data, slice(len(years_dfs)), _years)

df_year_wise_pm_mean = y_df_f(years_dfs, "ctc", percent_mt_f(mean), branches_to_get_data,
                              slice(len(_years)), _years)

df_year_wise_pm_median = y_df_f(years_dfs, "ctc", percent_mt_f(median), branches_to_get_data,
                                slice(len(_years)), _years)

df_year_wise_pl_mean = y_df_f(years_dfs, "ctc", percent_lt_f(mean), branches_to_get_data,
                              slice(len(_years)), _years)


df_year_wise_pl_median = y_df_f(years_dfs, "ctc", percent_lt_f(median), branches_to_get_data,
                                slice(len(_years)), _years)

# print(df_year_wise_mean_c)
# print(ys_df_f_c(df_year_wise_mean_c, transform=lambda x: x.mean()))
# print(ys_df_f_c(df_year_wise_median, transform=lambda x: x.median()))
# print(df_year_wise_max)
# print(df_year_wise_min)


# print(ys_df_f_c(df_year_wise_mean_c, transform=lambda x: x.mean()))
# print(ys_df_f(df_year_wise_max, _index=_years,
#       transform=lambda x: x.max(), name="max. CTC over years"))


# Plots for Comparison

# 1. Branch x vs. Branch y vs. ... over years y1, y2, ... yn
branches_to_compare = ["cse", "ece", "it"]
branch_names_neat = [branch_names[branch] for branch in branches_to_compare]
years_to_compare_branches = get_years("2009-2022")
title = "Year wise mean of branches - " + ", ".join(branch_names_neat)
filepath_list_branch = [
    "branch", f"year-wise-mean-of-{'-'.join(branches_to_compare)}.png"]
comparison_data = df_year_wise_mean

plot_branches(comparison_data, years_to_compare_branches, branches_to_compare,
              title, "Years", "Mean CTC", filepath_list=filepath_list_branch)


# 2. Categrory x vs. Category y vs. ... over years y1, y2, ... yn
categories_to_compare = ["ug_core", "ug_noncore"]
categories_names_neat = [branch_names[cat] for cat in categories_to_compare]
years_to_compare_categories = get_years("2009-2022")
title = "Year wise mean of categories - " + ", ".join(categories_names_neat)
filepath_list_cat = [
    "category", f"year-wise-mean-of-{','.join(categories_to_compare)}.png"]
comparison_data = df_year_wise_mean
def func(x): return x.mean(axis=1)


plot_categories(comparison_data, years_to_compare_categories,
                categories_to_compare, func, title, "Years", "Mean CTC", filepath_list=filepath_list_cat)

# 3. Branch x vs. Category y vs. ... over years y1, y2, ... yn
branches_to_compare = ["cse", "ece", "it"]
branch_names_neat = [branch_names[branch] for branch in branches_to_compare]
categories_to_compare = ["ug_core", "ug_noncore"]
categories_names_neat = [branch_names[cat] for cat in categories_to_compare]
years_to_compare_b_and_c = get_years("2009-2022")
title = "Year wise mean of branches - " + \
    ", ".join(branch_names_neat) + " and categories - " + \
    ", ".join(categories_names_neat)
filepath_list_b_and_c = [
    "branch_and_category", f"year-wise-mean-of-{'-'.join(branches_to_compare)}-and-{','.join(categories_to_compare)}.png"]
comparison_data = df_year_wise_mean
def func(x): return x.mean(axis=1)


plot_b_and_c(comparison_data, years_to_compare_b_and_c, branches_to_compare,
             categories_to_compare, func, title, "Years", "Mean CTC", filepath_list=filepath_list_b_and_c)

# 4. Total Number of Placements over years
str_year_to_check = "2009-2022"
years_to_check = get_years(str_year_to_check)
branches_to_check = branches['all']
branches_to_check_neat = [branch_names[branch] for branch in branches_to_check]
branches_title = ", ".join(branches_to_check_neat)
title = f"Total Number of Placements over years - {str_year_to_check} - {branches_title if len(branches_title) < 30 else branches_title[:30] + '...'}"
filepath_list_total = ["total", "total-placements-over-years.png"]
comparison_data = df_year_wise_total.loc[years_to_check][branches_to_check]
def func_axis0(x): return x.sum(axis=1)
def func_axis1(x): return x.sum(axis=1)


plot_total(df_year_wise_total, years_to_check,
           branches_to_check, title, filepath_list_total, transform=func_axis1, xlabel="Year", ylabel="Total Placements")


# 5. Quality of placements over years
# finding no. of placements over mean
years_str = "2009-2022"
years_to_check = get_years(years_str)
branches_to_check = ["cse", "ece", "it"]
branches_to_check_neat = [branch_names[branch] for branch in branches_to_check]
comparison_data_pm = df_year_wise_pm_mean.loc[years_to_check][branches_to_check]
title = f"Quality of placements over years - {years_str} - {', '.join(branches_to_check_neat)}"
filepath_list_quality = ["quality", "quality-of-placements-over-years.png"]

comparison_data_pm.plot(kind="bar", title=title, figsize=(10, 5))
save_fig(filepath_list_quality)
plt.show()
