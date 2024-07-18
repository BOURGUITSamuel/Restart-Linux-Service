#!/usr/bin/python3
# coding=utf-8

import subprocess
import datetime
import time
import logging
import os
import platform

# Emplacement du fichier de log
log_directory = "/var/log/"
log_file = os.path.join(log_directory, 'service_restart.log')

# Configuration du logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# Fonction pour récupérer le hostname du serveur
def get_hostname():
    try:
        hostname = platform.node()
        if not hostname:
            raise ValueError("Le nom de l'hôte est vide.")
        return hostname
    except Exception as e:
        message = f"La récupération du hostname a échoué avec l'erreur: {e}"
        logging.warning(message)
        print(message)
        try:
            uname_info = platform.uname()
            fallback_hostname = f"{uname_info.system}-{uname_info.node}"
            message = f"Nom de l'hôte alternatif récupéré: {fallback_hostname}"
            logging.info(message)
            print(message)
            return fallback_hostname
        except Exception as fallback_error:
            message = f"Échec de la récupération du nom de l'hôte alternatif avec l'erreur: {fallback_error}"
            logging.error(message)
            print(message)
            return "Nom de l'hôte inconnu"

# Fonction pour vérifier si le service est actif
def check_service_running(service_name):
    try:
        result = subprocess.run(["systemctl", "is-active", service_name], text=True, capture_output=True)
        output = result.stdout.strip()

        if result.returncode == 0 and output == "active":
            return True
        else:
            message = f"Le service {service_name} n'est pas actif. Statut actuel: {output}"
            logging.warning(message)
            print(message)
            return False
    except Exception as e:
        message = f"Une erreur inattendue s'est produite lors de la vérification du service {service_name}: {e}"
        logging.error(message)
        print(message)
        return False

# Fonction pour récupérer les statistiques de ressources du service
def get_service_stats(service_name, silent=False):
    stats = []
    try:
        pid_output = subprocess.check_output(['pgrep', '-f', service_name], text=True)
        pids = pid_output.split()
        message = f"PIDs du service {service_name} : {pids}"
        logging.info(message)
        if not silent:
            print(message)

        for pid in pids:
            ps_output = subprocess.check_output(['ps', '-p', pid, '-o', 'pid,%cpu,%mem'], text=True)
            stats.append(ps_output.strip())
            message = f"Statistiques de ressources pour le PID {pid} :\n{ps_output}"
            logging.info(message)
            if not silent:
                print(message)

    except subprocess.CalledProcessError as e:
        message = f"Erreur lors de la récupération des statistiques du service {service_name}: {e}"
        logging.error(message)
        if not silent:
            print(message)

    return "\n".join(stats)

# Fonction pour redémarrer le service
def restart_service(service_name):
    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"{current_time} - Redémarrage du service {service_name} en cours..."
        logging.info(message)
        print(message)

        subprocess.run(["systemctl", "restart", service_name], check=True)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"{current_time} - Le service {service_name} a été redémarré."
        logging.info(message)
        print(message)
    except subprocess.CalledProcessError as e:
        message = f"Erreur lors du redémarrage du service {service_name}: {e}"
        logging.error(message)
        print(message)

# Fonction pour attendre que le service redémarre
def wait_for_service():
    time.sleep(10)

# Fonction pour envoyer le fichier de log par email
def send_log_via_email(sender, email_recipient, service_name):
    subject = f"Rédemarrage du service {service_name} sur le serveur {get_hostname()}"
    stats = get_service_stats(service_name, silent=True)
    body = f"Alerte {get_hostname()}:\n\nVoici les statistiques du service {service_name}:\n\n{stats}\n\nLe fichier de log est en pièce jointe."

    try:
        process = subprocess.Popen(
            ["mailx", "-r", sender, "-s", subject, "-A", log_file, email_recipient],
            stdin=subprocess.PIPE,
            text=True
        )
        process.communicate(body)
        message = f"Le fichier de log a été envoyé à {email_recipient}."
        logging.info(message)
        print(message)
    except subprocess.CalledProcessError as e:
        message = f"Erreur lors de l'envoi du fichier de log à {email_recipient}: {e}"
        logging.error(message)
        print(message)

# Nom du service à vérifier et à redémarrer
service_name = "your_service_name"

# Adresse email pour l'envoi du fichier de log
email_recipient = "your_email_recipient"

# Émetteur du message
sender = "your_email_sender"

# Vérifier si le service est activé , redémarrage du service si celui-ci n'est pas actif
if not check_service_running(service_name):
    message = f"Le service {service_name} est en panne. Redémarrage en cours..."
    print(message)
    logging.info(message)
    try:
        restart_service(service_name)
        wait_for_service()
        if check_service_running(service_name):
            message = f"Le service {service_name} a été redémarré avec succès."
            print(message)
            logging.info(message)
            get_service_stats(service_name)
        else:
            message = f"Le redémarrage du service {service_name} a échoué."
            print(message)
            logging.error(message)
        send_log_via_email(sender, email_recipient, service_name)
    except Exception as e:
        message = f"Erreur lors du redémarrage du service {service_name}."
        print(message)
        logging.error(f"Erreur lors du redémarrage du service {service_name} : {e}")
        send_log_via_email(sender, email_recipient, service_name)
else:
    message = f"Le service {service_name} est en cours d'exécution."
    print(message)
    logging.info(message)
