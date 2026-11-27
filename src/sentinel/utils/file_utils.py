"""Human-readable file sizes."""
def format_size(size: int) -> str:
    amount=float(size)
    for unit in ("B","KB","MB","GB","TB"):
        if amount < 1024 or unit == "TB": return f"{amount:.1f} {unit}" if unit != "B" else f"{size} B"
        amount/=1024
    return f"{amount:.1f} TB"
