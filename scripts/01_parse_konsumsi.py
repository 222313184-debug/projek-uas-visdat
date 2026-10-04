"""Parse 8 tabel BPS 'Rata-rata Konsumsi Perkapita Seminggu Menurut Kelompok ... Per Kabupaten/kota 2024' (xlsx)
-> data/processed/{konsumsi_long,konsumsi_wide,kabkota_multivariat}.csv + docs/kamus_data.csv

Format sumber: baris 3 = nama komoditas, baris 4 = tahun, baris 5+ = 514 kab/kota; kolom B = penanda kelompok (selalu 0 -> dibuang).
Sel '-' (tidak tercatat) diperlakukan 0 dan ditandai di kolom `strip`. Nilai bertipe teks dikonversi ke angka."""
import glob, re, unicodedata, yaml
import openpyxl, pandas as pd

cfg = yaml.safe_load(open("config.yaml", encoding="utf-8"))

# Urutan baris sumber = urutan kode wilayah. (provinsi, kode, pulau, jumlah kab/kota, kab/kota pertama untuk verifikasi)
PROV = [
 ("Aceh",11,"Sumatera",23,"Simeulue"),("Sumatera Utara",12,"Sumatera",33,"Nias"),("Sumatera Barat",13,"Sumatera",19,"Kepulauan Mentawai"),
 ("Riau",14,"Sumatera",12,"Kuantan Singingi"),("Jambi",15,"Sumatera",11,"Kerinci"),("Sumatera Selatan",16,"Sumatera",17,"Ogan Komering Ulu"),
 ("Bengkulu",17,"Sumatera",10,"Bengkulu Selatan"),("Lampung",18,"Sumatera",15,"Lampung Barat"),("Kep. Bangka Belitung",19,"Sumatera",7,"Bangka"),
 ("Kepulauan Riau",21,"Sumatera",7,"Karimun"),("DKI Jakarta",31,"Jawa",6,"Kepulauan Seribu"),("Jawa Barat",32,"Jawa",27,"Bogor"),
 ("Jawa Tengah",33,"Jawa",35,"Cilacap"),("DI Yogyakarta",34,"Jawa",5,"Kulon Progo"),("Jawa Timur",35,"Jawa",38,"Pacitan"),
 ("Banten",36,"Jawa",8,"Pandeglang"),("Bali",51,"Bali & Nusa Tenggara",9,"Jembrana"),("Nusa Tenggara Barat",52,"Bali & Nusa Tenggara",10,"Lombok Barat"),
 ("Nusa Tenggara Timur",53,"Bali & Nusa Tenggara",22,"Sumba Barat"),("Kalimantan Barat",61,"Kalimantan",14,"Sambas"),
 ("Kalimantan Tengah",62,"Kalimantan",14,"Kotawaringin Barat"),("Kalimantan Selatan",63,"Kalimantan",13,"Tanah Laut"),
 ("Kalimantan Timur",64,"Kalimantan",10,"Paser"),("Kalimantan Utara",65,"Kalimantan",5,"Malinau"),("Sulawesi Utara",71,"Sulawesi",15,"Bolaang Mongondow"),
 ("Sulawesi Tengah",72,"Sulawesi",13,"Banggai Kepulauan"),("Sulawesi Selatan",73,"Sulawesi",24,"Kepulauan Selayar"),
 ("Sulawesi Tenggara",74,"Sulawesi",17,"Buton"),("Gorontalo",75,"Sulawesi",6,"Boalemo"),("Sulawesi Barat",76,"Sulawesi",6,"Majene"),
 ("Maluku",81,"Maluku",11,"Maluku Tenggara Barat"),("Maluku Utara",82,"Maluku",10,"Halmahera Barat"),
 ("Papua Barat",91,"Papua",7,"Fakfak"),("Papua Barat Daya",92,"Papua",6,"Raja Ampat"),("Papua",94,"Papua",9,"Jayapura"),
 ("Papua Selatan",93,"Papua",4,"Merauke"),("Papua Tengah",95,"Papua",8,"Mimika"),("Papua Pegunungan",96,"Papua",8,"Nduga"),
]

def slug(s, n=40):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")[:n]

def baca(path):
    grup = re.search(r"Kelompok_(.*?)_Per_", path).group(1).replace("_", " ")
    R = list(openpyxl.load_workbook(path, data_only=True).active.iter_rows(values_only=True))
    head, yrs, data = R[2], R[3], R[4:]
    assert {y for y in yrs[1:] if y} == {str(cfg["tahun"])}, f"{grup}: tahun tidak sesuai"
    recs = [(r[0], grup, head[j], r[j] == "-", 0.0 if r[j] == "-" else float(r[j]))
            for r in data for j in range(2, len(head))]
    return pd.DataFrame(recs, columns=["kabkota", "grup", "komoditas", "strip", "nilai"])

files = sorted(glob.glob(cfg["raw_glob"]))
assert len(files) == 8, f"Ditemukan {len(files)} file, diharapkan 8"
long = pd.concat([baca(f) for f in files], ignore_index=True)

names = list(dict.fromkeys(long.kabkota))
assert len(names) == 514 and sum(p[3] for p in PROV) == 514
wil, i = [], 0
for prov, kode, pulau, n, first in PROV:
    assert names[i] == first, f"Batas provinsi {prov} tidak cocok: {names[i]} != {first}"
    # "Kota Baru" adalah Kab. Kotabaru (Kalsel), bukan kota
    wil += [(nm, kode, prov, pulau, "Kota" if (nm.startswith("Kota ") and nm != "Kota Baru") else "Kabupaten") for nm in names[i:i + n]]
    i += n
wil = pd.DataFrame(wil, columns=["kabkota", "kode_prov", "provinsi", "pulau", "tipe"])

long["komoditas_id"] = long.grup.map(slug).str[:6] + "__" + long.komoditas.map(slug)
assert long.groupby(["kabkota", "komoditas_id"]).size().max() == 1
long = long.merge(wil, on="kabkota")
long.to_csv("data/processed/konsumsi_long.csv", index=False)

wide = long.pivot(index="kabkota", columns="komoditas_id", values="nilai").reindex(names)
wil.set_index("kabkota").join(wide).reset_index().to_csv("data/processed/konsumsi_wide.csv", index=False)

sel = {}
for k, m in cfg["variabel_multivariat"].items():
    s = long[(long.grup == m["grup"]) & (long.komoditas == m["komoditas"])].set_index("kabkota")
    assert len(s) == 514, f"Komoditas tidak ditemukan: {m}"
    sel[k] = s.nilai
multi = wil.set_index("kabkota").join(pd.DataFrame(sel).reindex(names)).reset_index()
multi.to_csv("data/processed/kabkota_multivariat.csv", index=False)

kamus = (long.groupby(["grup", "komoditas", "komoditas_id"])
         .agg(n_strip=("strip", "sum"), rata2=("nilai", "mean"), sd=("nilai", "std"), maks=("nilai", "max")).round(4).reset_index())
pakai = {(m["grup"], m["komoditas"]) for m in cfg["variabel_multivariat"].values()}
kamus["dipakai_multivariat"] = [(g, k) in pakai for g, k in zip(kamus.grup, kamus.komoditas)]
kamus.to_csv("docs/kamus_data.csv", index=False)

print(f"OK: {len(names)} kab/kota, {long.komoditas_id.nunique()} komoditas, {len(PROV)} provinsi")
print(f"Sel '-' dianggap 0: {int(long.strip.sum())} dari {len(long)} ({long.strip.mean():.1%})")
