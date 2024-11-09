upstream web_app {
    server web:8000;
}

// server {
//     listen 443 ssl;
//     server_name resumechecker-be.mostafijur.xyz;
//
//     ssl_certificate /etc/letsencrypt/live/resumechecker-be.mostafijur.xyz/fullchain.pem;
//     ssl_certificate_key /etc/letsencrypt/live/resumechecker-be.mostafijur.xyz/privkey.pem;
//
//     access_log /var/log/nginx/access.log;
//     error_log /var/log/nginx/error.log;
//
//     location /static/ {
//         alias /var/www/static/;
//     }
//
//     location / {
//         proxy_pass http://web_app;
//         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
//         proxy_set_header Host $host;
//         proxy_redirect off;
//     }
// }

server {
    listen 80;
        server_name your_domain.com;

    location ~/.well-known/acme-challenge {
        allow all;
        root /var/www/certbot;
    }

    return 301 https://$host:$request_uri;
}