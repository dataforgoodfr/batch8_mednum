[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/slamer59/batch8_mednum.git/master?urlpath=/proxy/5006/mednumapp)

# batch8_mednum

Développement d'un outil de localisation des zones d'exclusion numérique du territoire national grâce à l'indice de fragilité numérique.
Outil à destination des collectivités et des élus locaux.

## Installation

Cloner et configurer:

```bash
# Récupération du repo git
git clone https://github.com/dataforgoodfr/batch8_mednum.git
cd batch8_mednum
# creation et activation d'un nouvel environnement virtuel
conda create -y --name fragil_num python=3.7

# Installation des dépendances
conda env update --name fragil_num --file environment.yml

# chargement de l'environnement virtuel
conda activate fragil_num

```

# Téléchargement des données

Dans le répertoire principal `batch8_mednum` et après avoir activé l'environnement.

```bash
python -m mednum.data.process all
```

pour mettre en place l'ensemble

ou simplement une seule étape

```bash
python -m mednum.data.process download_geojson
```

# Lancement panel Bokeh

```bash
panel serve dockerize-apps/panel/mednumapp.py
```

# Lancement dockers

<img src="https://www.docker.com/sites/default/files/d8/styles/role_icon/public/2019-07/Moby-logo.png?itok=sYH_JEaJ" alt="drawing" width="200"/>


```bash
cd dockerize-apps
docker-compose up 

```
