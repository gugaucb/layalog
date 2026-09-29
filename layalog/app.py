import os
import uuid
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Response, Query, Body
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json

from layalog.models import AnalysisRecord, LogStats, ErrorIncident, GravityProfile, ProfileSnapshot
from layalog.parser import LogParser
from layalog.classifier import LayaClassifier
from layalog.exporter import MarkdownExporter
from layalog.profiles import get_default_profile
from layalog.database import (
    init_db,
    save_analysis,
    list_analyses,
    get_analysis,
    get_analysis_lines,
    delete_analysis,
    list_profiles,
    get_profile,
    save_profile,
    delete_profile
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("layalog")

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    global classifier_instance
    init_db()
    logger.info("Initializing Laya classifier...")
    try:
        classifier_instance = LayaClassifier(preload=True)
    except Exception as e:
        logger.error(f"Erro ao inicializar LayaClassifier no lifespan: {e}")
    yield

app = FastAPI(title="LayaLog API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier_instance: Optional[LayaClassifier] = None
STATIC_DIR = Path(__file__).parent / "static"
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def get_classifier() -> LayaClassifier:
    global classifier_instance
    if classifier_instance is None:
        classifier_instance = LayaClassifier(preload=True)
    return classifier_instance

@app.get("/v2")
def serve_v2():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/", status_code=307)

@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "laya_initialized": classifier_instance is not None and classifier_instance.initialized
    }

# ================= PROFILES API =================

@app.get("/api/profiles", response_model=List[GravityProfile])
def get_all_profiles():
    return list_profiles()

@app.get("/api/profiles/{profile_id}", response_model=GravityProfile)
def get_single_profile(profile_id: str):
    profile = get_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    return profile

@app.post("/api/profiles", status_code=201, response_model=GravityProfile)
def create_profile(profile_in: GravityProfile):
    if not profile_in.name.strip():
        raise HTTPException(status_code=422, detail="Nome do perfil é obrigatório.")
    if not profile_in.criteria_baixa.strip() or not profile_in.criteria_media.strip() or not profile_in.criteria_critica.strip():
        raise HTTPException(status_code=422, detail="Os 3 critérios de gravidade (Baixa, Média, Crítica) são obrigatórios.")
    
    if not profile_in.id or profile_in.id.strip() == "":
        profile_in.id = f"custom-{uuid.uuid4().hex[:8]}"
    
    # Force custom profile
    profile_in.is_builtin = False
    return save_profile(profile_in)

@app.put("/api/profiles/{profile_id}", response_model=GravityProfile)
def update_profile(profile_id: str, profile_in: Dict[str, Any] = Body(...)):
    existing = get_profile(profile_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    if existing.is_builtin:
        raise HTTPException(status_code=400, detail="Perfis nativos (Built-in) não podem ser alterados diretamente. Utilize a opção Clonar.")
    
    name = profile_in.get("name", existing.name).strip()
    if not name:
        raise HTTPException(status_code=422, detail="Nome do perfil é obrigatório.")
    
    baixa = profile_in.get("criteria_baixa", existing.criteria_baixa).strip()
    media = profile_in.get("criteria_media", existing.criteria_media).strip()
    critica = profile_in.get("criteria_critica", existing.criteria_critica).strip()
    
    if not baixa or not media or not critica:
        raise HTTPException(status_code=422, detail="Os 3 critérios de gravidade são obrigatórios.")
    
    existing.name = name
    existing.description = profile_in.get("description", existing.description)
    existing.system_context = profile_in.get("system_context", existing.system_context)
    existing.criteria_baixa = baixa
    existing.criteria_media = media
    existing.criteria_critica = critica
    
    return save_profile(existing)

@app.post("/api/profiles/{profile_id}/clone", status_code=201, response_model=GravityProfile)
def clone_profile(profile_id: str, payload: Dict[str, Any] = Body(default={})):
    source = get_profile(profile_id)
    if not source:
        raise HTTPException(status_code=404, detail="Perfil de origem não encontrado.")
    
    new_name = payload.get("name") or f"{source.name} (Cópia)"
    new_id = f"custom-{uuid.uuid4().hex[:8]}"
    
    cloned = GravityProfile(
        id=new_id,
        name=new_name,
        description=source.description,
        system_context=source.system_context,
        criteria_baixa=source.criteria_baixa,
        criteria_media=source.criteria_media,
        criteria_critica=source.criteria_critica,
        is_builtin=False
    )
    return save_profile(cloned)

@app.delete("/api/profiles/{profile_id}")
def remove_profile(profile_id: str):
    existing = get_profile(profile_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    if existing.is_builtin:
        raise HTTPException(status_code=400, detail="Não é permitido excluir perfis nativos (Built-in).")
    
    try:
        delete_profile(profile_id)
        return {"status": "deleted", "id": profile_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ================= ANALYSES API =================

@app.get("/api/analyses")
def get_analyses_history():
    return list_analyses(limit=50)

@app.get("/api/analyses/{analysis_id}")
def get_analysis_detail(analysis_id: str):
    data = get_analysis(analysis_id, include_raw=False)
    if not data:
        raise HTTPException(status_code=404, detail="Análise não encontrada.")
    return data

@app.get("/api/analyses/{analysis_id}/lines")
def get_lines_chunk(
    analysis_id: str,
    start_line: int = Query(1, ge=1, description="Linha inicial (1-indexed)"),
    limit: int = Query(200, ge=1, le=1000, description="Quantidade de linhas a retornar")
):
    chunk_data = get_analysis_lines(analysis_id, start_line=start_line, limit=limit)
    if not chunk_data:
        raise HTTPException(status_code=404, detail="Análise não encontrada.")
    return chunk_data

@app.delete("/api/analyses/{analysis_id}")
def remove_analysis(analysis_id: str):
    success = delete_analysis(analysis_id)
    if not success:
        raise HTTPException(status_code=404, detail="Análise não encontrada para exclusão.")
    return {"status": "deleted", "id": analysis_id}

@app.get("/api/analyses/{analysis_id}/export-md")
def export_analysis_md(analysis_id: str):
    data = get_analysis(analysis_id, include_raw=True)
    if not data:
        raise HTTPException(status_code=404, detail="Análise não encontrada.")

    stats = LogStats(**data["stats"])
    incidents = [ErrorIncident(**inc) for inc in data["incidents"]]
    snapshot = ProfileSnapshot(**data["profile_snapshot"]) if data.get("profile_snapshot") else None
    
    record = AnalysisRecord(
        id=data["id"],
        filename=data["filename"],
        created_at=data["created_at"],
        total_lines=data["total_lines"],
        stats=stats,
        incidents=incidents,
        profile_id=data.get("profile_id"),
        profile_snapshot=snapshot
    )
    md_content = MarkdownExporter.export(record)
    
    filename = f"analise_{Path(data['filename']).stem}_{record.id[:8]}.md"
    return Response(
        content=md_content,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

@app.post("/api/analyze-stream")
async def analyze_log_file_stream(
    file: UploadFile = File(...),
    profile_id: Optional[str] = Form(None)
):
    filename = file.filename or "uploaded_log.txt"
    content_bytes = await file.read()

    # Resolve gravity profile
    active_profile = None
    if profile_id:
        active_profile = get_profile(profile_id)
    if not active_profile:
        active_profile = get_default_profile()

    snapshot = ProfileSnapshot(
        profile_id=active_profile.id,
        profile_name=active_profile.name,
        system_context=active_profile.system_context or "",
        criteria_baixa=active_profile.criteria_baixa,
        criteria_media=active_profile.criteria_media,
        criteria_critica=active_profile.criteria_critica
    )

    def event_stream():
        try:
            yield json.dumps({
                "type": "progress",
                "percent": 5,
                "message": f"Iniciando decodificação com perfil: {active_profile.name}..."
            }) + "\n"

            try:
                content = content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                content = content_bytes.decode("latin-1", errors="replace")

            yield json.dumps({
                "type": "progress",
                "percent": 10,
                "message": "Efetuando parsing e identificação de blocos de log..."
            }) + "\n"

            parser = LogParser()
            blocks, total_lines = parser.parse_text(content)

            yield json.dumps({
                "type": "progress",
                "percent": 20,
                "message": f"Parsing concluído ({total_lines:,} linhas). Agrupando incidentes por assinatura...".replace(",", ".")
            }) + "\n"

            grouped = parser.group_incidents(blocks)
            total_groups = len(grouped)
            total_error_count = sum(g["occurrences"] for g in grouped.values())

            yield json.dumps({
                "type": "progress",
                "percent": 25,
                "message": f"Agrupamento concluído: {total_groups} incidentes únicos consolidados a partir de {total_error_count} erros. Avaliando com Laya AI...",
                "current": 0,
                "total": total_groups
            }) + "\n"

            classifier = get_classifier()
            incidents: List[ErrorIncident] = []

            critical_count = 0
            medium_count = 0
            low_count = 0
            unavailability_count = 0

            dept_counts: Dict[str, int] = {}
            severity_counts: Dict[str, int] = {"Crítica": 0, "Média": 0, "Baixa": 0}
            failure_type_counts: Dict[str, int] = {}

            for idx, (sig, group_data) in enumerate(grouped.items()):
                # Classify with active profile
                try:
                    inc = classifier.classify_incident(group_data, profile=active_profile)
                except TypeError:
                    inc = classifier.classify_incident(group_data)
                incidents.append(inc)

                occ = inc.total_occurrences
                if inc.gravidade == 3:
                    critical_count += occ
                    severity_counts["Crítica"] += occ
                elif inc.gravidade == 2:
                    medium_count += occ
                    severity_counts["Média"] += occ
                else:
                    low_count += occ
                    severity_counts["Baixa"] += occ

                if inc.causa_indisponibilidade:
                    unavailability_count += occ

                dept_counts[inc.setor] = dept_counts.get(inc.setor, 0) + occ
                failure_type_counts[inc.tipo_falha] = failure_type_counts.get(inc.tipo_falha, 0) + occ

                # Calculate progress from 25% to 90%
                pct = int(25 + ((idx + 1) / total_groups) * 65) if total_groups > 0 else 90
                short_msg = inc.title[:55]
                yield json.dumps({
                    "type": "progress",
                    "percent": pct,
                    "message": f"Avaliando padrão único {idx + 1} de {total_groups} ({occ} ocorrências): {short_msg}...",
                    "current": idx + 1,
                    "total": total_groups
                }) + "\n"

            # Sort incidents
            incidents.sort(key=lambda x: (x.gravidade, x.total_occurrences), reverse=True)

            most_affected = "Nenhum"
            if dept_counts:
                most_affected = max(dept_counts.items(), key=lambda x: x[1])[0]

            unavail_rate = (unavailability_count / total_error_count * 100.0) if total_error_count > 0 else 0.0

            stats = LogStats(
                total_lines=total_lines,
                total_errors=total_error_count,
                unique_errors=len(incidents),
                critical_errors=critical_count,
                medium_errors=medium_count,
                low_errors=low_count,
                unavailability_rate=round(unavail_rate, 1),
                most_affected_department=most_affected,
                department_counts=dept_counts,
                severity_counts=severity_counts,
                failure_type_counts=failure_type_counts
            )

            yield json.dumps({
                "type": "progress",
                "percent": 95,
                "message": "Gravando análise no banco e compilando métricas..."
            }) + "\n"

            analysis_id = str(uuid.uuid4())
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Save physical log file in uploads/
            safe_fname = "".join(c for c in filename if c.isalnum() or c in "._- ")
            saved_file_path = UPLOAD_DIR / f"{analysis_id}_{safe_fname}"
            try:
                saved_file_path.write_bytes(content_bytes)
            except Exception as fe:
                logger.warning(f"Não foi possível salvar arquivo físico em uploads/: {fe}")

            record = AnalysisRecord(
                id=analysis_id,
                filename=filename,
                created_at=created_at,
                total_lines=total_lines,
                stats=stats,
                incidents=incidents,
                profile_id=active_profile.id,
                profile_snapshot=snapshot
            )

            save_analysis(record, raw_text=content, file_path=str(saved_file_path))

            yield json.dumps({
                "type": "progress",
                "percent": 100,
                "message": "Análise concluída com sucesso!"
            }) + "\n"

            yield json.dumps({
                "type": "complete",
                "data": {
                    "id": record.id,
                    "filename": record.filename,
                    "created_at": record.created_at,
                    "total_lines": record.total_lines,
                    "stats": record.stats.model_dump(),
                    "incidents": [inc.model_dump() for inc in record.incidents],
                    "profile_id": record.profile_id,
                    "profile_snapshot": snapshot.model_dump(),
                    "raw_log_text": None
                }
            }) + "\n"

        except Exception as e:
            logger.exception("Erro durante stream de análise")
            yield json.dumps({
                "type": "error",
                "message": str(e)
            }) + "\n"

    return StreamingResponse(event_stream(), media_type="application/x-ndjson")

@app.post("/api/analyze")
async def analyze_log_file(
    file: UploadFile = File(...),
    profile_id: Optional[str] = Form(None)
):
    try:
        content_bytes = await file.read()
        try:
            content = content_bytes.decode("utf-8")
        except UnicodeDecodeError:
            content = content_bytes.decode("latin-1", errors="replace")

        filename = file.filename or "uploaded_log.txt"
        
        # Resolve profile
        active_profile = None
        if profile_id:
            active_profile = get_profile(profile_id)
        if not active_profile:
            active_profile = get_default_profile()

        snapshot = ProfileSnapshot(
            profile_id=active_profile.id,
            profile_name=active_profile.name,
            system_context=active_profile.system_context or "",
            criteria_baixa=active_profile.criteria_baixa,
            criteria_media=active_profile.criteria_media,
            criteria_critica=active_profile.criteria_critica
        )

        parser = LogParser()
        blocks, total_lines = parser.parse_text(content)
        grouped = parser.group_incidents(blocks)

        classifier = get_classifier()
        incidents: List[ErrorIncident] = []

        total_error_count = sum(g["occurrences"] for g in grouped.values())
        critical_count = 0
        medium_count = 0
        low_count = 0
        unavailability_count = 0

        dept_counts: Dict[str, int] = {}
        severity_counts: Dict[str, int] = {"Crítica": 0, "Média": 0, "Baixa": 0}
        failure_type_counts: Dict[str, int] = {}

        for sig, group_data in grouped.items():
            try:
                inc = classifier.classify_incident(group_data, profile=active_profile)
            except TypeError:
                inc = classifier.classify_incident(group_data)
            incidents.append(inc)

            occ = inc.total_occurrences
            if inc.gravidade == 3:
                critical_count += occ
                severity_counts["Crítica"] += occ
            elif inc.gravidade == 2:
                medium_count += occ
                severity_counts["Média"] += occ
            else:
                low_count += occ
                severity_counts["Baixa"] += occ

            if inc.causa_indisponibilidade:
                unavailability_count += occ

            dept_counts[inc.setor] = dept_counts.get(inc.setor, 0) + occ
            failure_type_counts[inc.tipo_falha] = failure_type_counts.get(inc.tipo_falha, 0) + occ

        # Sort incidents: Critical (3) -> Medium (2) -> Low (1), then occurrences desc
        incidents.sort(key=lambda x: (x.gravidade, x.total_occurrences), reverse=True)

        # Most affected department
        most_affected = "Nenhum"
        if dept_counts:
            most_affected = max(dept_counts.items(), key=lambda x: x[1])[0]

        unavail_rate = (unavailability_count / total_error_count * 100.0) if total_error_count > 0 else 0.0

        stats = LogStats(
            total_lines=total_lines,
            total_errors=total_error_count,
            unique_errors=len(incidents),
            critical_errors=critical_count,
            medium_errors=medium_count,
            low_errors=low_count,
            unavailability_rate=round(unavail_rate, 1),
            most_affected_department=most_affected,
            department_counts=dept_counts,
            severity_counts=severity_counts,
            failure_type_counts=failure_type_counts
        )

        analysis_id = str(uuid.uuid4())
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        safe_fname = "".join(c for c in filename if c.isalnum() or c in "._- ")
        saved_file_path = UPLOAD_DIR / f"{analysis_id}_{safe_fname}"
        try:
            saved_file_path.write_bytes(content_bytes)
        except Exception as fe:
            logger.warning(f"Não foi possível salvar arquivo físico em uploads/: {fe}")

        record = AnalysisRecord(
            id=analysis_id,
            filename=filename,
            created_at=created_at,
            total_lines=total_lines,
            stats=stats,
            incidents=incidents,
            profile_id=active_profile.id,
            profile_snapshot=snapshot
        )

        save_analysis(record, raw_text=content, file_path=str(saved_file_path))

        return {
            "id": record.id,
            "filename": record.filename,
            "created_at": record.created_at,
            "total_lines": record.total_lines,
            "stats": record.stats.model_dump(),
            "incidents": [inc.model_dump() for inc in record.incidents],
            "profile_id": record.profile_id,
            "profile_snapshot": snapshot.model_dump(),
            "raw_log_text": None
        }

    except Exception as e:
        logger.exception("Erro ao processar análise de log")
        raise HTTPException(status_code=500, detail=str(e))

# Static files mount
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
