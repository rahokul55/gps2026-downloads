#!/usr/bin/env python3
"""medya/ klasorunu tarar, medya.json dizinini ve kucuk onizlemeleri uretir.

Calistirma: python .github/scripts/medya_index.py
Cikti     : medya/medya.json  +  medya/kucuk/*.webp|jpg

Site galeriyi yalnizca medya.json uzerinden okur; bu dosya elle duzenlenmez.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
MEDYA = KOK / "medya"
GORSEL = MEDYA / "gorsel"
VIDEO = MEDYA / "video"
KUCUK = MEDYA / "kucuk"
DIZIN = MEDYA / "medya.json"
BASLIKLAR = MEDYA / "basliklar.json"

DEPO = os.environ.get("GITHUB_REPOSITORY", "rahokul55/gps2026-downloads")
DAL = os.environ.get("GITHUB_REF_NAME") or "main"
if DAL.startswith("v") or "/" in DAL:
    DAL = "main"
HAM = f"https://raw.githubusercontent.com/{DEPO}/{DAL}"
MEDYA_ETIKET = "medya"

GORSEL_UZANTI = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
VIDEO_UZANTI = {".mp4", ".webm"}
MIME = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".webp": "image/webp", ".gif": "image/gif",
    ".mp4": "video/mp4", ".webm": "video/webm",
}
ONIZLEME_EN = 720


def baslik_uret(ad: str) -> str:
    """kurulum-adim-1.png -> 'Kurulum adim 1'"""
    govde = re.sub(r"^\d{6,}[-_]", "", Path(ad).stem)
    govde = re.sub(r"[-_]+", " ", govde).strip()
    govde = re.sub(r"\s+", " ", govde)
    if not govde:
        return Path(ad).stem
    return govde[0].upper() + govde[1:]


def basliklari_oku() -> dict:
    try:
        veri = json.loads(BASLIKLAR.read_text(encoding="utf-8"))
        return veri if isinstance(veri, dict) else {}
    except (OSError, ValueError):
        return {}


def gorsel_olcu_ve_onizleme(kaynak: Path) -> tuple[int, int, str]:
    """Pillow varsa olcu okur ve webp onizleme uretir."""
    try:
        from PIL import Image
    except ImportError:
        return 0, 0, ""

    try:
        with Image.open(kaynak) as im:
            en, boy = im.size
            if en <= ONIZLEME_EN and kaynak.suffix.lower() == ".webp":
                return en, boy, ""
            kucuk = im.convert("RGB") if im.mode in ("P", "RGBA", "LA") else im.copy()
            kucuk.thumbnail((ONIZLEME_EN, ONIZLEME_EN))
            KUCUK.mkdir(parents=True, exist_ok=True)
            hedef = KUCUK / f"{kaynak.stem}.webp"
            kucuk.save(hedef, "WEBP", quality=76, method=4)
            return en, boy, f"medya/kucuk/{hedef.name}"
    except Exception as hata:  # bozuk dosya dizini bozmasin
        print(f"  ! onizleme uretilemedi: {kaynak.name} ({hata})", file=sys.stderr)
        return 0, 0, ""


def video_onizleme(kaynak: Path) -> str:
    if not shutil.which("ffmpeg"):
        return ""
    KUCUK.mkdir(parents=True, exist_ok=True)
    hedef = KUCUK / f"{kaynak.stem}.jpg"
    komut = [
        "ffmpeg", "-y", "-loglevel", "error", "-ss", "1", "-i", str(kaynak),
        "-frames:v", "1", "-vf", f"scale={ONIZLEME_EN}:-2", str(hedef),
    ]
    try:
        subprocess.run(komut, check=True, timeout=120)
    except Exception:
        return ""
    return f"medya/kucuk/{hedef.name}" if hedef.exists() else ""


def yerel_ogeler(basliklar: dict) -> list[dict]:
    ogeler = []
    for klasor, tur, uzantilar in (
        (GORSEL, "gorsel", GORSEL_UZANTI),
        (VIDEO, "video", VIDEO_UZANTI),
    ):
        if not klasor.is_dir():
            continue
        for dosya in sorted(klasor.iterdir()):
            if not dosya.is_file() or dosya.suffix.lower() not in uzantilar:
                continue
            ustveri = basliklar.get(dosya.name, {})
            if isinstance(ustveri, str):
                ustveri = {"baslik": ustveri}
            yol = f"medya/{'gorsel' if tur == 'gorsel' else 'video'}/{dosya.name}"
            en = boy = 0
            onizleme = ""
            if tur == "gorsel":
                en, boy, onizleme = gorsel_olcu_ve_onizleme(dosya)
            else:
                onizleme = video_onizleme(dosya)
            ogeler.append({
                "ad": dosya.name,
                "tur": tur,
                "baslik": ustveri.get("baslik") or baslik_uret(dosya.name),
                "aciklama": ustveri.get("aciklama", ""),
                "yol": yol,
                "url": f"{HAM}/{yol}",
                "onizleme": f"{HAM}/{onizleme}" if onizleme else "",
                "boyut": dosya.stat().st_size,
                "mime": MIME.get(dosya.suffix.lower(), "application/octet-stream"),
                "en": en,
                "boy": boy,
                "sira": int(ustveri.get("sira", 500)),
                "kaynak": "depo",
            })
    return ogeler


def release_ogeleri(basliklar: dict) -> list[dict]:
    """medya etiketli Release'e yuklenmis buyuk dosyalar da galeriye girer."""
    istek = urllib.request.Request(
        f"https://api.github.com/repos/{DEPO}/releases/tags/{MEDYA_ETIKET}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "gps2026-medya-index",
        },
    )
    jeton = os.environ.get("GITHUB_TOKEN")
    if jeton:
        istek.add_header("Authorization", f"Bearer {jeton}")
    try:
        with urllib.request.urlopen(istek, timeout=20) as yanit:
            surum = json.load(yanit)
    except Exception:
        return []

    ogeler = []
    for varlik in surum.get("assets", []):
        uzanti = Path(varlik["name"]).suffix.lower()
        if uzanti in GORSEL_UZANTI:
            tur = "gorsel"
        elif uzanti in VIDEO_UZANTI:
            tur = "video"
        else:
            continue
        ustveri = basliklar.get(varlik["name"], {})
        if isinstance(ustveri, str):
            ustveri = {"baslik": ustveri}
        ogeler.append({
            "ad": varlik["name"],
            "tur": tur,
            "baslik": ustveri.get("baslik") or baslik_uret(varlik["name"]),
            "aciklama": ustveri.get("aciklama", ""),
            "yol": "",
            "url": varlik["browser_download_url"],
            "onizleme": "",
            "boyut": varlik.get("size", 0),
            "mime": varlik.get("content_type") or MIME.get(uzanti, "application/octet-stream"),
            "en": 0,
            "boy": 0,
            "sira": int(ustveri.get("sira", 600)),
            "kaynak": "release",
        })
    return ogeler


