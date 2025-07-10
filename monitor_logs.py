# monitor_logs.py

import json
import time
from core.creator_db import compute_creator_score, get_creator_stats
from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

def display_creator_log(creator_address: str):
    score = compute_creator_score(creator_address)
    stats = get_creator_stats(creator_address)

    if not stats:
        console.print(f"[grey]Créateur inconnu : {creator_address}[/grey]")
        return

    status = "[bold red]RUG ❌[/bold red]" if score < 0.6 else "[bold green]OK ✅[/bold green]"

    table = Table(title=f"📊 Score Créateur : {creator_address[:6]}... ({status})", box=box.SIMPLE)
    table.add_column("Clé", style="cyan", no_wrap=True)
    table.add_column("Valeur", style="white")

    liq_values = stats.get("liquidity_values", [])
    avg_liq = round(sum(liq_values) / max(len(liq_values), 1), 2)

    table.add_row("Score", str(score))
    table.add_row("Total Tokens", str(stats.get("total_created", 0)))
    table.add_row("Rugpulls", str(stats.get("rugged_count", 0)))
    table.add_row("Moy. Liquidité", f"{avg_liq} SOL")
    table.add_row("Créations", str(len(stats.get("created_timestamps", []))))
    table.add_row("Dernier Vu", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.get("last_seen", 0))))

    console.print(table)

if __name__ == "__main__":
    test_creator = input("Adresse du créateur à inspecter : ").strip()
    display_creator_log(test_creator)
