FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    git \
    make \
    gcc \
    python3-pip \
    && curl -LO https://go.dev/dl/go1.22.0.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz \
    && rm go1.22.0.linux-amd64.tar.gz

ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/go"

RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

RUN curl -LO https://github.com/yannh/kubeconform/releases/latest/download/kubeconform-linux-amd64.tar.gz \
    && tar -xzvf kubeconform-linux-amd64.tar.gz \
    && mv kubeconform /usr/local/bin/ \
    && rm kubeconform-linux-amd64.tar.gz

RUN helm plugin install https://github.com/jtyr/kubeconform-helm

RUN pip install pyyaml

WORKDIR /app

COPY validate_values.py /app/validate_values.py

RUN chmod +x /app/validate_values.py

ENTRYPOINT ["python", "/app/validate_values.py"]

