# encoding: utf-8

'''🧠 LabCAS Infosphere: self-signed TLS certificate material for local HTTPS.

Because our sysadmins that even localhost can be compromised 🙄
'''

from __future__ import annotations

import ipaddress, tempfile
from datetime import datetime, timedelta, timezone

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID


def create_self_signed_tls_files() -> tuple[str, str]:
    '''Create a PEM certificate and private key on disk; return ``(cert_path, key_path)``.'''
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'localhost')])
    now = datetime.now(timezone.utc)
    san = x509.SubjectAlternativeName([
            x509.DNSName('localhost'),
            x509.IPAddress(ipaddress.IPv4Address('127.0.0.1')),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=1))
        .not_valid_after(now + timedelta(days=365))
        .add_extension(san, critical=False)
        .sign(key, hashes.SHA256())
    )
    key_bytes = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    cert_bytes = cert.public_bytes(serialization.Encoding.PEM)
    key_file = tempfile.NamedTemporaryFile(prefix='labcas-infosphere-', suffix='-key.pem', delete=False)
    cert_file = tempfile.NamedTemporaryFile(prefix='labcas-infosphere-', suffix='-cert.pem', delete=False)
    try:
        key_file.write(key_bytes)
        cert_file.write(cert_bytes)
    finally:
        key_file.close()
        cert_file.close()
    return cert_file.name, key_file.name
