from typing import List
from layalog.models import AnalysisRecord, ErrorIncident

class MarkdownExporter:
    @staticmethod
    def export(record: AnalysisRecord) -> str:
        s = record.stats
        
        # Sort incidents: Critical (3) -> Medium (2) -> Low (1), then by total_occurrences descending
        sorted_incidents: List[ErrorIncident] = sorted(
            record.incidents,
            key=lambda x: (x.gravidade, x.total_occurrences),
            reverse=True
        )

        md = []
        md.append("# Relatório de Análise de Log - LayaLog\n")
        md.append(f"**Arquivo Analisado:** `{record.filename}`  ")
        md.append(f"**Data da Análise:** {record.created_at}  ")
        md.append(f"**Total de Linhas:** {record.total_lines:,}  ".replace(",", "."))
        md.append(f"**Total de Erros Detectados:** {s.total_errors:,}  ".replace(",", "."))
        md.append(f"**Índice de Indisponibilidade Estimado:** {s.unavailability_rate:.1f}%\n")
        md.append("---\n")

        md.append("## 1. Sumário Executivo\n")
        md.append("| Métrica | Valor |")
        md.append("|---|---|")
        md.append(f"| **Erros Críticos (Severidade Alta)** | {s.critical_errors} |")
        md.append(f"| **Erros Médios (Severidade Média)** | {s.medium_errors} |")
        md.append(f"| **Erros Baixos / Avisos** | {s.low_errors} |")
        md.append(f"| **Setor Mais Impactado** | {s.most_affected_department} |")
        md.append(f"| **Impacto em Disponibilidade** | {'Crítico / Alto' if s.unavailability_rate > 30 else 'Moderado / Baixo'} ({s.unavailability_rate:.1f}%) |\n")

        md.append("### Distribuição por Setor")
        for dept, count in sorted(s.department_counts.items(), key=lambda x: x[1], reverse=True):
            pct = (count / s.total_errors * 100) if s.total_errors > 0 else 0
            md.append(f"- **{dept}:** {count} ocorrências ({pct:.1f}%)")
        md.append("\n---\n")

        md.append("## 2. Erros Priorizados por Criticidade\n")

        for idx, inc in enumerate(sorted_incidents, start=1):
            grav_tag = inc.gravidade_label.upper()
            indisp_str = "Sim (Causa indisponibilidade de serviço)" if inc.causa_indisponibilidade else "Não (Degradação pontual sem derrubar o sistema)"
            lines_str = ", ".join(str(l) for l in inc.lines[:10])
            if len(inc.lines) > 10:
                lines_str += f"... (+{len(inc.lines) - 10} outras)"

            md.append(f"### [{grav_tag}] #{idx} - {inc.title}")
            md.append(f"- **Setor Responsável:** {inc.setor}")
            md.append(f"- **Tipo de Falha:** {inc.tipo_falha}")
            md.append(f"- **Gravidade:** {inc.gravidade} / 3 ({inc.gravidade_label})")
            md.append(f"- **Causa Indisponibilidade do Sistema:** {indisp_str}")
            md.append(f"- **Total de Ocorrências:** {inc.total_occurrences} vezes")
            md.append(f"- **Primeira Ocorrência:** Linha {inc.first_seen_line} ({inc.first_seen_time or 'N/D'})")
            md.append(f"- **Linhas no Log:** {lines_str}")
            md.append(f"- **Resumo Técnico:** {inc.technical_summary}\n")

            if inc.sample_raw:
                md.append("#### Trecho do Log / Stacktrace:")
                md.append("```")
                # Truncate sample if too large for clean MD
                sample = inc.sample_raw.strip()
                if len(sample) > 1500:
                    sample = sample[:1500] + "\n... [trecho truncado para o relatório]"
                md.append(sample)
                md.append("```\n")
            md.append("---\n")

        md.append("## 3. Recomendações de Ação\n")
        recs_added = set()
        rec_counter = 1
        for inc in sorted_incidents:
            if inc.recommendation and inc.recommendation not in recs_added:
                md.append(f"{rec_counter}. **{inc.setor} ({inc.tipo_falha}):** {inc.recommendation}")
                recs_added.add(inc.recommendation)
                rec_counter += 1

        if not recs_added:
            md.append("1. Analisar as linhas de erro destacadas no log e aplicar testes de regressão.")

        return "\n".join(md)
