import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import seaborn as sns
from numpy import savetxt

df = pd.read_csv("Time Americans Spend Sleeping.csv")

#               GRUPARI SI AGREGARI STANDARD
df2 = df.groupby(['Year', 'Sex'], as_index=False)['Avg hrs per day sleeping'].mean()
df2.to_csv("Avg_hrs_Sex_Year.csv")

df3 = df.groupby(['Age Group', 'Sex', 'Year'])['Avg hrs per day sleeping'].agg(['mean', 'min', 'max'])
df3.to_csv("AgeGroup_Sex_Year_functii.csv")

df4 = df.groupby(['Type of Days','Year'])['index'].count()
df4.to_csv("Day_Year_count.csv")

df5 = df.groupby(['Sex', 'Age Group']).first(5)
df5.to_csv("Sex_AgeGroup_first.csv")


#                 FILTARE DUPA ANUMITE GRUPE DE VARSTA, AGREGAREA DATELOR
age_groups = ['15 years and over', '18 years and over']
filtered_data = df[df['Age Group'].isin(age_groups)]

#   Grouping and aggregating the data
grouped_data = filtered_data.groupby(['Year', 'Sex']).agg({'Avg hrs per day sleeping': 'mean'})
print("Average hours of sleep per day by Year and Sex:\n", grouped_data)

#       Clasament dupa varste si sex pt avg_hrs
df['Rank'] = df.groupby(['Age Group', 'Sex'])['Avg hrs per day sleeping'].transform(lambda x: x.rank(ascending=False, method='min'))
ranked_data=df[['Age Group', 'Sex','Avg hrs per day sleeping','Rank']]
ranked_data.to_csv("Ranked_age_sex.csv")

#                        CREARE COLOANA NOUA
grouped_data = df.groupby(['Year', 'Type of Days']).agg({'Avg hrs per day sleeping': 'sum'})
total_sleep_per_year = grouped_data.groupby('Year').transform('sum')
grouped_data['Percentage Contribution'] = grouped_data / total_sleep_per_year * 100
print("Total hours of sleep per Year and Type of Days with Percentage Contribution:\n",grouped_data)


# Extrage valorile procentuale și etichetele din DataFrame
values = grouped_data['Percentage Contribution'].values
plot.pie(values, autopct='%1.1f%%')
plot.title('Contribuția procentuală în funcție de ani si tipul zilei')
plot.show()


#                        ABATERE STANDARD
grouped_data = df.groupby(['Age Group', 'Activity']).agg({'Avg hrs per day sleeping': ['mean', 'std']})
print("Average and Standard Deviation of hours of sleep per day by Age Group and Activity:\n",grouped_data)


#                        CORELATI DINTRE ORE DORMITE SI AN
correlation = df['Avg hrs per day sleeping'].corr(df['Year'])
print("Correlation between Avg hrs per day sleeping and Year:", correlation)

#              GRUPARE SI SORTARE CRESCATOARE A ORELOR DE SOMN DUPA GRUPA DE VARSTA (cresc după o val și descresc după alta simultan)
grouped_data = df.groupby(['Age Group']).apply(lambda x: x.sort_values(['Age Group', 'Avg hrs per day sleeping'], ascending=[True, False]))
print("Grouped and Sorted Data:\n", grouped_data)


# Impart setul de date in grupe diferite dupa Sex- FILTRARE
f_filter = df['Sex'] == 'Women'
df_filtered = df[f_filter]  #dff contine obervatii doar pt sex=women
df_filtered.to_csv("Women.csv")
df_filtered_gr = df_filtered.groupby('Year')['Avg hrs per day sleeping'].mean()


#          CALCUL MIN SI MAX PE DF FILTRAT
f_avg = df[f_filter].agg(f_MINavgHours=('Avg hrs per day sleeping', np.min),
                         f_MAXavgHours=('Avg hrs per day sleeping', np.max))
f_avg.to_csv("MinMax.csv")

#        numPy array for Avg hours per day sleeping
avg_hours = df[['Avg hrs per day sleeping']].values
savetxt('Hours.csv', avg_hours, delimiter=',')


# group all types of days -> numpy array
day = df['Type of Days'].unique()
print(day)
savetxt('Grupare_dupa_Zi.csv', day, delimiter=',', fmt='%s')


# matrice cu tot setul de date
variabile_observate = list(df.columns)[:]
x = df[variabile_observate].values
xx = x[:315:15]
# print(xx) #toate linile in anul2003
savetxt('Grupare_dupa_2003.csv', xx, delimiter=',', fmt='%s')


# matrice cu nr de ore pe anul 2003 pt ambele sexe-> 21 de observatii
xxx = df["Avg hrs per day sleeping"].values
hours_list_2003_Both = xxx[:315:15]
savetxt('Grupare_dupa_2003_BOTH.csv', hours_list_2003_Both, delimiter=',', fmt='%s')
# print("Both: 2003: avg hrs per day sleeping: regardless of the age")
# print("Media nr de ore pe care o pers il doarme,in medie, intr-o zi in anul 2003, indiferent de varsta sau zi",np.mean(hours_list_2003_Both))
# print(hours_list_2003_Both) #tabel cu datele pe care se aplica media

y = df["Avg hrs per day sleeping"].values
hours_list_2017_Both = y[14:315:15]
# print("Both: 2017: avg hrs per day sleeping: regardless of the age")
# print("Media nr de ore pe care o pers il doarme,in medie, intr-o zi in anul 2017, indiferent de varsta sau zi",np.mean(hours_list_2017_Both))
# print(hours_list_2017_Both) #tabel cu datele pe care se aplica media

variabile_observate = list(df2.columns)[:]
z = df2[variabile_observate].values
zz = z[::3]  # doar Both -> toti anii -> avg hours per day
# print(zz.size)
# print(zz)

# sortez crescator
zzz = zz[zz[:, 2].argsort()]
savetxt('Sortare_cresc_Both.csv', zzz, delimiter=',', fmt='%s')



# #Grafic
plot.figure(figsize=(12, 10))
sns.barplot(x='Avg hrs per day sleeping', y='Year', data=df2, dodge=False)
plot.title("Ore vs Ani", fontsize=16)
plot.xlabel("Avg hrs per day sleeping")
plot.ylabel("Year")
plot.ylim(2003, 2017)
plot.show()

