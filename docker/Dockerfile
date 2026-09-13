FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip install --no-cache-dir pytest

COPY docker/entrypoint.sh /usr/local/bin/repair-loop-entrypoint
RUN chmod 0555 /usr/local/bin/repair-loop-entrypoint

USER 65534:65534
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/repair-loop-entrypoint"]
CMD ["python", "-m", "pytest", "-q"]
