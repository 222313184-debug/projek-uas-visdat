# Catatan temuan awal (BAHAN, bukan teks final)

Dihitung dari data 2024 dengan config.yaml saat ini (12 variabel, k-means k=4, random_state=1). Periksa ulang
setelah mengubah variabel atau k, lalu tulis interpretasi dengan kata-katamu sendiri.

- PCA: PC1 menjelaskan 29% dan PC2 15% varians.
  PC1 didorong positif oleh telur ayam ras, daging ayam ras, mie, dan gorengan; negatif oleh pisang dan kangkung.
- Klaster sangat terkait wilayah. Hampir semua kab/kota Jawa (107 dari 119) berada di satu klaster dengan konsumsi telur, ayam ras, dan mie di atas rata-rata.
  Klaster kecil (44 kab/kota) hampir seluruhnya di Papua (40 kab/kota): beras dan telur rendah, bayam dan kangkung tinggi.
  Penyebab di balik pola ini (mis. pangan pokok non-beras) TIDAK dapat dibuktikan dari 8 tabel ini; perlu data umbi-umbian atau sumber lain.
- Kesenjangan: beras terendah di Puncak (0,187) dan tertinggi di Manggarai Timur (2,654); rokok kretek filter terendah di Yahukimo (0,232) dan tertinggi di Solok Selatan (32,255) (satuan komoditas BPS).
- Pencilan |z|>4 terutama pada bayam dan pisang (masing-masing 6 kab/kota).

## Komposisi pulau per klaster
| pulau                |   Klaster 1 |   Klaster 2 |   Klaster 3 |   Klaster 4 |
|:---------------------|------------:|------------:|------------:|------------:|
| Bali & Nusa Tenggara |          33 |           0 |           1 |           7 |
| Jawa                 |           5 |           0 |           7 |         107 |
| Kalimantan           |           0 |           0 |          45 |          11 |
| Maluku               |          21 |           0 |           0 |           0 |
| Papua                |           2 |          40 |           0 |           0 |
| Sulawesi             |          44 |           4 |          32 |           1 |
| Sumatera             |          25 |           0 |          83 |          46 |

## Profil klaster (rata-rata z-score)
|                 |   Klaster 1 |   Klaster 2 |   Klaster 3 |   Klaster 4 |
|:----------------|------------:|------------:|------------:|------------:|
| beras           |        0.84 |       -1.25 |        0.21 |       -0.52 |
| terigu          |       -0.6  |       -0.61 |        0.6  |        0.02 |
| telur_ayam_ras  |       -1.02 |       -1.16 |        0.32 |        0.75 |
| susu_kental     |       -0.79 |        0.58 |        0.58 |       -0.11 |
| daging_ayam_ras |       -1.02 |       -0.29 |        0.24 |        0.61 |
| ikan_tongkol    |        0.68 |       -0.7  |       -0.06 |       -0.28 |
| kangkung        |        0.37 |        1.33 |       -0.16 |       -0.46 |
| bayam           |       -0.33 |        1.67 |       -0.15 |       -0.03 |
| pisang          |        0.34 |        0.54 |       -0.06 |       -0.34 |
| rokok_filter    |       -0.45 |       -1    |        1    |       -0.38 |
| gorengan        |       -0.63 |       -1.23 |        0.28 |        0.52 |
| mie             |       -0.71 |       -1.18 |       -0.11 |        0.94 |
