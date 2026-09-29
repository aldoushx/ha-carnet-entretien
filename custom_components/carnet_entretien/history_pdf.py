"""Génération du PDF d'export d'un véhicule : page de garde + tableau
chronologique de l'historique d'entretien, suivis en annexe de chaque
facture qui lui est liée (dans l'ordre chronologique des interventions).

Bibliothèques ajoutées aux "requirements" du manifest (installées
automatiquement par Home Assistant au chargement de l'intégration) :
- reportlab : mise en page du corps du document, pure Python, sans
  dépendance système.
- pypdf : fusion des pages (corps + annexes).
- Pillow : conversion des factures photographiées (JPEG/PNG/WebP) en pages
  PDF pour l'annexe — déjà présente dans la plupart des installations HA
  (utilisée par de nombreux autres composants), donc coût d'installation
  généralement nul.

Toutes les fonctions de ce module sont synchrones et bloquantes (E/S
disque, mise en page CPU) : à appeler exclusivement via
`hass.async_add_executor_job`, jamais directement depuis une coroutine.
"""
from __future__ import annotations

import io
import logging
from datetime import datetime
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from homeassistant.core import HomeAssistant
from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

from .invoices import vehicle_invoice_dir

_LOGGER = logging.getLogger(__name__)


def _fmt_date(ts: int | float | None) -> str:
    if not ts:
        return "—"
    return datetime.fromtimestamp(ts).strftime("%d/%m/%Y")


def _fmt_km(km: int | float | None) -> str:
    if km is None:
        return ""
    return f"{int(km):,}".replace(",", " ") + " km"


