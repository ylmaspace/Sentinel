from pathlib import Path
import hashlib

from sentinel.core.file_identity import identify_file


def test_sha256_and_identity(tmp_path: Path):
    fixture = b"harmless sample"
    f = tmp_path / "note.txt"
    f.write_bytes(fixture)
    result = identify_file(f)
    # Derive the expected value independently with the standard library instead
    # of preserving an incorrect, hard-coded digest.
    assert result.sha256 == hashlib.sha256(fixture).hexdigest()
    assert result.name == "note.txt" and result.size == 15


def test_sha256_matches_known_vector(tmp_path: Path):
    f = tmp_path / "known.txt"
    f.write_bytes(b"abc")
    assert identify_file(f).sha256 == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_missing_and_directory_paths(tmp_path: Path):
    import pytest
    with pytest.raises(FileNotFoundError):
        identify_file(tmp_path / "absent")
    with pytest.raises(ValueError):
        identify_file(tmp_path)


def test_extension_does_not_determine_type(tmp_path: Path):
    f = tmp_path / "not-a-pdf.pdf"
    f.write_bytes(b"plain text")
    assert identify_file(f).detected_type == "Text (UTF-8-compatible prefix)"
