# AI Image Generator 🎨

A beautiful, Firefly-inspired web application for generating high-quality images from text prompts using Stability AI's diffusion models.

![AI Image Generator](https://img.shields.io/badge/AI-Image%20Generator-ff0050?style=for-the-badge&logo=adobe&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)


## Project Structure

```
ai-image-generator/
├── server.js              # Express server with API endpoints
├── index.html             # Main application interface
├── package.json           # Project dependencies
├── README.md             # Project documentation
└── assets/               # Static assets (if any)
```

## Understanding Diffusion Models

### What are Diffusion Models?

Diffusion models are a class of generative AI models that have revolutionized image generation. They work by learning to reverse a gradual noising process, effectively "denoising" random noise into coherent images.

### How Diffusion Models Work

#### 1. **Forward Process (Noising)**
```
Original Image → Add Noise → Add More Noise → ... → Pure Noise
```
- Gradually adds Gaussian noise to training images over many timesteps
- Each step makes the image slightly more noisy
- Final result is pure random noise

#### 2. **Reverse Process (Denoising)**
```
Pure Noise → Remove Noise → Remove More Noise → ... → Generated Image
```
- Neural network learns to predict and remove noise at each step
- Guided by text embeddings from your prompt
- Results in high-quality, coherent images

### Key Advantages

- **High Quality**: Produces extremely detailed and realistic images
- **Text Control**: Excellent understanding of complex text prompts
- **Flexibility**: Can generate diverse styles and concepts
- **Scalability**: Works well at high resolutions (1024x1024+)

### Stable Diffusion XL

This project uses **Stable Diffusion XL 1024**, which offers:

- **Higher Resolution**: Native 1024x1024 generation
- **Better Text Understanding**: Improved prompt comprehension
- **Enhanced Details**: More realistic textures and lighting
- **Faster Generation**: Optimized inference pipeline

### Technical Parameters

```javascript
{
  text_prompts: [{ text: "your prompt here" }],
  cfg_scale: 7,        // Classifier-free guidance (higher = more prompt adherence)
  steps: 30,           // Denoising steps (more = higher quality, slower)
  width: 1024,         // Image width in pixels
  height: 1024         // Image height in pixels
}
```

## API Endpoints

### POST `/generate`

Generate an image from a text prompt.

**Request Body:**
```json
{
  "prompt": "A majestic mountain landscape at sunset"
}
```

**Response:**
```json
{
  "image": "base64_encoded_image_data"
}
```

**Error Responses:**
- `400`: Missing prompt
- `500`: API error or generation failure

## Customization

### Modify Generation Parameters

In `server.js`, you can adjust:

```javascript
{
  cfg_scale: 7,        // 1-20, higher values follow prompt more closely
  steps: 30,           // 10-50, more steps = better quality
  width: 1024,         // 512, 768, 1024
  height: 1024,        // 512, 768, 1024
  samples: 1,          // Number of images to generate
  seed: 0              // For reproducible results
}
```

## Features

- ** Professional UI**: Adobe Firefly-inspired design with glassmorphism effects
- ** High-Quality Generation**: Powered by Stable Diffusion XL 1024x1024 models
- ** Multiple Save Options**: PNG, JPG formats with one-click download
- ** Clipboard Support**: Direct image copying for easy sharing
- ** Native Sharing**: Built-in Web Share API integration
- ** Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- ** Real-time Generation**: Fast image creation with loading states
- ** Beautiful Animations**: Smooth transitions and floating elements

## Quick Start

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Stability AI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/ai-image-generator.git
   cd ai-image-generator
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up your API key**
   ```javascript
   // In server.js, replace with your Stability AI API key
   const api_key = "your-stability-ai-api-key-here";
   ```

4. **Start the server**
   ```bash
   node server.js
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

## Tech Stack

### Backend
- **Express.js**: Web server framework
- **Node-fetch**: HTTP client for API requests
- **Body-parser**: Request parsing middleware
- **CORS**: Cross-origin resource sharing

### Frontend
- **Vanilla JavaScript**: Core functionality
- **CSS3**: Advanced styling with animations
- **HTML5**: Modern semantic markup
- **Canvas API**: Image processing and format conversion

### AI Service
- **Stability AI API**: Stable Diffusion XL models
- **Text-to-Image**: Advanced diffusion model pipeline

### Styling Customization

The UI uses CSS custom properties for easy theming:

```css
:root {
  --primary-gradient: linear-gradient(135deg, #ff0050 0%, #ff4081 100%);
  --background-gradient: linear-gradient(135deg, #1a0d2e 0%, #16213e 50%, #0f4c75 100%);
  --glass-background: rgba(255, 255, 255, 0.1);
  --glass-border: rgba(255, 255, 255, 0.2);
}
```

## Configuration Options

### Environment Variables

Create a `.env` file:

```env
STABILITY_API_KEY=your_api_key_here
PORT=3000
NODE_ENV=production
```

### Advanced Features

- **Negative Prompts**: Add unwanted elements to avoid
- **Style Presets**: Apply artistic styles
- **Aspect Ratios**: Different image dimensions
- **Batch Generation**: Multiple images at once

## Error Handling

The application includes comprehensive error handling:

- **Network Errors**: Connection timeouts and retries
- **API Limits**: Rate limiting and quota management
- **Invalid Prompts**: Content filtering and validation
- **Browser Compatibility**: Fallbacks for older browsers

## Performance Optimization

- **Image Compression**: Automatic optimization for web
- **Lazy Loading**: Efficient resource management
- **Caching**: Smart caching strategies
- **Progressive Enhancement**: Works without JavaScript

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request