def _simple_pdf_page(title: str, lines: list[str]) -> bytes:
    """Une page simple (titre + paragraphes) — utilisée pour la page de
    garde et la page de séparation avant les annexes."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=3 * cm, bottomMargin=2 * cm, leftMargin=2 * cm, rightMargin=2 * cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("CarnetTitle", parent=styles["Title"], fontSize=20, spaceAfter=16)
    body_style = ParagraphStyle("CarnetBody", parent=styles["Normal"], fontSize=11, textColor=colors.HexColor("#555555"), spaceAfter=6)
    elements = [Paragraph(title, title_style)]
    for line in lines:
        elements.append(Paragraph(line, body_style))
    doc.build(elements)
    return buf.getvalue()


def _build_body_pdf(vehicle: dict[str, Any]) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, topMargin=2 * cm, bottomMargin=2 * cm, leftMargin=1.5 * cm, rightMargin=1.5 * cm)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("CarnetTitle", parent=styles["Title"], fontSize=20, spaceAfter=4)
    subtitle_style = ParagraphStyle("CarnetSubtitle", parent=styles["Normal"], fontSize=11, textColor=colors.grey, spaceAfter=20)
    cell_style = ParagraphStyle("CarnetCell", parent=styles["Normal"], fontSize=8, leading=10)

    vname = f"{vehicle.get('brand', '')} {vehicle.get('model', '')}".strip() or "Véhicule"
    elements = [Paragraph(f"Carnet d'entretien — {escape(vname)}", title_style)]
    meta_bits = [str(b) for b in (vehicle.get("year"), _fmt_km(vehicle.get("mileage")), vehicle.get("license_plate")) if b]
    elements.append(Paragraph(" · ".join(meta_bits), subtitle_style))

    consumables = [c for c in vehicle.get("consumables", []) if c.get("label") or c.get("value")]
    if consumables:
        elements.append(Paragraph("Références des consommables", styles["Heading3"]))
        ref_data = [[Paragraph(f"<b>{escape(c.get('label', ''))}</b>", cell_style), Paragraph(escape(c.get("value", "")), cell_style)] for c in consumables]
        ref_table = Table(ref_data, colWidths=[5 * cm, 13 * cm])
        ref_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F5F5F5")),
                ]
            )
        )
        elements.append(ref_table)
        elements.append(Paragraph("Historique des interventions", styles["Heading3"]))

    log = sorted(vehicle.get("maintenance_log", []), key=lambda e: e.get("date") or 0)
    if not log:
        elements.append(Paragraph("Aucune intervention enregistrée.", styles["Normal"]))
    else:
        # Uniquement les champs que la carte permet réellement de
        # renseigner (date, km, nom, commentaire) : "garage" et "cost"
        # existent côté service HA (log_maintenance, pour les
        # automatisations) mais n'ont aucun formulaire dans la carte, donc
        # aucun moyen normal de les remplir — les afficher ici laisserait
        # deux colonnes presque toujours vides.
        header = ["Date", "Km", "Intervention", "Commentaire"]
        data: list[list[Any]] = [header]
        for e in log:
            data.append(
                [
                    _fmt_date(e.get("date")),
                    _fmt_km(e.get("km")),
                    Paragraph(escape(e.get("item_name", "") or ""), cell_style),
                    Paragraph(escape(e.get("notes", "") or ""), cell_style),
                ]
            )
        table = Table(data, colWidths=[2.3 * cm, 2.1 * cm, 5.5 * cm, 7 * cm], repeatRows=1)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2B1B12")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTSIZE", (0, 0), (-1, 0), 9),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                    ("TOPPADDING", (0, 0), (-1, 0), 6),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F5F5")]),
                ]
            )
        )
        elements.append(table)

    doc.build(elements)
    return buf.getvalue()


def _invoice_to_pdf_bytes(path: Path, mime: str) -> bytes | None:
    if mime == "application/pdf":
        try:
            return path.read_bytes()
        except OSError:
            return None
    try:
        with Image.open(path) as img:
            rgb = img.convert("RGB")
            out = io.BytesIO()
            rgb.save(out, format="PDF")
            return out.getvalue()
    except Exception:  # fichier image corrompu/illisible : on l'ignore plutôt que de faire échouer tout l'export
        _LOGGER.warning("Facture illisible ignorée dans l'export PDF : %s", path)
        return None


def build_history_pdf(hass: HomeAssistant, vehicle: dict[str, Any], vehicle_id: str, base_dir: str | None = None) -> bytes:
    """Construit le PDF complet : corps (page de garde + tableau
    d'historique), puis, si des factures sont liées à au moins une
    intervention, une page de séparation suivie de chaque facture (dans
    l'ordre chronologique des interventions auxquelles elle est liée),
    convertie en page PDF si besoin.

    base_dir : dossier de factures personnalisé (réglage
    "invoices_base_dir"), voir invoices.py::vehicle_invoice_dir.
    """
    writer = PdfWriter()
    writer.append(PdfReader(io.BytesIO(_build_body_pdf(vehicle))))

    invoices_by_id = {inv["id"]: inv for inv in vehicle.get("invoices", [])}
    log = sorted(vehicle.get("maintenance_log", []), key=lambda e: e.get("date") or 0)
    ordered_invoice_ids: list[str] = []
    seen: set[str] = set()
    for entry in log:
        for inv_id in entry.get("invoice_ids") or []:
            if inv_id not in seen and inv_id in invoices_by_id:
                seen.add(inv_id)
                ordered_invoice_ids.append(inv_id)

    if ordered_invoice_ids:
        directory = vehicle_invoice_dir(hass, vehicle_id, base_dir)
        annex_lines = [f"{len(ordered_invoice_ids)} document(s), dans l'ordre chronologique des interventions."]
        writer.append(PdfReader(io.BytesIO(_simple_pdf_page("Annexe — Factures", annex_lines))))
        for inv_id in ordered_invoice_ids:
            inv = invoices_by_id[inv_id]
            path = directory / inv.get("stored_filename", "")
            if not path.is_file():
                continue
            pdf_bytes = _invoice_to_pdf_bytes(path, inv.get("mime", ""))
            if not pdf_bytes:
                continue
            try:
                writer.append(PdfReader(io.BytesIO(pdf_bytes)))
            except Exception:
                _LOGGER.warning("Facture illisible ignorée dans l'export PDF : %s", path)
                continue

    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()
