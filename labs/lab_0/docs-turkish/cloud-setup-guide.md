# Bulut GPU Kurulum Rehberi: Isaac Sim + Isaac Lab

NVIDIA Isaac Sim 5.1 ve Isaac Lab 2.3.0'i bulut GPU instance'larinda calistirmak icin kapsamli rehber. Docker tabanli pipeline, Vast.ai yapilandirmasi, dogrulama, egitim ve maliyet yonetimini kapsar.

## Icindekiler

- [Genel Bakis](#genel-bakis)
- [On Kosullar](#on-kosullar)
- [Docker Image](#docker-image)
- [Vast.ai Kurulumu](#vastai-kurulumu)
- [Diger Bulut Saglayicilari](#diger-bulut-saglayicilari)
- [On-Start Script](#on-start-script)
- [Dogrulama](#dogrulama)
- [Ilk Egitim](#ilk-egitim)
- [Video Kaydi](#video-kaydi)
- [Veri Kaliciligi ve Yedekleme](#veri-kaliciligi-ve-yedekleme)
- [Maliyet Yonetimi](#maliyet-yonetimi)
- [Sorun Giderme](#sorun-giderme)
- [Bilinen Sorunlar](#bilinen-sorunlar)
- [Ek: Versiyon Matrisi](#ek-versiyon-matrisi)

---

## Genel Bakis

Isaac Sim, render islemi icin RT Core'lara sahip NVIDIA RTX GPU gerektirir. Cogu yerel makinede bu donanim bulunmadigindan bulut GPU instance'lari kullaniyoruz. Bu proje, tum yigini iceren ozel bir Docker image'i kullanir:

```
Docker Image (ozkanceylan/isaacsim-robotics-lab:latest)
├── NVIDIA CUDA 12.8 Runtime (Ubuntu 22.04)
├── Miniconda + Python 3.11 (ortam: isaaclab)
├── Isaac Sim 5.1.0 (NVIDIA PyPI'den pip ile kurulum)
├── Isaac Lab 2.3.0 (kaynak kurulumu, /opt/IsaacLab)
├── PyTorch 2.7.0+cu128
├── RL Games, SKRL (RL frameworkleri)
├── TensorBoard, pytest, matplotlib
└── On-start script: /opt/vastai_onstart.sh
```

Proje kodu image'in icine **dahil edilmez**. Her acilista on-start script araciligiyla GitHub'dan klonlanir, boylece her zaman en son surume sahip olursunuz.

---

## On Kosullar

### Bulut Hesabi

- **Vast.ai:** [vast.ai](https://vast.ai) adresinden hesap olusturun, odeme yontemi ekleyin. Minimum 5$ kredi onerilir.
- **Diger saglayicilar:** NVIDIA RTX GPU ve Docker destegi olan herhangi bir saglayici (Lambda, RunPod, GCP vb.).

### Yerel Makine

- SSH istemcisi (macOS/Linux'ta yerlesik, Windows'ta Git Bash veya WSL)
- Git
- VNC goruntuleyici (istege bagli, GUI erisimi icin) — [TigerVNC](https://tigervnc.org/) veya [RealVNC](https://www.realvnc.com/)
- Kod editoru (VS Code onerilir)

### GPU Gereksinimleri

Isaac Sim, iskin izlemeli render icin **RT Core'lara** sahip NVIDIA GPU gerektirir:

| GPU | RT Core | VRAM | Destekleniyor mu? |
|-----|---------|------|-------------------|
| RTX 4090 | Var | 24 GB | Evet (onerilen) |
| RTX 5090 | Var | 32 GB | Evet (test edildi) |
| RTX A6000 | Var | 48 GB | Evet |
| RTX 3090 | Var | 24 GB | Evet (eski surucu) |
| A100 | Yok | 40/80 GB | **Hayir** |
| H100 | Yok | 80 GB | **Hayir** |
| T4 | Var (sinirli) | 16 GB | Kismi (dusuk VRAM) |

> **Onemli:** A100 ve H100 cok guclu GPU'lar olmasina ragmen RT Core'lari yoktur ve Isaac Sim ile kullanilamazlar.

---

## Docker Image

### Image Detaylari

- **Docker Hub:** `ozkanceylan/isaacsim-robotics-lab:latest`
- **Temel:** `nvidia/cuda:12.8.0-devel-ubuntu22.04`
- **Boyut:** ~15 GB (Docker Hub'da sikistirilmis ~8 GB)
- **Dockerfile:** Proje reposunda `docker/Dockerfile`

### Image'i Yerel Olarak Olusturma

Ozellestirme veya yeniden olusturma gerekiyorsa:

```bash
cd docker/
bash build_and_push.sh              # varsayilan: ozkanceylan/isaacsim-robotics-lab:latest
bash build_and_push.sh kullanici    # ozel Docker Hub kullanicisi
bash build_and_push.sh kullanici v2 # ozel etiket
```

Olusturma sureci:
1. Sistem bagimliklarini kurar (git, curl, VNC araclari, Vulkan vb.)
2. Python 3.11 ile Miniconda'yi kurar
3. NVIDIA PyPI'den Isaac Sim 5.1.0'i kurar
4. Isaac Lab 2.3.0'i kaynaktan klonlar ve yukleyiciyi calistirir
5. `isaaclab` cekirdek paketini kurar (import sorunu icin duzeltme)
6. NVIDIA Omniverse EULA'yi onceden kabul eder
7. CUDA 12.8 destekli PyTorch 2.7.0'i kurar
8. On-start script'i `/opt/vastai_onstart.sh`'a kopyalar

Olusturma suresi: ~30-45 dakika (ag hizina bagli).

---

## Vast.ai Kurulumu

### Adim 1: Hazir Sablonu Kullanin (En Hizli Yol)

1. Sablonu acin: [Isaac Sim Vast.ai Sablonu](https://cloud.vast.ai/?ref_id=460420&creator_id=460420&name=isaacsim)
   - Sablon hash: `e2b4bc434edeb622c212f9966e532815`
2. Sablon asagidakileri onceden yapilandirir:
   - Docker image: `ozkanceylan/isaacsim-robotics-lab:latest`
   - On-start script
   - Onerilen kaynak tahsisleri

### Adim 2: Instance Secimi

Filtreleme kriterleri:

| Kriter | Minimum | Onerilen |
|--------|---------|----------|
| GPU | RTX 4090 (24 GB) | RTX 5090 (32 GB) |
| RAM | 32 GB | 64 GB |
| Disk | 50 GB | 100 GB |
| Yukleme hizi | 100 Mbps | 500 Mbps+ |
| Guvenilirlik | >%95 | >%99 |
| Konum | Herhangi | AB (Avrupa'dan dusuk gecikme) |

### Adim 3: Instance Yapilandirmasi

- **Docker image:** `ozkanceylan/isaacsim-robotics-lab:latest`
- **On-start script:**
  ```
  bash /opt/vastai_onstart.sh
  ```
- **Disk tahsisi:** En az 50 GB (Isaac Sim varliklari buyuktur)
- **Kalici depolama:** Varsa `/data` birimini etkinlestirin

### Adim 4: Baslatma ve Baglanti

```bash
# Instance'a SSH ile baglanin (port ve IP Vast.ai panosundan)
ssh -p <port> root@<host>

# GPU'yu dogrulayin
nvidia-smi

# Conda ortami otomatik olarak aktive edilir
python -c "import torch; print(torch.cuda.is_available())"  # True yazdirmali

# Proje reposu buradadir:
cd /workspace/isaacsim-robotics-lab
```

### Adim 5: Bosta Otomatik Kapatma

Vast.ai panosunda bosta kalma zaman asimini 30 dakikaya ayarlayin. Bu, gereksiz ucretleri onler.

---

## Diger Bulut Saglayicilari

### Genel Docker Kurulumu

Docker + NVIDIA GPU destegi olan herhangi bir saglayici icin:

```bash
# Image'i cekin
docker pull ozkanceylan/isaacsim-robotics-lab:latest

# GPU erisimi ve kalici depolama ile calistirin
docker run -it --gpus all \
  --shm-size=8g \
  -v /host/data:/data \
  -p 6006:6006 \
  -p 6080:6080 \
  ozkanceylan/isaacsim-robotics-lab:latest

# Container icinde
conda activate isaaclab
git clone https://github.com/ozkannceylan/isaacsim-robotics-lab.git /workspace/isaacsim-robotics-lab
cd /workspace/isaacsim-robotics-lab
bash labs/lab_0/scripts/validate_setup.sh
```

### Lambda Cloud

```bash
# SSH ile baglanin, sonra:
docker pull ozkanceylan/isaacsim-robotics-lab:latest
docker run -it --gpus all -v /home/ubuntu/data:/data ozkanceylan/isaacsim-robotics-lab:latest
```

### RunPod

Docker image'i dogrudan RunPod sablon image'i olarak kullanin veya terminal uzerinden cekin.

---

## On-Start Script

On-start script (`docker/vastai_onstart.sh`, image'da `/opt/vastai_onstart.sh`'a kopyalanir) her Vast.ai instance acilisinda otomatik olarak calisir:

1. **Conda aktivasyonu:** `isaaclab` ortamini aktive eder
2. **Proje klonlama/cekme:** GitHub'dan klonlar (veya zaten mevcutsa en son surumu ceker)
3. **Kalici sembolik baglantilar:** `outputs/`, `checkpoints/`, `logs/` dizinlerini `/data/` birimine baglar
4. **Saglik kontrolu:** GPU, Python ve CUDA kullanilabilirligini dogrular

Loglar `/data/onstart.log` dosyasina yazilir.

---

## Dogrulama

### Tam Dogrulama Paketi

```bash
conda activate isaaclab
cd /workspace/isaacsim-robotics-lab
bash labs/lab_0/scripts/validate_setup.sh
```

Dogrulama script'i su kontrolleri yapar:

| # | Kontrol | Ne Dogrulanir |
|---|---------|---------------|
| 1 | GPU Algilama | RT Core'lu RTX GPU, surucu surumu |
| 2 | Python Ortami | Python 3.11, conda veya Docker |
| 3 | Isaac Sim | `import isaacsim` basarili |
| 4 | Isaac Lab | `from isaaclab.app import AppLauncher` basarili |
| 5 | PyTorch | PyTorch surumu, CUDA kullanilabilirligi |
| 6 | Basliksiz Duman Testi | Isaac Sim basliksiz modda hatasiz calisir |
| 7 | RL Frameworkleri | RL Games ve SKRL iceri aktarilabilir |

### Hizli Manuel Kontroller

```bash
# GPU
nvidia-smi

# Python + CUDA
python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA: {torch.cuda.is_available()}, GPU: {torch.cuda.get_device_name(0)}')"

# Isaac Sim
python -c "import isaacsim; print('Isaac Sim OK')"

# Isaac Lab
python -c "from isaaclab.app import AppLauncher; print('Isaac Lab OK')"
```

### Ilk Calistirma Notlari

Bir instance olusturduktan sonra ilk calistirmada:
- **Shader derleme:** Isaac Sim ilk baslatmada GPU shader'larini derler (2-5 dk)
- **Varlik indirme:** Bazi varliklar ilk kullanimda AWS S3'ten indirilir (~10 GB)
- **EULA:** Docker image'da onceden kabul edilmistir

Sonraki calistirmalar cok daha hizlidir (10-30 saniye).

---

## Ilk Egitim

### CartPole (Duman Testi)

```bash
# Hizli test: 50 iterasyon, ~20 saniye
bash /opt/IsaacLab/isaaclab.sh -p \
  /opt/IsaacLab/scripts/reinforcement_learning/rl_games/train.py \
  --task Isaac-Cartpole-v0 --headless --num_envs 512 --max_iterations 50
```

### CartPole (Tam Egitim)

```bash
# Tam egitim: 300 iterasyon, ~2 dakika
bash /opt/IsaacLab/isaaclab.sh -p \
  /opt/IsaacLab/scripts/reinforcement_learning/rl_games/train.py \
  --task Isaac-Cartpole-v0 --headless --num_envs 2048 --max_iterations 300
```

### Ant Yuruyusu

```bash
bash /opt/IsaacLab/isaaclab.sh -p \
  /opt/IsaacLab/scripts/reinforcement_learning/rl_games/train.py \
  --task Isaac-Ant-v0 --headless --num_envs 2048 --max_iterations 500
```

### CartPole Odullerini Anlama

Varsayilan CartPole odul yapisi ceza terimlerine dayanir:
- Hayatta kalma bonusu: +1.0
- Aci cezasi: -1.0
- Araba hizi cezasi: -0.01
- Cubuk hizi cezasi: -0.005
- Sonlanma cezasi: -2.0

**Negatif toplam oduller normaldir.** Ajan ~-1.80'den 0'a dogru ilerler. Sifira yakin deger hedeftir. Detaylar icin TensorBoard'da bireysel odul bilesenlerini kontrol edin.

### `num_envs` Kisitlamalari

RL Games'in CartPole varsayilan yapilandirmasi:
- `minibatch_size: 8192`
- `horizon_length: 16`
- `batch_size = num_envs * horizon_length`

Bu nedenle: `num_envs >= 512` (cunku 512 * 16 = 8192 = minibatch_size).

Daha az ortam kullanmak `AssertionError` hatasina neden olur.

---

## Video Kaydi

### Egitilmis Politikanin Kaydedilmesi

```bash
# Egitimden sonra video kaydı ile oynatma
bash /opt/IsaacLab/isaaclab.sh -p \
  /opt/IsaacLab/scripts/reinforcement_learning/rl_games/play.py \
  --task Isaac-Cartpole-v0 --headless --num_envs 4 \
  --video --video_length 200
```

Videolar egitim log dizininde `videos/play/` altina kaydedilir.

### Ozel Kayit Scriptleri

Proje `labs/lab_0/scripts/` dizininde ozel kayit scriptleri icerir:

```bash
# Sinusoidal kontrol ile tek ortam demosu
bash /opt/IsaacLab/isaaclab.sh -p labs/lab_0/scripts/record_demo.py --headless --enable_cameras

# Rastgele eylemlerle 16 paralel ortam
bash /opt/IsaacLab/isaaclab.sh -p labs/lab_0/scripts/multi_env_demo.py --headless --enable_cameras
```

> **Onemli bayrak:** `--enable_cameras` basliksiz video kaydi icin gereklidir. Omniverse Replicator'u ekran disi render icin etkinlestirir.

---

## Veri Kaliciligi ve Yedekleme

### Kalici Birim (`/data/`)

Vast.ai, instance yeniden baslatmalarini atlatan kalici bir `/data` birimi saglar. On-start script sembolik baglantilar olusturur:

```
/workspace/isaacsim-robotics-lab/outputs/     -> /data/outputs/
/workspace/isaacsim-robotics-lab/checkpoints/ -> /data/checkpoints/
/workspace/isaacsim-robotics-lab/logs/        -> /data/logs/
```

### Yedekleme Stratejisi

```bash
# Bir instance'i durdurmadan once her zaman kod degisikliklerini gonderin
cd /workspace/isaacsim-robotics-lab
git add -A && git commit -m "checkpoint: <aciklama>" && git push

# Buyuk dosyalari (video, checkpoint) yerel makineye indirin
scp -P <port> root@<host>:/data/checkpoints/model.pth ./yerel_yedekler/
scp -P <port> root@<host>:/workspace/isaacsim-robotics-lab/labs/lab_0/media/*.mp4 ./
```

### Veri Akisi

```
Yerel Makine (kod yazma, dokumantasyon)
       │  git push
       v
    GitHub (tek dogru kaynak)
       │  git pull (on-start script ile otomatik)
       v
Bulut Instance (egitim, render)
       │  /data birimi (yeniden baslatmalarda kalici)
       │  scp / git push (kod degisiklikleri icin)
       v
Yerel Makine (analiz, portfolyo)
```

---

## Maliyet Yonetimi

### Fiyatlandirma (Nisan 2026)

| GPU | Vast.ai Spot | Vast.ai On-Demand |
|-----|-------------|-------------------|
| RTX 4090 | $0.20-0.30/saat | $0.35-0.45/saat |
| RTX 5090 | $0.35-0.50/saat | $0.50-0.65/saat |

### Butce Ipuclari

1. **Bosta otomatik kapatma** ayarini Vast.ai panosunda 30 dakikaya ayarlayin
2. **Basliksiz mod** (`--headless`) kullanin — ekran yuku olmaz
3. **Yerel gelistirme:** Kod, yapilandirma ve dokumantasyonu yerel makinede yazin. Instance'a yalnizca calistirma icin baglanin
4. **Toplulestirme:** Bulut oturumlarinizi planlayin. Instance'i baslatin, tum deneyleri calistirin, sonuclari gonderin, instance'i durdurun
5. **Maliyeti izleme:** Vast.ai, panoda canli maliyet gosterir

### Lab Basina Tahmini Maliyet

| Lab | Tahmini Saat | Tahmini Maliyet |
|-----|-------------|----------------|
| Lab 0: Kurulum ve Dogrulama | 2-4 saat | $1-2 |
| Lab 1: RL Temelleri | 8-12 saat | $3-5 |
| Lab 2: Ozel Gorevler | 10-15 saat | $4-6 |
| Lab 3: Sensorler ve Sentetik Veri | 8-12 saat | $3-5 |
| Lab 4: Simden Gerceğe | 10-15 saat | $4-6 |
| **Toplam** | **38-58 saat** | **$15-24** |

---

## Sorun Giderme

### Isaac Sim Import Hatasi

```
ModuleNotFoundError: No module named 'isaaclab.app'
```

Isaac Lab yukleyicisi bazen cekirdek paketi atlar:

```bash
cd /opt/IsaacLab/source/isaaclab
pip install -e . --no-build-isolation
```

### EULA Import Sirasinda Takilma

```
import isaacsim  # giris bekleyerek takilir
```

EULA'yi onceden kabul edin:

```bash
echo 'Y' | python -c "import isaacsim"
```

### Vulkan Surucu Hatasi (RTX 5090)

```
vkCreateInstance failed. Vulkan 1.1 is not supported
```

RTX 5090 Vulkan 1.4 sunar ancak Ubuntu 22.04'te Vulkan yukleyici 1.3'tur. **Bu, basliksiz egitimi veya video kaydini etkilemez.** Guvle bir sekilde yok sayilabilir.

### Yigit Boyutu Dogrulama Hatasi

```
AssertionError: self.batch_size % self.minibatch_size == 0
```

`num_envs` degerini artirin. Varsayilan RL Games yapilandirmasi ile CartPole icin: `num_envs >= 512`.

### Bellek Yetersizligi (OOM)

```
CUDA out of memory
```

`num_envs` degerini azaltin. VRAM'i izleyin:

```bash
watch -n 1 nvidia-smi
```

### Scriptler `invalid option name` ile Basarisiz

```
set: pipefail: invalid option name
```

Kabuk scriptlerinde Windows satir sonlari (`\r\n`). Duzeltme:

```bash
sed -i 's/\r$//' labs/lab_0/scripts/*.sh
```

### Isaac Sim Ilk Calistirmada Yavas

Normaldir. Ilk baslatma shader derler ve AWS S3'ten 10 GB'a kadar varlik indirebilir. 5-10 dakika bekleyin. Sonraki baslatmalar 10-30 saniye surer.

### `isaaclab` Komutu Bulunamadi

Docker image'da `isaaclab.sh` PATH'e eklenmez. Tam yolu kullanin:

```bash
bash /opt/IsaacLab/isaaclab.sh -p <script.py>
```

---

## Bilinen Sorunlar

| Sorun | Durum | Gecici Cozum |
|-------|-------|-------------|
| RTX 5090'da Vulkan 1.4 ICD / 1.3 yukleyici uyumsuzlugu | Acik (upstream) | Basliksiz mod sorunsuz calisir |
| Isaac Sim stdout'u yakalar | Tasarim geregi | Algilama icin dosya isaretcileri veya cikis kodlari kullanin |
| Isaac Lab 3.0 Beta kirici degisiklikler | Kacinilmali | v2.3.0'da kalin |
| NumPy 2.x uyumsuzlugu | Ara sira | `pip install "numpy<2"` |

---

## Ek: Versiyon Matrisi

7 Nisan 2026'da RTX 5090 instance'inda dogrulanmistir:

| Bilesen | Surum |
|---------|-------|
| GPU | NVIDIA GeForce RTX 5090 |
| VRAM | 32 GB |
| NVIDIA Surucu | 570.144 |
| CUDA | 12.8 |
| Python | 3.11.15 |
| PyTorch | 2.7.0+cu128 |
| Isaac Sim | 5.1 |
| Isaac Lab | 2.3.0 |
| RL Games | Dahil |
| SKRL | Dahil |
| TensorBoard | En son |
| imageio | 2.37.0 |
| OpenCV | 4.11.0 |
| MoviePy | 2.1.2 |
| Gymnasium | 1.2.0 |
| IS | Ubuntu 22.04 (Docker) |
