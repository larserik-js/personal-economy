#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 19:47:05 2021

@author: larserikskjegstad
"""
import numpy as np
import pandas as pd
import sys

path = "Documents/python_files/portfolio/"
sys.path.append(path)


df = pd.read_csv(path + "foreign_income_and_balance.csv",skiprows=8,
                 delimiter=";",usecols=np.arange(5))
print(df)

headers = df.columns.values
print(headers)

#Mintos = (df.loc[df.Category == "Mintos_IIPY"]).to_numpy()[0][1:]

#############################################################################
############################## WRITE TAX YEAR ###############################

tax_year = "2020"

#############################################################################
#############################################################################

# Sets the exchange rates for the tax year
ER_NOK = (df.loc[(df.Category == "ER_NOK")])[tax_year].to_numpy()[0]
ER_EUR = (df.loc[(df.Category == "ER_EUR")])[tax_year].to_numpy()[0]

## Renteudgifterne i rubrik 432
## Gælden i rubrik 493


print("#######################################################################")
print("NORGE: Renter og formue fra udlandet:")
print("#######################################################################")
# Renteindtægter
print("431 Renteindtægter:")
df_array = (df.loc[(df.Category == "Brukskonto_IIPY") 
               | (df.Category == "Sparekonto_IIPY")
               | (df.Category == "BSU_IIPY")
               | (df.Category == "BSU_Start_IIPY")
               | (df.Category == "SPOE_IIPY")]
        )[tax_year].to_numpy()

print("Totalt: " + str(df_array.sum()) + str(" NOK") + " = "\
      + f"{0.01*ER_NOK*(df_array.sum()):.2f}" + " DKK\n"
      )

# Renteudgifter
print("432 Renteudgifter af gæld i udlandet:")
df_array = (df.loc[(df.Category == "Laanekassen_IP")])[tax_year].to_numpy()
#print(df_array)

print("Totalt: " + str(df_array[0]) + str(" NOK") + " = "\
      + f"{0.01*ER_NOK*df_array[0]:.2f}" + " DKK\n"
      )

# Kapitalværdistigninger af udenlandske pensionsordninger
print("433 Kapitalværdistigninger af udenlandske pensionsordninger:")
print("Totalt: 0 NOK" + " = 0 DKK\n")

# Anden kapitalindkomst
print("434 Anden kapitalindkomst, herunder gevinst eller tab på")
print("investeringsforening og finansielle instrumenter. Fradragsberettiget")
print("tab angives med minus.")
print("Totalt: 0 NOK\n")

print("492 Indestående i udenlandske pengeinstitutter mv. Kursværdi af")
print("obligationer og af pantebreve i udenlandsk depot mv.")
print("Totalt: 0 NOK\n")

# Gæld i udlandet
print("493 Gæld til udenlandske pengeinstitutter, pantebreve i udenlandsk")
print("depot mv.")
df_array = (df.loc[(df.Category == "Laanekassen_Debt")])[tax_year].to_numpy()
#print(df_array)

print("Totalt: " + str(df_array[0]) + str(" NOK") + " = "\
      + f"{0.01*ER_NOK*df_array[0]:.2f}" + " DKK\n"
      )

# #Betalt skat i udlandet
# print("Betalt skat i udlandet:")
# print("Totalt: 0 NOK\n")

# #Formueoplysninger 
# print("Formueoplysninger:")
# df_array = (df.loc[(df.Category == "Brukskonto_AB") 
#                | (df.Category == "Sparekonto_AB")
#                | (df.Category == "BSU_AB")
#                | (df.Category == "BSU_Start_AB")
#                | (df.Category == "SPOE_AB")]
#         )[tax_year].to_numpy()

# print("Totalt: " + str(df_array.sum()) + str(" NOK\n"))




## Udenlandske aktier og investeringsbeviser
print("#######################################################################")
print("NORGE: Udenlandske aktier og investeringsbeviser:")
print("#######################################################################")

print("422 Gevinst/tab på udenlandske aktier/beviser i obligationsbaserede")
print("investeringsselskaber (lagerprincippet, kapitalindkomst).")
print("Tab angives med minus")
df_array = (df.loc[
                  (df.Category == "DNB_MFB_Gain") 
                | (df.Category == "DNB_MFB_Loss")
                | (df.Category == "DNB_MFB_Unrealized")
                ]
                )[tax_year].to_numpy()

print("Totalt: " + str(df_array.sum()) + str(" NOK") + " = "\
       + f"{0.01*ER_NOK*df_array.sum():.2f}" + " DKK\n"
       )


# # Aktieudbytte, der er kapitalindkomst
# print("Aktieudbytte, der er kapitalindkomst:")
# print("Totalt: 0 NOK\n")

# # Udbytter, der er aktieindkomst
# print("Udbytter, der er aktieindkomst:")
# print("Totalt: 0 NOK\n")

# Gevinst/tab på aktier og investeringsbeviser 
print("Gevinst/tab på aktier og investeringsbeviser:")
df_array = (df.loc[(df.Category == "DNB_MFS_Gain") 
               | (df.Category == "DNB_MFS_Loss")
               | (df.Category == "DNB_MFB_Gain")
               | (df.Category == "DNB_MFB_Loss")]
        )[tax_year].to_numpy()

#print(df_array)
print("Totalt: " + str(df_array[0]-df_array[1]+df_array[2]-df_array[3]) 
      + str(" NOK\n"))
# Formue oplysninger.
print("Formueoplysninger:")
print("Totalt: 0 NOK\n")


print("#######################################################################")
print("LETLAND: Renter og formue fra udlandet:")
print("#######################################################################")

# Renteindtægter
print("Renteindtægter:")
df_array = (df.loc[(df.Category == "Mintos_IIPY")])[tax_year].to_numpy()

print("Totalt: " + str(df_array.sum()) + str(" EUR\n"))

#Formueoplysninger 
print("Formueoplysninger:")
df_array = (df.loc[(df.Category == "Mintos_AB")]
        )[tax_year].to_numpy()

#print(RI)
print("Totalt: " + str(df_array.sum()) + str(" EUR\n"))
