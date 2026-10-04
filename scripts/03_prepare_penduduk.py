"""Tabel BPS 'Jumlah Penduduk menurut Kabupaten/Kota dan Kelompok Umur 2024' -> data/raw/penduduk_kabkota_2024.csv
Catatan format sumber: provinsi ditulis HURUF BESAR diikuti kab/kota-nya; 26 kab/kota Papua muncul dua kali (di provinsi lama dan
provinsi baru) dengan nilai identik -> diduplikasi dengan memeriksa kesamaan nilai. Total nasional dipakai untuk validasi."""
import glob, openpyxl, pandas as pd

F = glob.glob("data/raw/Jumlah_Penduduk_menurut_Kabupaten_Kota_dan_Kelompok_Umur_2024.xlsx")[0]
R = list(openpyxl.load_workbook(F, data_only=True).active.iter_rows(values_only=True))
umur = list(R[2][2:]); assert R[3][1] == "2024"
rows, nasional = [], None
for r in R[4:]:
    if r[0] == "INDONESIA": nasional = int(r[1])
    if r[0].isupper(): continue                                 # baris provinsi/nasional
    rows.append([r[0], int(r[1])] + [int(x) for x in r[2:]])
d = pd.DataFrame(rows, columns=["nama", "penduduk"] + umur)
dup = d[d.nama.duplicated(keep=False)]
assert (dup.groupby("nama").penduduk.nunique() == 1).all(), "duplikat bernilai beda"
d = d.drop_duplicates("nama")

# Nama versi tabel penduduk -> nama di tabel konsumsi
ALIAS = {"Toba Samosir / Toba": "Toba Samosir", "Kep. Seribu": "Kepulauan Seribu", "Kotabaru": "Kota Baru", "Kota Makasar": "Kota Makassar",
         "Mamuju Utara / Pasangkayu": "Mamuju Utara", "Maluku Tenggara Barat / Kepulauan Tanimbar": "Maluku Tenggara Barat"}
d["kabkota"] = d.nama.replace(ALIAS)
ref = pd.read_csv("data/processed/kabkota_multivariat.csv")[["kabkota"]]
assert set(d.kabkota) == set(ref.kabkota), (set(ref.kabkota) ^ set(d.kabkota))
assert len(d) == 514
d["pct_0_14"] = ((d["0-4"] + d["5-9"] + d["10-14"]) / d.penduduk * 100).round(2)
d["pct_65plus"] = ((d["65-69"] + d["70-74"] + d["75+"]) / d.penduduk * 100).round(2)
out = ref.merge(d[["kabkota", "penduduk", "pct_0_14", "pct_65plus"]], on="kabkota", how="left")
out.to_csv("data/raw/penduduk_kabkota_2024.csv", index=False)
s = int(out.penduduk.sum())
print(f"OK: 514 kab/kota; jumlah = {s:,} vs total nasional tabel = {nasional:,} (selisih {nasional - s:,})")
print(out.sort_values("penduduk").iloc[[0, -1]][["kabkota", "penduduk"]].to_string(index=False))
