import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle


data = pd.read_csv("data.csv")  
X = data[['jenis_produk', 'permintaan', 'stok_bahan', 'mesin_aktif', 'tenaga_kerja']]
y = data['lama_produksi']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestRegressor()
model.fit(X_train, y_train)


with open("model_rf_terbaik.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model baru disimpan dalam versi yang kompatibel.")
