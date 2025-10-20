# Use Node.js 18 Alpine for smaller image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Expose port 4321 (default Astro port)
EXPOSE 4321

# Start the preview server
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0"]