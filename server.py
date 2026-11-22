#!/usr/bin/env python3
"""Servidor local para probar e instalar DocScan PDF desde el telefono Android."""

import argparse
import datetime
import functools
import http.server
import ipaddress
import os
import socket
import socketserver
import ssl
import tempfile
from pathlib import Path


class AppHandler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        '.js': 'application/javascript; charset=utf-8',
        '.mjs': 'application/javascript; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
        '.json': 'application/manifest+json; charset=utf-8',
        '.webmanifest': 'application/manifest+json; charset=utf-8',
        '.svg': 'image/svg+xml',
        '.png': 'image/png',
        '.html': 'text/html; charset=utf-8',
    }

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()


class ReusableTCPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def get_lan_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
    except OSError:
        return '127.0.0.1'


def generate_self_signed_cert(lan_ip: str, cert_dir: Path) -> tuple[Path, Path]:
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.x509.oid import NameOID

    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, 'DocScan PDF Local')])
    now = datetime.datetime.now(datetime.timezone.utc)

    sans = [
        x509.DNSName('localhost'),
        x509.IPAddress(ipaddress.ip_address('127.0.0.1')),
    ]
    if lan_ip and lan_ip != '127.0.0.1':
        sans.append(x509.IPAddress(ipaddress.ip_address(lan_ip)))

    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(minutes=5))
        .not_valid_after(now + datetime.timedelta(days=30))
        .add_extension(x509.SubjectAlternativeName(sans), critical=False)
        .sign(key, hashes.SHA256())
    )

    cert_path = cert_dir / 'cert.pem'
    key_path = cert_dir / 'key.pem'
    cert_path.write_bytes(cert.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        )
    )
    return cert_path, key_path


def main():
    parser = argparse.ArgumentParser(description='Servidor web local para DocScan PDF')
    parser.add_argument('--port', type=int, default=8000, help='Puerto HTTP/HTTPS (por defecto 8000)')
    parser.add_argument('--https', action='store_true', help='Habilitar HTTPS autofirmado para camara continua en Wi-Fi')
    args = parser.parse_args()

    root_dir = Path(__file__).resolve().parent
    handler = functools.partial(AppHandler, directory=str(root_dir))
    server = ReusableTCPServer(('0.0.0.0', args.port), handler)

    lan_ip = get_lan_ip()
    scheme = 'http'

    tmp_ctx = None
    if args.https:
        tmp_ctx = tempfile.TemporaryDirectory(prefix='docscan-cert-')
        cert_path, key_path = generate_self_signed_cert(lan_ip, Path(tmp_ctx.name))
        ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_ctx.load_cert_chain(certfile=str(cert_path), keyfile=str(key_path))
        server.socket = ssl_ctx.wrap_socket(server.socket, server_side=True)
        scheme = 'https'

    print(f'DocScan PDF activo en:')
    print(f'  Local:   {scheme}://localhost:{args.port}')
    print(f'  Android: {scheme}://{lan_ip}:{args.port}  (misma red Wi-Fi)')
    print('Presiona Ctrl+C para detener.')

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServidor detenido.')
    finally:
        server.server_close()
        if tmp_ctx is not None:
            tmp_ctx.cleanup()


if __name__ == '__main__':
    main()
