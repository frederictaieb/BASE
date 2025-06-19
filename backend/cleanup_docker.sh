#!/bin/bash

echo "⚠️ ATTENTION : Ce script va supprimer tous les conteneurs, images, volumes et réseaux non utilisés !"

# Supprimer tous les conteneurs (même arrêtés)
docker rm -f $(docker ps -aq) 2>/dev/null

# Supprimer toutes les images
docker rmi -f $(docker images -aq) 2>/dev/null

# Supprimer tous les volumes
docker volume rm $(docker volume ls -q) 2>/dev/null

# Supprimer tous les réseaux créés manuellement (sauf les par défaut)
docker network rm $(docker network ls | grep "bridge\|host\|none" -v | awk '{print $1}') 2>/dev/null

# Nettoyage final
docker system prune -a --volumes -f

echo "✅ Docker nettoyé."
