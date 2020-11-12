# batch8_mednum
Développement d'un outil de localisation des zones d'exclusion numérique du territoire national grâce à l'indice de fragilité numérique.
Outil à destination des collectivités et des élus locaux.



## Installation
Cloner et configurer:

```
# Récupération du repo git
git clone https://github.com/dataforgoodfr/batch8_mednum.git
cd batch8_mednum
# creation et activation d'un nouvel environnement virtuel
conda create -y --name fragil_num python=3.7

# Installation des dépendances
conda install --force-reinstall -y --name fragil_num -c conda-forge --file requirements.txt

# chargement de l'environnement virtuel
conda activate fragil_num

```

# Téléchargement des données
Dans le répertoire principal `batch8_mednum` et après avoir activé l'environnement.

```
python -m mednum.data.download_geojson
```