def main() -> int:
    MEDYA.mkdir(parents=True, exist_ok=True)
    GORSEL.mkdir(parents=True, exist_ok=True)
    VIDEO.mkdir(parents=True, exist_ok=True)

    basliklar = basliklari_oku()
    ogeler = yerel_ogeler(basliklar) + release_ogeleri(basliklar)
    ogeler.sort(key=lambda o: (o["sira"], o["tur"] != "video", o["ad"].lower()))

    # artik olmayan dosyalarin onizlemelerini temizle
    gecerli = {Path(o["onizleme"]).name for o in ogeler if o["onizleme"]}
    if KUCUK.is_dir():
        for eski in KUCUK.iterdir():
            if eski.is_file() and eski.name not in gecerli:
                eski.unlink()

    dizin = {
        "surum": 1,
        "depo": DEPO,
        "guncelleme": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "adet": len(ogeler),
        "ogeler": ogeler,
    }

    eski_metin = DIZIN.read_text(encoding="utf-8") if DIZIN.exists() else ""
    try:
        eski = json.loads(eski_metin)
        eski.pop("guncelleme", None)
    except ValueError:
        eski = None
    yeni_karsilastirma = dict(dizin)
    yeni_karsilastirma.pop("guncelleme")
    if eski == yeni_karsilastirma:
        print(f"Dizin guncel ({len(ogeler)} oge), degisiklik yok.")
        return 0

    DIZIN.write_text(
        json.dumps(dizin, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"medya.json yazildi: {len(ogeler)} oge")
    for oge in ogeler:
        print(f"  - [{oge['tur']}] {oge['ad']}  {oge['boyut'] / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
