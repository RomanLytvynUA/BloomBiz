# frontend/Dockerfile

FROM node:16-alpine

WORKDIR /src

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

EXPOSE 5173

# Serve the application
CMD ["npm", "run", "dev"]
