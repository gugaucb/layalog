#!/usr/bin/env python3
"""
Script CLI para validação e inspeção de auditoria do LayaLog.
Permite consultar registros de chamadas ao Laya e visualizar a resposta bruta (raw)
ou o payload completo.

Uso:
  python scripts/inspect_audit.py --last
  python scripts/inspect_audit.py <assinatura_ou_termo>
  python scripts/inspect_audit.py --list
  python scripts/inspect_audit.py --last --full
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_LOG_PATH = Path("logs/laya_audit.jsonl")


def load_audit_records(log_path: Path) -> List[Dict[str, Any]]:
    """Carrega todas as linhas válidas do arquivo de log JSONL."""
    if not log_path.exists():
        return []

    records = []
    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                sys.stderr.write(f"Aviso: linha {line_num} inválida no JSONL: {e}\n")
    return records


def list_records(records: List[Dict[str, Any]], limit: int = 10) -> None:
    """Exibe um resumo dos últimos N registros."""
    if not records:
        print("Nenhum registro de auditoria encontrado.")
        return

    to_show = records[-limit:]
    print(f"\n📋 Últimos {len(to_show)} registros de auditoria (total: {len(records)}):")
    print("-" * 80)
    print(f"{'#':<4} {'TIMESTAMP':<25} {'STATUS':<9} {'PERFIL':<15} {'ASSINATURA'}")
    print("-" * 80)

    start_idx = len(records) - len(to_show) + 1
    for i, r in enumerate(to_show, start=start_idx):
        ts = r.get("timestamp", "-")[:19]
        status = r.get("status", "-")
        profile = (r.get("profile_name") or r.get("profile_id") or "-")[:14]
        sig = r.get("incident_signature", "-")
        status_icon = "🟢" if status == "success" else "🔴"
        print(f"{i:<4} {ts:<25} {status_icon} {status:<7} {profile:<15} {sig}")
    print("-" * 80)
    print("Dica: Use `python scripts/inspect_audit.py <assinatura>` para inspecionar um item.\n")


def find_record(records: List[Dict[str, Any]], query: str) -> Optional[Dict[str, Any]]:
    """Busca um registro por assinatura exata, índice ou correspondência de texto."""
    if not records:
        return None

    # Tenta por índice numérico (1-based)
    if query.isdigit():
        idx = int(query)
        if 1 <= idx <= len(records):
            return records[idx - 1]

    # Tenta por assinatura exata
    for r in reversed(records):
        if r.get("incident_signature") == query:
            return r

    # Tenta por correspondência parcial na assinatura ou mensagem de erro
    query_lower = query.lower()
    for r in reversed(records):
        sig = str(r.get("incident_signature", "")).lower()
        msg = str(r.get("payload_sent", {}).get("state", {}).get("error_message", "")).lower()
        if query_lower in sig or query_lower in msg:
            return r

    return None


def format_output(record: Dict[str, Any], show_full: bool = False) -> str:
    """Formata a saída do registro."""
    if show_full:
        return json.dumps(record, indent=2, ensure_ascii=False)

    # Por padrão, extrai e exibe o raw da resposta do Laya junto com informações essenciais
    raw_prediction = record.get("prediction_received")
    if raw_prediction is None and record.get("status") == "error":
        return json.dumps({
            "status": "error",
            "error": record.get("error"),
            "incident_signature": record.get("incident_signature"),
            "duration_ms": record.get("duration_ms")
        }, indent=2, ensure_ascii=False)

    return json.dumps(raw_prediction, indent=2, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspeciona e valida itens de auditoria e respostas raw do Laya AI."
    )
    parser.add_argument(
        "item",
        nargs="?",
        help="Assinatura, índice ou termo de busca do incidente a inspecionar.",
    )
    parser.add_argument(
        "-l",
        "--last",
        action="store_true",
        help="Inspeciona o último registro gravado.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Lista os registros de auditoria mais recentes.",
    )
    parser.add_argument(
        "-f",
        "--full",
        action="store_true",
        help="Exibe o registro completo (payload enviado + resposta raw + metadados).",
    )
    parser.add_argument(
        "-n",
        "--limit",
        type=int,
        default=10,
        help="Quantidade de registros a listar com --list (padrão: 10).",
    )
    parser.add_argument(
        "-p",
        "--file",
        type=Path,
        default=DEFAULT_LOG_PATH,
        help=f"Caminho do arquivo de auditoria (padrão: {DEFAULT_LOG_PATH}).",
    )

    args = parser.parse_args()

    records = load_audit_records(args.file)

    if args.list:
        list_records(records, limit=args.limit)
        return 0

    if not records:
        print(f"Nenhum registro encontrado no arquivo: {args.file}")
        return 1

    target_record: Optional[Dict[str, Any]] = None

    if args.last or (not args.item and not args.list):
        target_record = records[-1]
    elif args.item:
        target_record = find_record(records, args.item)

    if not target_record:
        print(f"❌ Nenhum registro encontrado para a busca: '{args.item}'")
        return 1

    # Cabeçalho informativo
    sig = target_record.get("incident_signature", "N/A")
    ts = target_record.get("timestamp", "N/A")
    status = target_record.get("status", "N/A")
    duration = target_record.get("duration_ms", 0.0)
    profile = target_record.get("profile_name") or target_record.get("profile_id", "default")

    print(f"\n🔍 [Auditoria Laya] Incidente: {sig}")
    print(f"⏱️  Timestamp: {ts} | Status: {status} ({duration}ms) | Perfil: {profile}")
    if args.full:
        print("📦 Payload Completo (Envio + Resposta):")
    else:
        print("🧠 Resposta Raw do Laya (Prediction):")
    print("-" * 60)
    print(format_output(target_record, show_full=args.full))
    print("-" * 60 + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
