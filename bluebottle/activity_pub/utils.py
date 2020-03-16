import httpsig


def verify_request_signature(request, public_key):
    headers = dict(
        (header.replace('HTTP_', '').lower(), value)
        for header, value in request.META.items()
        if isinstance(header, (str, unicode)) and header.startswith('HTTP_')
    )

    verifier = httpsig.HeaderVerifier(
        headers,
        public_key,
        method=request.method, path=request.path
    )

    return verifier.verify()
