import hashlib,json,pathlib,zipfile
from cryptography import x509
from cryptography.hazmat.primitives import hashes,serialization
from cryptography.hazmat.primitives.asymmetric import padding
from payload import wire,one
root=pathlib.Path(__file__).resolve().parent
h=json.loads((root/'payload-header.json').read_text())
with (root/'original/OPD2413_16.0.10.600_CN01.zip').open('rb') as f:
    f.seek(h['offset']);metadata=f.read(24+h['manifest_length']);sigblob=f.read(h['metadata_signature_length'])
signatures=[one(wire(v),2) for v in wire(sigblob)[1]]
certpath=root/'donor-tree-case/my_engineering/etc/security/otacerts.zip'
results=[]
with zipfile.ZipFile(certpath) as z:
    for name in z.namelist():
        raw=z.read(name)
        cert=x509.load_pem_x509_certificate(raw) if b'BEGIN CERTIFICATE' in raw else x509.load_der_x509_certificate(raw)
        key=cert.public_key();ok=False
        for sig in signatures:
            try:key.verify(sig,metadata,padding.PKCS1v15(),hashes.SHA256());ok=True
            except Exception:pass
        results.append(dict(name=name,subject=cert.subject.rfc4514_string(),cert_sha256=cert.fingerprint(hashes.SHA256()).hex(),spki_sha256=hashlib.sha256(key.public_bytes(serialization.Encoding.DER,serialization.PublicFormat.SubjectPublicKeyInfo)).hexdigest(),metadata_signature_valid=ok))
assert any(r['metadata_signature_valid'] for r in results)
(root/'metadata-signature-result.json').write_text(json.dumps(dict(scope='Metadata signature checked against certificate embedded in the acquired official-server image; independent historical key comparison still separate',certificates=results),indent=2))
print('METADATA_SIGNATURE_PASS',results)
