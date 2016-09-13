df['score_sum_dow'] = df.groupby('day_of_week')['score'].transform(sum)

df.sort_values('day_of_week').plot(x='day_of_week', y='score_sum_dow')


df['score_sum_user'] = df.groupby('by')['score'].transform(sum)

df.sort_values('score_sum_user', ascending=False).groupby('by')[['by', 'score_sum_user']].head(1)
