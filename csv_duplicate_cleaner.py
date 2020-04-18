from more_itertools import unique_everseen
with open('teams.csv','r') as f, open('teams_final.csv','w') as out_file:
    out_file.writelines(unique_everseen(f))
