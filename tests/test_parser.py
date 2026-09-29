import pytest
from layalog.parser import LogParser, generate_signature, normalize_log_message, clean_sample_message

SAMPLE_LOG = """[2026-09-25 00:01:13] production.ERROR: Erro no envio de e-mail e/ou na criação da notificação: Trying to get property 'seccional_id' of non-object  
[2026-09-25 00:04:06] production.ERROR: Erro no envio de e-mail e/ou na criação da notificação: Trying to get property 'seccional_id' of non-object  
[2026-09-25 09:26:32] production.ERROR: The Response content must be a string or object implementing __toString(), "object" given. {"userId":"MA8500075","email":"user1@test.com","exception":"[object] (UnexpectedValueException(code: 0): The Response content must be a string or object implementing __toString(), \\"object\\" given. at /var/www/html/sistema/vendor/Response.php:399)"}
[stacktrace]
#0 /var/www/html/sistema/vendor/Response.php(45): setContent(Object(stdClass))
#1 /var/www/html/sistema/vendor/Router.php(724): prepareResponse()
[2026-09-25 09:28:10] production.ERROR: The Response content must be a string or object implementing __toString(), "object" given. {"userId":"TR9999999","email":"another@trf1.jus.br","exception":"[object] (UnexpectedValueException(code: 0): The Response content must be a string or object implementing __toString(), \\"object\\" given. at /var/www/html/sistema/vendor/Response.php:399)"}
[stacktrace]
#0 /var/www/html/sistema/vendor/Response.php(45): setContent(Object(stdClass))
#1 /var/www/html/sistema/vendor/Router.php(724): prepareResponse()
"""

def test_parser_extracts_blocks_and_lines():
    parser = LogParser()
    blocks, total_lines = parser.parse_text(SAMPLE_LOG)
    
    assert total_lines >= 8
    assert len(blocks) == 4
    assert blocks[0].level == "ERROR"
    assert "seccional_id" in blocks[0].message
    assert len(blocks[2].stacktrace_lines) == 3

def test_parser_grouping_normalizes_dynamic_contexts():
    parser = LogParser()
    blocks, total_lines = parser.parse_text(SAMPLE_LOG)
    grouped = parser.group_incidents(blocks)

    # 4 error blocks must be grouped into exactly 2 unique incidents:
    # 1. seccional_id error (2 occurrences)
    # 2. Response content error (2 occurrences across different userIds/emails)
    assert len(grouped) == 2
    
    # Find email incident
    email_inc = next(g for g in grouped.values() if "seccional_id" in g["message"])
    assert email_inc["occurrences"] == 2
    assert email_inc["lines"] == [1, 2]

    # Find response error
    resp_inc = next(g for g in grouped.values() if "Response content" in g["message"])
    assert resp_inc["occurrences"] == 2
    assert resp_inc["lines"] == [3, 7]
    assert resp_inc["first_seen_line"] == 3

def test_signature_ignores_dynamic_parameters():
    msg1 = 'The Response content must be a string, "object" given. {"userId":"BA123","email":"a@b.com"}'
    msg2 = 'The Response content must be a string, "object" given. {"userId":"TO999","email":"c@d.com"}'
    
    sig1 = generate_signature(msg1)
    sig2 = generate_signature(msg2)
    assert sig1 == sig2

def test_signature_ignores_query_strings_and_urls():
    msg1 = 'Server error: `GET http://srvsarhapi-trf1/sarh-api/api/funcionarios/all?offset=0&ano=2027` resulted in a `500`'
    msg2 = 'Server error: `GET http://srvsarhapi-trf1/sarh-api/api/funcionarios/all?offset=100&ano=2028` resulted in a `500`'
    
    sig1 = generate_signature(msg1)
    sig2 = generate_signature(msg2)
    assert sig1 == sig2

def test_clean_sample_message():
    raw = 'The HTTP status code "1" is not valid. {"userId":"BA353403","email":"rubem.bacelar@trf1.jus.br"}'
    clean = clean_sample_message(raw)
    assert 'userId' not in clean
    assert 'rubem.bacelar' not in clean
    assert clean == 'The HTTP status code "1" is not valid.'

