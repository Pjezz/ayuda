import pandas as pd

df = pd.read_csv("export.csv")

def get_recommendations(brand, budget, transmission, types):
    # Filtrar por los valores seleccionados
    filtered = df.copy()

    if brand:
        filtered = filtered[filtered["marca"].str.lower() == brand.lower()]

    if budget:
        filtered = filtered[filtered["precio"] <= float(budget)]

    if transmission:
        filtered = filtered[filtered["transmision"].str.lower() == transmission.lower()]

    if types:
        filtered = filtered[filtered["tipo"].str.lower().isin([t.lower() for t in types])]

    results = filtered.to_dict(orient="records")
    return results