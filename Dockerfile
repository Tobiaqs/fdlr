### UNIVERSAL ###
FROM node:16.13-alpine AS uni-frontend-packages
WORKDIR /packages/
COPY ["frontend/package.json", "frontend/package-lock.json", "/packages/"]
RUN npm ci


### PROD ###
FROM python:3.10 AS prod-backend
WORKDIR /tmp/
COPY backend/requirements/prod.txt /tmp/prod.txt
RUN pip install -r /tmp/prod.txt
WORKDIR /app/
COPY backend/ /app/
EXPOSE 8000
RUN python manage.py collectstatic
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "fdlr.asgi:application"]

FROM node:16.13-alpine AS prod-frontend-build
WORKDIR /app/
COPY --from=uni-frontend-packages /packages/ /app/
COPY frontend/ /app/
RUN npm run build

FROM nginx:1.21-alpine AS prod-frontend
RUN rm /etc/nginx/conf.d/default.conf
COPY config/prod/proxy.conf /etc/nginx/conf.d/proxy.conf
WORKDIR /app/
COPY --from=prod-frontend-build /app/build/ /app/


### DEV ###
FROM python:3.10 AS dev-backend
WORKDIR /tmp/
COPY backend/requirements/dev.txt /tmp/dev.txt
RUN pip install -r /tmp/dev.txt
WORKDIR /app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM node:16.13-alpine AS dev-frontend
WORKDIR /app/
COPY --from=uni-frontend-packages /packages/ /app/
EXPOSE 3000
CMD ["npm", "run", "start"]

FROM nginx:1.21-alpine AS dev-proxy
RUN rm /etc/nginx/conf.d/default.conf
COPY config/dev/proxy.conf /etc/nginx/conf.d/proxy.conf
