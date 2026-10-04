# Checklist UAS (topik: multivariat + geospasial + hierarki)
## Data
- [ ] 9 tabel BPS (8 konsumsi + penduduk) tercatat di data/SUMBER_DATA.csv (URL + tanggal akses diisi)
- [x] Penduduk kab/kota 2024 (BPS) diolah: `python scripts/03_prepare_penduduk.py`
- [x] Shapefile kab/kota dicocokkan: `python scripts/02_prepare_geo.py` -> 514/514 (3 alias di data/geo/alias_nama.csv)
- [ ] Catat sumber asli shapefile di data/geo/README_GEO.md dan SUMBER_DATA.csv
- [ ] data/processed/ ikut di-commit ke GitHub (dipakai saat deploy)
## Syarat topik
- [ ] Multivariat: >=8 variabel (ada 12), >=34 unit (514), PCA + parallel coordinates + heatmap, brushing-linking, interpretasi klaster & pencilan
- [ ] Geospasial: 514 kab/kota, 2 jenis peta (choropleth + simbol proporsional), klasifikasi & palet dijustifikasi, tooltip, legenda, zoom/pan, kontrol layer
- [ ] Hierarki: >=3 level (Indonesia>Pulau>Provinsi>Kab/kota), treemap + sunburst, ukuran=penduduk, warna=konsumsi, breadcrumb
## Umum
- [ ] "Sumber: BPS" di setiap visual; judul, legenda, satuan jelas
- [ ] Dicek di ponsel; palet ramah buta warna
- [ ] Situs publik tanpa login + repo publik + README
- [ ] Makalah IEEE 6-8 hal, >=10 referensi (>=3 jurnal/konferensi internasional), URL situs & repo setelah Kesimpulan
- [ ] Abstrak <=200 kata + kata kunci; deklarasi AI di Metodologi
- [ ] kelas_nim_nama.pdf diunggah ke https://s.stis.ac.id/UAS-Visdat-2026 + hardcopy
