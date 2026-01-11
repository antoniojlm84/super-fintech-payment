FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

# Environment variable check (optional)
# ENV NEXT_PUBLIC_API_URL=http://localhost:8000/api

CMD ["npm", "run", "dev"]
