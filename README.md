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

## Execution

`python3 /tmp/galerie/app_photo/app.py`

## Utilisation

![utilisation](app_photo/doc/img/galerie_utilisation.png)

`firefox http://galerie:8000`

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