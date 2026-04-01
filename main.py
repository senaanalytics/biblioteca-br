import bacen

# Selic pelo código
df1 = bacen.serie(codigo=11)
print(df1)

# IPCA pelo código
df2 = bacen.serie(codigo=433)
print(df2)