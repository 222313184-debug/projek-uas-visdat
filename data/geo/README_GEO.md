# Batas wilayah kab/kota (data pendukung non-BPS)
Berkas: Administrasi_Kabupaten.shp (+ .dbf, .prj, .cpg). Isi: 517 fitur; atribut `sumber` = BPS, `periode` = 2019.
- 3 fitur bukan kab/kota (kdkab = 00: Waduk Kedungombo, Danau Limboto, Danau Toba) dibuang.
- Pembeda kabupaten/kota memakai `kdkab` (>= 71 = kota).
- Batas 2019 (34 provinsi). Provinsi baru Papua (2022) tidak ada di atribut shapefile; provinsi diambil dari tabel BPS 2024.
- Berkas .shx tidak ikut terunggah; GDAL memulihkannya otomatis (SHAPE_RESTORE_SHX=YES, sudah diset di skrip).
- ISI: sumber asli dan tanggal unduh shapefile.
