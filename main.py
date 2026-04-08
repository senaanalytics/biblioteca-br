from biblioteca_br import pib, desemprego, populacao, ibge_ipca

print("=== PIB (2015-2024) ===")
df_pib = pib(inicio="201501", fim="202403")
print(df_pib.tail())

print("\n=== Desemprego (2020-2024) ===")
df_des = desemprego(inicio="202001", fim="202403")
print(df_des.tail())