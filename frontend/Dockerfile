# Use Node image
FROM node:18

# Create app directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Build React app
RUN npm run build

# Install serve to run production build
RUN npm install -g serve

# Run the app
CMD ["serve", "-s", "build", "-l", "3000"]