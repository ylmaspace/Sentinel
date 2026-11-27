from pathlib import Path
from sentinel.core.file_identity import identify_file

def test_sha256_and_identity(tmp_path: Path):
    f=tmp_path/"note.txt"; f.write_bytes(b"harmless sample")
    result=identify_file(f)
    assert result.sha256 == "e9a1d1b2949d8587c58977d36c8b279b60a485ff443435c615529336987e38a4"
    assert result.name == "note.txt" and result.size == 15

def test_missing_and_directory_paths(tmp_path: Path):
    import pytest
    with pytest.raises(FileNotFoundError): identify_file(tmp_path/"absent")
    with pytest.raises(ValueError): identify_file(tmp_path)

def test_extension_does_not_determine_type(tmp_path: Path):
    f=tmp_path/"not-a-pdf.pdf"; f.write_bytes(b"plain text")
    assert identify_file(f).detected_type == "Text (UTF-8-compatible prefix)"
