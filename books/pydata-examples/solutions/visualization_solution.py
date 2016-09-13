print(grouped_mean_df.index)

subset = grouped_mean_df.loc[['United Kingdom', 'Germany', 'Greece', 'United States', 'Czech Republic']]

chart = draw_line(subset)

show(chart)
