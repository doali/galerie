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

## Configuration

```
<user>@Host-001 ~ $ cat /etc/hosts 
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

<@ip machine_cible>	galerie
```

## Execution

`python3 /tmp/galerie/app_photo/app.py`

## Utilisation

![utilisation](app_photo/doc/img/galerie_utilisation.png)

`firefox http://galerie:8000`
