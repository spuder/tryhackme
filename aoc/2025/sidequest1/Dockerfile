FROM node:20-alpine
RUN addgroup -g 1500 -S svc_vidops \
    && adduser -S -D -H -u 1500 -G svc_vidops -s /sbin/nologin svc_vidops
WORKDIR /app
COPY server.js /app/server.js
RUN chown -R 1500:1500 /app
USER 1500:1500
EXPOSE 13403
CMD ["node","/app/server.js"]