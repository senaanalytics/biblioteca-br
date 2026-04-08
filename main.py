from biblioteca_br import bacen

print("=== Selic (2020-2024) ===")
df_selic = bacen.selic(inicio="01/01/2020", fim="31/12/2024")
print(df_selic.tail())

print("\n=== IPCA (2020-2024) ===")
df_ipca = bacen.ipca(inicio="01/01/2020", fim="31/12/2024")
print(df_ipca.tail())

print("\n=== Dólar (2020-2024) ===")
df_dolar = bacen.cambio("USD", inicio="01/01/2020", fim="31/12/2024")
print(df_dolar.tail())