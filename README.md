# current-app
This app is designed to be used with the boat that Carter and Al built <3
This program will parse the CAN Bus data and display it on a UI on the raspberry pi screen. 
Carter & Jillian 4eva <3


List of PGNs and expected outputs

0xFF20  # MCU_Summary
Returns             Value       Factor      Unit
MCU_charged_energy  number      0.01        kWh
MCU_Chargestate     y/n                     
MCU_PlugState
9x fault categories

## This one was entered wrong in the script initially, as FF10, returned MCU_config which is not needed
0xFF21 MCU_PackSummary  
Returns             Value       Factor      Unit
MCU_PackVoltage     number      0.1         volts
MCU_PackCurrent     number      0.1         amps
## We will also calculate Pack kW by multiplying PackVoltage and PackCurrent

0xFF22 MCU_CellSummary
Returns             Value       Factor      Unit
MCU_CellCount       number      1
MCU_LowestCellV     number      0.1         mV
MCU_MeanCellV       number      0.1         mV
MCU_HighestCellV    number      0.1         mV

0xFF24 MCU_SOCSummary
Returns             Value       Factor      Unit
MCU_SOC             0-100                   %
MCU_PackCurKwh      number                  kWh
MCU_PackMaxKwh      number                  kWh

0xFF11 BMS_Config1
Returns             Value       Factor      maximum     Unit
BMS_HVC             number      0.1         1           mV
BMS_LVC             number      0.1         1           mV
BMS_BVMin           number      0.1         1           mV

## THIS ONE ONLY FOR MAKING MCU CONFIGURATION CHANGES ##
0xEFD0 MCU_Write
Will edit MCU_Profile in B1 8bits long enter 1 for profile 1, 2 for profile 2


