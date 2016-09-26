import ast

def get_list_len(line):
    if not line:
        return 0
    elif isinstance(line, list):
        return len(line)
    return len(ast.literal_eval(line))


df['hourly_desc_max'] = df.groupby('hour')['descendants'].transform(max)

df.sort_values('hour').plot(x='hour', y='hourly_desc_max')

df['num_kids'] = df['kids'].map(get_list_len)

df['hourly_kids_median'] = df.groupby('hour')['num_kids'].transform(median)

df.sort_values('hour').plot(x='hour', y='hourly_kids_median')

