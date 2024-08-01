# Restart-Linux-Service.py

Python script to restart a linux service.

## Getting Started

Ce script Python permet de redémarrer un service spécifique sur une machine Linux.
Il est utile pour les administrateurs système ou les développeurs DevOps qui ont besoin d'automatiser le redémarrage de services.

### Prerequisites

L'utilisation du programme nécessite l'acquisition d'un système d'exploitation Linux : Debian / CentOS / Ubuntu...

Le programme a été conçu avec le language Python (Version 3.11).

## Installing & Using

1- Copiez le programme dans le répertoire de votre choix

2- Ajustez les variables suivantes selon votre situation :

Nom du service à surveiller et à redémarrer :
service_name = "your_service_name"

Adresse e-mail pour l'envoi des logs :
email_recipient = "your_email_recipient"

Adresse e-mail de l'expéditeur :
sender = "your_email_sender"

3- Pour utiliser ce script, exécutez la commande suivante : python3 restart_linux_service.py

4- Vous pouvez appliquer vos propres paramètres en modifiant le script

5- Il est possible d'indiquer plusieurs destinataires pour l'envoi de mail

## Running the tests

Le programme a été conçu dans un environnement de développement intégré(IDE) sur l'OS Windows 11 64Bits.

Le programme a été testé sur l'OS Debian 64bits.

## Versioning

Version 1.0

## Authors

Jean - Samuel BOURGUIT 

Administrateur Infrastuture et Cloud

## License
Copyright 2023 Jean - Samuel BOURGUIT

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

