#!/usr/bin/env python3
"""
Real-Time Metrics Pipeline
============================
Practice Project 2: Producer-Consumer Pattern with Queue, Lock, Semaphore, Event

Run: python main.py
"""

from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    console.print(Panel.fit(
        "[bold green]Real-Time Metrics Pipeline[/bold green]\n"
        "Practice Project 2: Producer-Consumer with Queue, Lock, Semaphore, Event",
        border_style="green"
    ))
    console.print()

    try:
        from app import run
        run()
    except NotImplementedError as e:
        console.print(f"[yellow]Not yet implemented:[/yellow] {e}")
    except TypeError as e:
        if "NoneType" in str(e):
            console.print(f"[yellow]A function returned None.[/yellow]")
            console.print(f"[dim]Error: {e}[/dim]")
        else:
            raise

if __name__ == "__main__":
    main()
