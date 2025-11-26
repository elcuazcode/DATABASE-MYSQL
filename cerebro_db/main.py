import typer
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import database as db

# Inicializamos la aplicación y la consola
app = typer.Typer()
console = Console()

@app.command()
def recordar(
    persona: str = typer.Argument(..., help="Nombre de la persona o entidad."),
    dato: str = typer.Argument(..., help="El pensamiento, dato o recuerdo."),
    etiquetas: str = typer.Option("", "--tags", "-t", help="Temas separados por coma (ej: 'física, personal').")
):
    """
    Guarda un nuevo pensamiento en la base de datos.
    """
    console.print(f"[bold blue]Procesando...[/bold blue]")
    exito, mensaje = db.guardar_pensamiento(persona, dato, etiquetas)
    
    if exito:
        rprint(f"[bold green]✓ Éxito:[/bold green] {mensaje}")
        rprint(f"   [dim]Persona:[/dim] {persona}")
        rprint(f"   [dim]Tags:[/dim] {etiquetas if etiquetas else 'Ninguna'}")
    else:
        rprint(f"[bold red]✗ Error:[/bold red] {mensaje}")

@app.command()
def asociar(tema: str):
    """
    Busca conexiones neuronales basadas en un TEMA.
    """
    console.print(f"Buscando conexiones para: [bold cyan]'{tema}'[/bold cyan]...")
    resultados = db.buscar_por_tema(tema)
    
    if resultados:
        table = Table(title=f"Asociaciones: {tema.upper()}")
        table.add_column("Persona", style="magenta", justify="left")
        table.add_column("Información", style="white", justify="left")
        
        for persona, info in resultados:
            table.add_row(persona, info)
            
        console.print(table)
    else:
        rprint(f"[yellow]No se encontraron pensamientos vinculados al tema '{tema}'.[/yellow]")

@app.command()
def perfil(nombre: str):
    """
    Muestra todo el conocimiento acumulado sobre una PERSONA.
    """
    console.print(f"Recuperando perfil de: [bold magenta]'{nombre}'[/bold magenta]...")
    resultados = db.obtener_perfil(nombre)
    
    if resultados:
        table = Table(title=f"Expediente: {nombre.upper()}")
        table.add_column("Pensamiento / Dato", style="white")
        table.add_column("Temas Relacionados", style="cyan")
        
        for info, temas in resultados:
            temas_display = temas if temas else "[dim]---[/dim]"
            table.add_row(info, temas_display)
            
        console.print(table)
    else:
        rprint(f"[yellow]No existe información registrada para '{nombre}'.[/yellow]")

if __name__ == "__main__":
    app()