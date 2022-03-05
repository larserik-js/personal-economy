import numpy as np

# # Porteføljeværdi pr. 04.02.22 (REGNER IKKE PENSION MED)

current_year = 2022

## Indsæt dagens valutakurser
er_NOK = 0.76305419
er_EUR = 7.4440008


## Norge (alle værdier i NOK)
# Kontanter
coop = 393.33                                  # COOP Midt-Norge
spb_oe = 0.0                               # Sparebank Øst-konto
BSU = 0                     # BSU-konto + brukskonto

kontanter_NO = coop + spb_oe

# Gæld
laanekassen = 159910                        # Lånekassen
Anna = 19000                                # Gæld til Anna

gaeld_NO = laanekassen + Anna

# Værdipapirer
DNB_aktiv_30 = 0                        # DNB Aktiv 30, kombinationsfond
DNB_EM = 0                              # DNB Emerging Markets
DNB_Global = 0                          # DNB Global Indeks

vaerdipapirer_NO = DNB_aktiv_30 + DNB_EM + DNB_Global

total_NO = (kontanter_NO + BSU - gaeld_NO + vaerdipapirer_NO)*er_NOK

# Pension
alderspension = 76026.00                    # Alderspension (NAV)

pension_no = 0.              # Total pension (Norge)

## Danmark (alle værdier i DKK)
# Kontanter
faelles = 6525.40/2                            # Nordea fælleskonto
privat = 1507.30                               # Nordea privatkonto

kontanter_DK = faelles + privat

# Gæld
SU_laan = 199379.00                            # SU-lån
BN = 9975                                 # Bank Norwegian-kreditkort

gaeld_DK = SU_laan + BN

# Obligationer
saxo_bonds = 19595                       # iShares Global Aggregate Bond...

# Aktier
saxo_stocks = 314536.67 - saxo_bonds                  # Saxo Investor

# Ejendom
TM = 37383.53                               # The Many

# Pension
pfa = 48057.00                              # Privat pension (PFA)

pension_dk = 0.                             # Total pension (Danmark)

total_DK = (kontanter_DK - gaeld_DK 
            + saxo_stocks + saxo_bonds 
            + TM + pension_dk)

total_DK = 700000
## Udlandet (valuta angivet)
Mintos = 3603.09                            # Værdi i EUR

total_udlandet = Mintos*er_EUR

## Total porteføljeværdi
aktier_tot = er_NOK*(0.30*DNB_aktiv_30 + DNB_EM + DNB_Global) + saxo_stocks
obl_tot = er_NOK*0.70*DNB_aktiv_30 + saxo_bonds
ejendom_tot = TM
laan_tot = er_EUR*Mintos
kontanter_tot = er_NOK*kontanter_NO + kontanter_DK
pension_tot = pension_no + pension_dk
BSU *= er_NOK
aktiva = aktier_tot + obl_tot + ejendom_tot + laan_tot + pension_tot

b = total_NO + total_DK + total_udlandet


print("Porteføljeværdi: {:.2f}".format(total_NO)  + " DKK (Norge) + {:.2f}".format(total_DK)\
                            + " DKK (Danmark)\n+ {:.2f}".format(total_udlandet) +\
                            " DKK (udlandet) = {:.2f}".format(b) + " DKK\n")
print("Andele af aktiva:")
print(f"Aktier: {100*aktier_tot/aktiva:.2f}%")
print("Obligationer: " + "{:.2f}".format(100*obl_tot/aktiva) + "%")
print("Ejendom: " + "{:.2f}".format(100*ejendom_tot/aktiva) + "%")
print("Lån: " + "{:.2f}".format(100*laan_tot/aktiva) + "%")
print(f"Totalt: {aktiva:.2f} DKK\n")
print(f"BSU: {BSU:.2f} DKK")
print(f"Øvrige kontanter: {kontanter_tot:.2f} DKK\n")


## Parametre
# Present value of portfolio WITHOUT PENSION FUNDS
##b = 300000       ## Comment out if using the actual value from above

l = 10000        ## Net monthly investments
r = 0.05         ## Expected average yearly return on portfolio
f = r/12         ## Factor of monthly return

g = 55300        ## Upper limit (DKK) on the 27% tax rate on "aktieindkomst" (2020)
s_l = 0.27       ## Tax rate for return below the limit on "aktieindkomst"
s_h = 0.42       ## Tax rate for return above the limit on "aktieindkomst"


y = 40           ## Number of years from present

v = b
v_gen = 0        ## Taxable value, i.e. value generated

for i in range(12*y):
    if (i+1)%12 != 0:
        val = f*v                   ## Value of monthly return
        v_gen += val                ## Adds monthly return to total yearly return
        v += val                    ## Adds the monthly return
        v += l                      ## Adds the salary at the end of the month
    else:
        y_no = (i+1)/12             ## The year number, for printing
        val = f*v                   ## Value of monthly return
        v_gen += val                ## Adds monthly return to total yearly return
        v += val                    ## Adds the monthly return
        if v_gen <= g:
            t = s_l*v_gen           ## Tax amount, calculated from taxable return
        else:
            t_h = s_h*(v_gen - g)   ## Tax amount, calculated from taxable return
                                    ## above the "aktieindkomst" limit
            t = s_l*g + t_h         ## Total tax amount, calculated from the total taxable return
            
        
        v += (l-t)                  ## Adds the last salary of the year, where tax is deducted
        
        print("Year " + str(int(y_no+current_year)) + ":")
        print("Taxable return: " + "{:.2f}".format(v_gen) + ", and tax paid: " + "{:.2f}".format(t))
        print("Portfolio value: " + "{:.2f}".format(v))
        print("")
        
        v_gen = 0                   ## Resets the taxable value to zero for the next calendar year

