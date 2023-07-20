import pandas as pd

df = pd.read_excel('code metrics sourcemonitor', sheet_name=None)

core_dfs = [df[sheet_name] for sheet_name in df.keys() if sheet_name.startswith('core')]

core_metrics = pd.concat(core_dfs, ignore_index=True, sort=False)
subsystems_metrics = df['subsystems']

with pd.ExcelWriter('BuR Metrics.xlsx') as writer:  
    core_metrics.to_excel(writer, sheet_name='Core')
    subsystems_metrics.to_excel(writer, sheet_name='Subsystems')
