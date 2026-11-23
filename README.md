# runia0-site

Runia0'nun portföy sitesi — *Ideas into things that work.*
Statik, Türkçe/İngilizce, izleme kodu ve çerez içermeyen site. GitHub Pages üzerinde yayınlanır.

## Yapı

| Yol | İçerik |
|---|---|
| `index.html`, `projeler.html`, `projeler/*.html`, `gizlilik.html` | Türkçe sayfalar |
| `en/index.html`, `en/projects.html`, `en/projects/*.html`, `en/privacy.html` | İngilizce sayfalar |
| `404.html`, `sitemap.xml`, `robots.txt` | GitHub Pages / SEO dosyaları |
| `assets/` | CSS, JS (proje filtresi ve arama), favicon, logo, Open Graph görseli, `covers/` temsilî proje kapakları |
| `tools/content.py` | **Bütün metinler ve proje envanteri burada** |
| `tools/build.py` | HTML, sitemap ve robots dosyalarını üretir |
| `tools/covers.py` | Proje kapaklarını (SVG) üretir |
| `tools/render_images.py` | Favicon PNG'leri ve OG görselini üretir (Playwright) |

## Güncelleme

```bash
# 1) tools/content.py dosyasını düzenle
python3 tools/build.py            # sayfaları yeniden üretir
python3 tools/render_images.py    # yalnızca logo/OG değişirse
```

Üretilen dosyalar da commit edilir; GitHub Pages ek bir derleme adımı olmadan doğrudan repo kökünden yayınlar.

## Yayın

GitHub → **Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)`**.
Adres: `https://runia0.github.io/runia0-site/`

## Özel alan adına geçiş (ör. runia0.dev)

1. Alan adını satın al (`.dev` alan adları yalnızca HTTPS ile çalışır; GitHub Pages bunu sağlar).
2. `tools/content.py` içinde `BASE_URL` değerini `https://runia0.dev/` yap, `python3 tools/build.py` çalıştır.
3. Repo köküne yalnızca `runia0.dev` satırını içeren bir `CNAME` dosyası ekle.
4. DNS'te GitHub'ın dokümanındaki apex `A`/`AAAA` kayıtlarını ve `www` için `runia0.github.io` CNAME kaydını tanımla.
5. Settings → Pages'te alan adını gir, doğrulandıktan sonra **Enforce HTTPS**'i aç.

## Lisans

Kod ve içerik için henüz lisans seçilmedi; tüm haklar saklıdır.
