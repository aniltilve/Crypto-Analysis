daily_elec_consump = 5.51 * 24 # kWh
elec_price = 0.181 # cents / kWh
btc_per_day = 0.00025723 # BTC

print(daily_elec_consump * elec_price / btc_per_day)