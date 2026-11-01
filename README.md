# Galerie

Exposition via HTTP d'images

- lien symbolique sur le répertoire `static/images`
- `images.txt` contient le chemin de chaque image depuis le répertoire `static/images`

**Exemple**
```bash
[...]
static/images/Camera/IMG-20230731-WA0014.jpeg
[...]
```

## Installation

> A realiser sur la machine_cible

- cd /tmp
- git clone https://github.com/doali/galerie.git
- cd galerie/static
- ln -s /mnt/HDD10T/Data/OnePlusTS/DCIM images
- find static/images/* >images.txt

### `find`

```bash
find static/images/* -iname "*.jpeg" -o -iname "*.jpg" -o -iname "*.png" | grep -vi system >images.txt
```

> `grep -vi system` pour eviter de recuperer les images : connecteurs, cartes, cables...

> Utiliser le script `gen_img.sh` qui realise cette operation

## Configuration

```
<user>@Host-001 ~ $ cat /etc/hosts 
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

<@ip machine_cible>	galerie
```

### `~/.local/bin`

> Creer des liens symboliques dans le repertoire `~/.local/bin`

```bash
ln -s $PWD/consultation.sh ~/.local/bin/photo_consultation
ln -s $PWD/creation.sh ~/.local/bin/photo_creation
```

### `~/.bashrc`

```bash
alias photo_anne='photo_creation --cat anne $@'
alias photo_cecile='photo_creation --cat cecile $@'
alias photo_jean='photo_creation --cat jean $@'
alias photo_nous='photo_creation --cat nous $@'
alias photo_paysage='photo_creation --cat paysage $@'

function photo_all {
        for p in anne cecile jean nous; do
                photo_creation --cat $p $@
        done
}
```

### `base_img.sh`

Chemin : `galerie/app_photo/scripts/base_img.sh`

> Lancer le script `base_img.sh` pour recuperer les chemins des images (en supprimant les doublons) et ainsi les telecharger

Par exemple pour une categorie *nous*, *janvier*, ... : `base_img nous`, `base_img janvier`, ...

```bash
> cat janvier
nous:static/images/OnePlusTS/WhatsApp_Images/WhatsApp Images/IMG-20240206-WA0004.jpg
maison:static/images/OnePlusTS/WhatsApp_Images/WhatsApp Images/IMG-20240206-WA0004.jpg
anne:static/images/OnePlusTS/WhatsApp_Images/WhatsApp Images/IMG-20240216-WA0004.jpg
cecile:static/images/OnePlusTS/WhatsApp_Images/WhatsApp Images/IMG-20240216-WA0004.jpg
```

```bash
> ./base_img.sh janvier
static/images/OnePlusTS/WhatsApp_Images/WhatsApp Images/IMG-20240206-WA0004.jpg
static/images/OnePlusTS/WhatsApp_Images/WhatsApp Images/IMG-20240216-WA0004.jpg
```

> Permet de supprimer les doublons

## Exécution

### Mode développement

Depuis le répertoire `app_photo` :

```bash
python3 app.py
```

Avec le code actuel :

```python
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
```

Le mode débogage Flask est activé :

- rechargement automatique lors d'une modification du code
- affichage détaillé des exceptions
- redémarrage automatique du processus Flask

Exemple :

```text
* Serving Flask app "app"
* Debug mode: on
* Running on http://0.0.0.0:8000/
* Restarting with stat
* Debugger is active!
```

---

### Mode production

Modifier la fin du fichier `app.py` :

```python
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8000)
```

ou :

```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

Le rechargement automatique et le debugger Flask sont alors désactivés.

Exemple :

```text
* Serving Flask app "app"
* Debug mode: off
* Running on http://0.0.0.0:8000/
```

---

## Exécution avec Screen

`screen` permet de détacher l'application du terminal courant puis de s'y rattacher ultérieurement.

### Lancement

```bash
cd ~/git-github/galerie/app_photo

screen -S galerie
python3 app.py
```

Détacher la session :

```bash
CTRL+a d
```

### Afficher les sessions

```bash
screen -ls
```

Exemple :

```text
There is a screen on:
    12345.galerie    (Detached)
```

### Reprendre la session

```bash
screen -r galerie
```

### Arrêter l'application

Se rattacher à la session :

```bash
screen -r galerie
```

Puis interrompre Flask :

```bash
CTRL+c
```

ou fermer complètement la session :

```bash
exit
```

### Lancement direct en arrière-plan

```bash
screen -dmS galerie python3 app.py
```

---

## Démarrage automatique avec systemd

> Méthode recommandée sur Debian et Raspberry Pi OS.

Créer le fichier :

```bash
sudo vim /etc/systemd/system/galerie.service
```

Contenu :

```ini
[Unit]
Description=Galerie Photo
After=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/git-github/galerie/app_photo
ExecStart=/usr/bin/python3 app.py

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Chargement du service

```bash
sudo systemctl daemon-reload
```

### Démarrage

```bash
sudo systemctl start galerie
```

### Activation au démarrage du Raspberry

```bash
sudo systemctl enable galerie
```

### Vérification du statut

```bash
sudo systemctl status galerie
```

Exemple :

```text
● galerie.service - Galerie Photo
     Loaded: loaded
     Active: active (running)
```

### Consultation des journaux

Afficher l'historique :

```bash
journalctl -u galerie
```

Suivre les messages en temps réel :

```bash
journalctl -fu galerie
```

Exemple :

```text
Nov 01 06:19:31 raspberrypi systemd[1]: Started Galerie Photo.
Nov 01 06:19:32 raspberrypi python3[9602]: * Serving Flask app 'app'
Nov 01 06:19:33 raspberrypi python3[9602]: 192.168.1.21 - - [01/Nov/2026 06:19:33] "GET / HTTP/1.1" 200 -
```

### Redémarrage après modification du code

```bash
sudo systemctl restart galerie
```

### Arrêt du ash
sudo systemctl stop galerie
```

### Désactivation du démarrage automatique

```bash
sudo systemctl disable galerie
```

---

## Exemple d'utilisation

Depuis un navigateur :

```bash
firefox http://galerie:8000
```

![utilisation](app_photo/doc/img/galerie_utilisation.png)

Recherche de toutes les images contenant "vacances" :

```text
vacances
```

Recherche de toutes les images de février 2024 :

```text
202402
```

Recherche via expression régulière :

```text
IMG-2024.*WA
```

Recherche des images WhatsApp :

```text
WhatsApp
```

Par défaut, les résultats sont paginés par groupe de 20 images. Les boutons de navigation permettent d'accéder aux pages suivantes tout en conservant le filtre de recherche.

## Pratique

> Copie de l'ensemble des images /media/blackpc/disk/DCIM/100MSDCF/DSC04523.JPG a /media/blackpc/disk/DCIM/100MSDCF/DSC04543.JPG de la machine blackpc a pi

```bash
/media/blackpc/disk/DCIM/100MSDCF/DSC04538.JPG
/media/blackpc/disk/DCIM/100MSDCF/DSC04539.JPG
/media/blackpc/disk/DCIM/100MSDCF/DSC04540.JPG
/media/blackpc/disk/DCIM/100MSDCF/DSC04541.JPG
/media/blackpc/disk/DCIM/100MSDCF/DSC04542.JPG
/media/blackpc/disk/DCIM/100MSDCF/DSC04543.JPG
blackpc blackpc:/media/blackpc/disk/DCIM/100MSDCF 
> scp $(for i in {4523..4543}; do echo $PWD/DSC0$i.JPG; done) pi@<adresse_pi>:/tmp/photo
pi@<adresse_pi>'s password: 
DSC04523.JPG                                                                                                                                                                                      100% 5568KB   3.7MB/s   00:01    
DSC04524.JPG                                                                                                                                                                                      100% 4896KB   4.7MB/s   00:01    
DSC04525.JPG                                                                                                                                                                                      100% 4992KB   4.7MB/s   00:01    
DSC04526.JPG                                                                                                                                                                                      100% 2720KB   4.6MB/s   00:00    
DSC04527.JPG                                                                                                                                                                                      100% 2560KB   4.4MB/s   00:00    
DSC04528.JPG                                                                                                                                                                                      100% 2496KB   4.2MB/s   00:00    
DSC04529.JPG                                                                                                                                                                                      100% 3264KB   4.3MB/s   00:00    
DSC04530.JPG                          
```
