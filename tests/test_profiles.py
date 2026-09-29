import pytest
import tempfile
from pathlib import Path
from layalog.models import GravityProfile, ProfileSnapshot, AnalysisRecord, LogStats, ErrorIncident
from layalog.profiles import get_builtin_profiles, get_default_profile, BUILTIN_PROFILES
from layalog.database import (
    init_db,
    get_profile,
    list_profiles,
    save_profile,
    delete_profile,
    save_analysis,
    get_analysis
)

def test_builtin_profiles_count_and_criteria():
    builtins = get_builtin_profiles()
    assert len(builtins) == 7
    
    ids = [p.id for p in builtins]
    assert "web-app-general" in ids
    assert "keycloak-iam" in ids
    assert "payments-checkout" in ids
    assert "microservices-rest" in ids
    assert "queues-workers" in ids
    assert "database-storage" in ids
    assert "edge-infra" in ids

    for p in builtins:
        assert p.is_builtin is True
        assert len(p.criteria_baixa.strip()) > 5
        assert len(p.criteria_media.strip()) > 5
        assert len(p.criteria_critica.strip()) > 5

def test_get_default_profile():
    default_p = get_default_profile()
    assert default_p.id == "web-app-general"
    assert default_p.is_builtin is True

def test_profile_database_crud():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        init_db(db_path)
        
        # Builtin profiles should be automatically seeded
        profiles = list_profiles(db_path=db_path)
        assert len(profiles) >= 7
        
        # Fetch Keycloak profile
        keycloak = get_profile("keycloak-iam", db_path=db_path)
        assert keycloak is not None
        assert keycloak.name == "Autenticação & Identidade (Keycloak / OAuth)"
        assert keycloak.is_builtin is True
        
        # Cannot delete builtin profile
        with pytest.raises(ValueError, match="built-in"):
            delete_profile("keycloak-iam", db_path=db_path)
            
        # Create a custom profile
        custom = GravityProfile(
            id="custom-erp",
            name="ERP Protheus Custom",
            description="Ambiente customizado de ERP",
            system_context="Servidor de regras de negócio Protheus com ADVPL",
            criteria_baixa="avisos de tela e cancelamento de busca pelo usuário",
            criteria_media="bloqueio de registro concorrente resolvido",
            criteria_critica="queda do DBAccess ou travamento de licenças",
            is_builtin=False
        )
        saved = save_profile(custom, db_path=db_path)
        assert saved.id == "custom-erp"
        
        # Retrieve custom profile
        fetched = get_profile("custom-erp", db_path=db_path)
        assert fetched is not None
        assert fetched.name == "ERP Protheus Custom"
        assert fetched.is_builtin is False
        
        # Update custom profile
        fetched.criteria_baixa = "novo critério baixa atualizado"
        save_profile(fetched, db_path=db_path)
        updated = get_profile("custom-erp", db_path=db_path)
        assert updated.criteria_baixa == "novo critério baixa atualizado"
        
        # Delete custom profile
        deleted = delete_profile("custom-erp", db_path=db_path)
        assert deleted is True
        assert get_profile("custom-erp", db_path=db_path) is None

def test_analysis_record_with_profile_snapshot():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        init_db(db_path)
        
        profile = get_profile("keycloak-iam", db_path=db_path)
        snapshot = ProfileSnapshot(
            profile_id=profile.id,
            profile_name=profile.name,
            system_context=profile.system_context,
            criteria_baixa=profile.criteria_baixa,
            criteria_media=profile.criteria_media,
            criteria_critica=profile.criteria_critica
        )
        
        record = AnalysisRecord(
            id="test-analysis-1",
            filename="keycloak.log",
            created_at="2026-09-28T20:00:00",
            total_lines=10,
            stats=LogStats(
                total_lines=10,
                total_errors=1,
                unique_errors=1,
                critical_errors=0,
                medium_errors=1,
                low_errors=0,
                unavailability_rate=0.0,
                most_affected_department="Autenticação / Segurança",
                department_counts={"Autenticação / Segurança": 1},
                severity_counts={"Média": 1},
                failure_type_counts={"Permission / Auth": 1}
            ),
            incidents=[],
            profile_id="keycloak-iam",
            profile_snapshot=snapshot
        )
        
        save_analysis(record, raw_text="log sample", db_path=db_path)
        
        loaded = get_analysis("test-analysis-1", db_path=db_path)
        assert loaded is not None
        assert loaded["profile_id"] == "keycloak-iam"
        assert loaded["profile_snapshot"]["profile_name"] == "Autenticação & Identidade (Keycloak / OAuth)"
        assert loaded["profile_snapshot"]["criteria_media"] == profile.criteria_media
