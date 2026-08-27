# Discord Müzik Botu

## Kurulum

### 1. Gerekli Python kütüphanelerini yükle

Terminali aç ve şu komutu çalıştır:

```bash
py -3.11 -m pip install -U discord.py PyNaCl davey yt-dlp requests
```

### 2. FFmpeg'i indir

FFmpeg'i indir ve ZIP dosyasını çıkart.

Klasörün içinde şu dosyaların olduğundan emin ol:

```text
ffmpeg.exe
ffplay.exe
ffprobe.exe
```

Örnek klasör:

```text
C:\Users\shuku\Desktop\ffmpeg-9.0.1-essentials_build\bin
```

### 3. FFmpeg'i test et

Terminale şunu yaz:

```bash
"C:\Users\shuku\Desktop\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe" -version
```

Sürüm bilgisi gelirse FFmpeg düzgün kurulmuştur.

`ffmpeg.exe` dosyasını çift tıklayarak çalıştırmana gerek yok.

### 4. FFmpeg yolunu bot koduna ekle

`bot.py` dosyasında FFmpeg ayarlarının olduğu yere şunu ekle:

```python
FFMPEG_PATH = r"C:\Users\shuku\Desktop\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe"
```

FFmpeg'in konumu farklıysa yolu değiştir.

### 5. Bot klasörüne git

Bot `M7L1` klasöründeyse:

```bash
cd C:\Users\shuku\Desktop\M7L1
```

### 6. Botu çalıştır

```bash
py -3.11 bot.py
```

Bot başarıyla açılırsa terminalde buna benzer bir mesaj görünür:

```text
BotUser olarak giriş yaptık
Bot hazır!
```

## Komutlar

### Genel

```text
,hello
```

Bot selam verir.

```text
,bilgi
```

Rastgele kedi bilgisi gönderir.

```text
,heh 10
```

10 tane `he` gönderir.

### Müzik

Önce bir ses kanalına gir.

```text
,join
```

Bot bulunduğun ses kanalına girer.

```text
,yt ŞARKI ADI
```

Şarkıyı arayıp çalar.

Örnek:

```text
,yt https://www.youtube.com/watch?v=KZscWQdztSw
```

```text
,pause
```

Müziği duraklatır.

```text
,resume
```

Müziği devam ettirir.

```text
,volume 50
```

Sesi %50 yapar.

```text
,stop
```

Müziği durdurur ve bot ses kanalından çıkar.

## Güvenlik

Bot tokenını GitHub, README veya başka herkese açık bir yerde paylaşma.

Token sızarsa Discord Developer Portal üzerinden tokenı yenile.
