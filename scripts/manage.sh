#!/bin/bash
set -e

case "$1" in
  start-normal)
    echo "=== Starting Standard FL Training ==="
    MALICIOUS=false docker compose up -d
    echo ""
    echo "Training started! Follow with: docker compose logs -f"
    echo "Outputs will appear in: ./output/history/ and ./output/plots/"
    ;;
  start-attack)
    echo "=== Starting FL Training with Label-Flip Attacker (Client 4) ==="
    MALICIOUS=true docker compose up -d
    echo ""
    echo "Attack demo started! Follow with: docker compose logs -f"
    echo "Outputs will appear in: ./output/history/ and ./output/plots/"
    ;;
  stop)
    echo "=== Stopping and Wiping Current Run ==="
    docker compose down -v
    echo "Done. All containers and volumes removed."
    ;;
  logs)
    docker compose logs -f $2
    ;;
  output)
    echo "=== Output Locations ==="
    echo "  ./output/history/  — JSON training history"
    echo "  ./output/plots/    — Generated charts"
    echo ""
    echo "To save full logs: docker compose logs > run.log"
    ;;
  *)
    echo "FL Demo Management Script"
    echo ""
    echo "Usage: ./manage.sh <command>"
    echo ""
    echo "Commands:"
    echo "  start-normal   Start standard FL training (5 honest clients)"
    echo "  start-attack   Start FL training with Client 4 as label-flip attacker"
    echo "  stop           Stop everything and wipe all volumes"
    echo "  logs [service] Follow container logs (optionally for a specific service)"
    echo "  output         Show output file locations"
    exit 1
    ;;
esac
