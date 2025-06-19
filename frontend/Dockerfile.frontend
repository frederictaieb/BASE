# Étape 1 : Dépendances
FROM node:18-alpine AS deps

WORKDIR /app

# Active Corepack et installe PNPM
RUN corepack enable && corepack prepare pnpm@8.15.4 --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Étape 2 : Build
FROM node:18-alpine AS builder
WORKDIR /app

RUN corepack enable && corepack prepare pnpm@8.15.4 --activate

COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN pnpm build

# Étape 3 : Exécution
FROM node:18-alpine AS runner
WORKDIR /app

RUN corepack enable && corepack prepare pnpm@8.15.4 --activate

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000

CMD ["pnpm", "start"]
