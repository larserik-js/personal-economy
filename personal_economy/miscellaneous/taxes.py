import numpy as np 



## Opgørelse af personlig indkomst
L = 77778                             # Lønindkomst, brutto
H = 13140                             # Honorarer, brutto (B-indkomst mv.)
AM = int(0.08*L) + int(0.08*H)        # Arbejdsmarkedsbidrag (AM-bidrag)

PDS = 73992                           # Pensioner, dagpenge, stipendier mv. (fx SU)

PI = L + H - AM + PDS                 # Personlig indkomst i alt

print("Personlig indkomst i alt: " + str(PI) + " DKK.")


## Kapitalindkomst
RI = -21                              # Renteindtægter
                                      # Fx bankkonti
UKI = 341                             # Udenlandsk kapitalindkomst
                                      # Fx udbytte fra kapitalindkomstbeskattede ETF-er
IS = 3054                             # Gevinst/tab på aktier/beviser i investeringsselskaber
                                      # Fx kapitalindkomstbeskattede ETF-er
KI = RI + UKI + IS                    # Kapitalindkomst i alt
print("Kapitalindkomst i alt: " + str(KI) + " DKK.")


## Ligningsmæssige fradrag
FK = 300                              # Fagligt kontingent (højst 6000 DKK (2020))
                                      # Fx afgift til fagforening
B = 3727                              # Befordring
                                      # Fx transport til og fra arbejde
EBF = round(0.64*B)                   # Beregnet ekstra befordringsfradrag (højst 15400 DKK (2020))
                                      # Bliver gradvist reduceret ved indkomst over 
                                      # 284300 DKK til 334300 DKK (2020). Kompliceret beregning.

ATP_brutto = 474                      # Indbetalinger til ATP (pension)
ATP = (1-0.08)*ATP_brutto             # Indbetalinger til privattegnede og arbejdsgiveradministrerede 
                                      # fradragsberettigede pensionsordninger, dvs. indbetalinger til ATP
                                      # efter arbejdsmarkedsbidrag (8,00%)
BF = round(0.101*(L+H+ATP_brutto))    # Beskæftigelsesfradrag (højst 37200 DKK (2020))
EATP = round(0.08*ATP)                # Ekstra pensionsfradrag (op til et grundbeløb på 71500 DKK (2020))

LF = FK + B + EBF + BF + EATP         # Ligningsmæssige fradrag i alt
print("Ligningsmæssige fradrag i alt: " + str(LF) + " DKK.")


## Aktieindkomst
AU = 381                              # Udbytte DK-aktier mv. på reguleret marked, DK-depot
                                      # Fx fra rene danske aktier og fonde, der ikke er ETF-er
AUU = 40                              # Udbytte af udenlandske aktier på reguleret marked, DK-depot
                                      # Fx fra rene udenlandske aktier og fonde, der ikke er ETF-er
A = -3035                             # Gevinst/tab på aktier på reguleret marked mv.
                                      # Fx rene aktier og fonde, der ikke er ETF-er

if AU + AUU + A < 0:                  # Tab på aktier på reguleret marked overført til ægtefælle
    O = np.abs(AU + AUU + A)
else:
    O = 0

AUI = 215                             # Udbytte DK-aktier ej på reguleret marked, DK-depot
                                      # Fx udbytte fra Brickshare-ejendomme
SA = AU + AUU + A + O + AUI           # Samlet aktieindkomst
print("Samlet aktieindkomst: " + str(SA) + " DKK.")


SI = PI + KI - LF                     # Skattepligtig indkomst i alt

print("Skattepligtig indkomst i alt: " + str(SI) + " DKK.")


## Skatteberegning og opgørelse
## Satser (2019):
BS = 0.1213                           # Bundskat (2019, 0.1211 i 2020)
KS = 0.2380                           # Kommuneskat (2019, 2020)
TS = 0.15                             # Topskat (2019,2020)
AS = 0.27                             # Skat af aktieindkomst
PF = 46200                            # Personfradrag (2019, 46500 i 2020)
TSF = 531400                          # Topskat (bundgrænse efter AM-bidrag er fratrukket (2019))
KIF = 44800                           # Bundfradrag i positiv nettokapitalindkomst i topskattegrundlag (2019, 45800 i 2020)

indeholdt_DK = AS*(AUI + AU)          # Indeholdt skat (Danmark)
                                      # Fx ved rene danske aktier og fonde, der ikke er ETF-er
                                      # og Brickshare

## Bundskat
if (0 < PI+KI) & (PI+KI <= PF):
    bundskat = 0
else:
    bundskat = BS*(PI+KI - PF)
    
## Topskat
if (PI > TSF) & (KI > KIF):           # Skattepligtig indkomst er i sig selv højere end bundfradraget (TSF)
                                      # I tillæg er nettokapitalindkomsten højere end bundfradraget (KIF)
    topskat = TS*(PI-TSF + KI)
elif (PI > TSF) & (KI <= KIF):        # Skattepligtig indkomst er i sig selv højere end bundfradraget (TSF)
                                      # Nettokapitalindkomsten er lavere end eller lig med bundfradraget (KIF)
    topskat = TS*(PI-TSF)
elif (PI <= TSF) & (KI-KIF > TSF-PI): # Skattepligtig indkomst er lavere end eller lig med bundfradraget (TSF)
                                      # Summen af nettokapitalindkomsten, der overstiger bundfradraget (KIF)
                                      # og skattepligtig indkomst, er højere end bundfradraget (TSF)
    topskat = TS*(PI-TSF+KI-KIF) 
else:
    topskat = 0
    
## Kommuneskat
if (0 < SI) & (SI <= PF):
    kommuneskat = 0
else:
    kommuneskat = KS*(SI - PF)
    
skat_aktie = AS*SA
                                      # Skråt loft: 52.06% (2020)
                                      # Loft på kapitalindkomst: 42% (2020)

beregnet_skat = AM + bundskat + topskat + kommuneskat + skat_aktie
print("Beregnet skat: " + "{:.2f}".format(beregnet_skat) + " DKK.")



print(PI+KI)



