"""Cocokkan shapefile batas kab/kota (non-BPS) dengan 514 kab/kota BPS lewat nama + tipe, sederhanakan geometri, simpan GeoJSON.
Output: data/processed/kabkota.geojson (properti: kabkota, provinsi, lon, lat), data/processed/provinsi.geojson,
        docs/geo_tak_cocok.csv (kosong bila semua cocok). Perbaikan nama manual: data/geo/alias_nama.csv (nama_geojson,kabkota)."""
import os, re, unicodedata, yaml
os.environ.setdefault("SHAPE_RESTORE_SHX", "YES")      # .shx tidak ada di zip asli -> dipulihkan GDAL
import geopandas as gpd, pandas as pd
from shapely.geometry import MultiPolygon, Polygon
from shapely.geometry.polygon import orient

cfg = yaml.safe_load(open("config.yaml", encoding="utf-8")); G = cfg["geo"]
bps = pd.read_csv("data/processed/kabkota_multivariat.csv")[["kabkota", "provinsi", "pulau", "tipe"]]

def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().strip()
    s = re.sub(r"^(kota|kab\.?|kabupaten)\s+", "", s)
    return re.sub(r"[^a-z0-9]", "", s)            # 'B A T A M' -> 'batam'

gdf = gpd.read_file(G["file"])
n0 = len(gdf)
gdf = gdf[gdf[G["prop_kdkab"]].astype(int) > 0].copy()           # buang waduk/danau
print(f"Fitur shapefile: {n0} -> {len(gdf)} setelah membuang non-kab/kota")

alias = {}
if os.path.exists("data/geo/alias_nama.csv"):
    a = pd.read_csv("data/geo/alias_nama.csv"); alias = dict(zip(a.nama_geojson, a.kabkota))
gdf["_nama"] = gdf[G["prop_nama"]].map(lambda x: alias.get(x, x))
gdf["_tipe"] = gdf[G["prop_kdkab"]].astype(int).map(lambda k: "Kota" if k >= 71 else "Kabupaten")
gdf["_key"] = gdf["_nama"].map(norm) + "|" + gdf["_tipe"]
bps["_key"] = bps.kabkota.map(norm) + "|" + bps.tipe
assert not gdf._key.duplicated().any() and not bps._key.duplicated().any(), "kunci ganda"

m = gdf[["_key", "geometry"]].merge(bps, on="_key", how="inner")
tak_g = gdf[~gdf._key.isin(bps._key)][[G["prop_nama"], "_tipe"]].rename(columns={G["prop_nama"]: "nama", "_tipe": "tipe"}).assign(sisi="shapefile")
tak_b = bps[~bps._key.isin(gdf._key)][["kabkota", "tipe"]].rename(columns={"kabkota": "nama"}).assign(sisi="BPS")
pd.concat([tak_g, tak_b]).to_csv("docs/geo_tak_cocok.csv", index=False)
print(f"Cocok: {len(m)}/514 | tak cocok shapefile: {len(tak_g)} | tak cocok BPS: {len(tak_b)}")
assert len(m) == 514, "Periksa docs/geo_tak_cocok.csv dan tambahkan baris di data/geo/alias_nama.csv"

m = gpd.GeoDataFrame(m, crs=gdf.crs).to_crs(4326)
try:    # simplifikasi menjaga batas bersama antar-poligon (tanpa celah/tumpang tindih)
    m["geometry"] = m.geometry.simplify_coverage(0.008)
except Exception as e:
    print("simplify_coverage tidak tersedia, pakai simplify biasa:", type(e).__name__)
    m["geometry"] = m.geometry.simplify(0.008, preserve_topology=True)
def putar(g):
    """Plotly (d3-geo) memakai poligon sferis: cincin luar harus searah jarum jam, lubang berlawanan. Satu poligon terbalik saja
    membuat SELURUH peta terisi warna, jadi arah diseragamkan untuk semua poligon (shapefile/simplifikasi bisa mencampur arah)."""
    if g.geom_type == "Polygon": return orient(g, sign=-1.0)
    return MultiPolygon([orient(p, sign=-1.0) for p in g.geoms])
m["geometry"] = m.geometry.map(putar)
c = m.geometry.representative_point(); m["lon"], m["lat"] = c.x.round(3), c.y.round(3)
m[["kabkota", "provinsi", "lon", "lat", "geometry"]].to_file("data/processed/kabkota.geojson", driver="GeoJSON", COORDINATE_PRECISION=3)
pv = m.dissolve(by="provinsi", as_index=False)[["provinsi", "geometry"]]
pv["geometry"] = pv.geometry.map(putar)
pv.to_file("data/processed/provinsi.geojson", driver="GeoJSON", COORDINATE_PRECISION=3)
for f in ("kabkota", "provinsi"): print(f"{f}.geojson: {os.path.getsize(f'data/processed/{f}.geojson')/1e6:.1f} MB")
