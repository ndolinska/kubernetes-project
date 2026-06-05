FROM nginx:1.25-alpine

# Usuń domyślną konfigurację nginx i zastąp własną
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Skopiuj aplikację
COPY index.html /usr/share/nginx/html/index.html
COPY style.css  /usr/share/nginx/html/style.css

# Uruchom jako użytkownik nginx (uid 101) — non-root
USER 101

EXPOSE 8080
