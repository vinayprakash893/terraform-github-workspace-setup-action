FROM alpine:3.10

COPY entrypoint.sh /entrypoint.sh
COPY variable.payload /tmp/variable.payload
COPY workspace.payload /tmp/workspace.payload
COPY workspaceid.payload /tmp/workspaceid.payload

RUN apk update && \
    apk add curl jq

ENTRYPOINT ["/entrypoint.sh"]