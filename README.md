# Generative AI Learning Repository

This repository provides comprehensive implementations and demonstrations of **Generative AI concepts** through practical examples. It serves as a learning platform for understanding how modern AI systems work, from basic language models to advanced retrieval-augmented generation and AI agents.

## Core Generative AI Concepts Implemented

### 1. Large Language Models (LLMs)
**Location**: `How LLM works/`
- **Basic Chat Implementation**: Demonstrates fundamental LLM interaction using Google's Gemini models
- **Conversation Management**: Shows how to maintain chat history and context
- **Model Selection**: Examples using different Gemini model variants (gemini-2.0-flash, gemini-2.5-flash)

### 2. Retrieval-Augmented Generation (RAG)
**Location**: `gemini-rag-chatbot/`
- **Document Processing**: Converts PDFs and text files into searchable chunks
- **Vector Embeddings**: Uses Gemini's embedding model to create semantic representations
- **Vector Database Integration**: Implements Pinecone for efficient similarity search
- **Context-Aware Responses**: Generates answers based on retrieved document context
- **Conversation Memory**: Maintains chat history for contextual follow-up questions

### 3. AI Agents with Function Calling
**Location**: `AI Agent/`
- **Tool Integration**: Demonstrates how AI agents can use external tools and APIs
- **Function Declarations**: Shows proper schema definition for tool parameters
- **Multi-Tool Coordination**: Implements agents that can choose between multiple available tools
- **Dynamic Tool Execution**: Real-time tool calling based on user queries
- **Tool Categories**: Mathematical operations, data fetching, and computational tasks

### 4. Advanced AI Agents
**Location**: `Cursor/` and `OpenAI Agent SDK/`
- **System Instructions**: Complex prompt engineering for specialized agent behavior
- **Command Execution**: Agents that can execute terminal commands and file operations
- **Multi-Step Planning**: Agents that break down complex tasks into sequential steps
- **Cross-Platform Support**: Handles different operating systems (Windows, Linux, macOS)
- **Validation Loops**: Implements plan-execute-validate-repeat workflows

### 5. Model Context Protocol (MCP)
**Location**: `MCP Server/`
- **Server Implementation**: Creates MCP servers for tool integration
- **Schema Validation**: Uses Zod for robust parameter validation
- **Tool Registration**: Demonstrates how to register and expose tools to AI models
- **Data Processing**: Shows integration with external data sources and APIs

### 6. Memory and Context Management
**Location**: `Memory in AI/`
- **Memory Types**: Documentation and examples of different memory patterns in AI systems
- **Context Preservation**: Techniques for maintaining conversation context
- **Memory Optimization**: Strategies for managing memory efficiently in long conversations

## Project Structure
```
Generative-AI/
│
├── AI Agent/                    # Function calling and tool integration
├── Cursor/                      # Advanced agent with command execution
├── gemini-rag-chatbot/         # Complete RAG implementation
├── How LLM works/              # Basic LLM concepts and chat
├── MCP Server/                 # Model Context Protocol implementation
├── OpenAI Agent SDK/           # Alternative agent framework
├── Memory in AI/               # Memory management concepts
├── RAG/                        # RAG documentation and resources
└── README.md
```

## Key Technologies and Frameworks

### AI Models
- **Google Gemini**: Primary LLM for text generation and embeddings
- **Gemini 2.0 Flash**: Latest model for conversational AI
- **Gemini 2.5 Flash**: Advanced model for complex reasoning
- **Embedding Models**: For semantic search and document similarity

### Vector Databases
- **Pinecone**: Cloud-based vector database for similarity search
- **Vector Operations**: Efficient storage and retrieval of embeddings

### Development Tools
- **Node.js**: Runtime environment for all implementations
- **Google Generative AI SDK**: Official SDK for Gemini integration
- **Pinecone SDK**: Vector database client
- **Zod**: Schema validation library
- **Axios**: HTTP client for API calls

### Agent Frameworks
- **Custom Agent Implementation**: Hand-built agent architecture
- **OpenAI Agent SDK**: Third-party agent framework
- **Model Context Protocol**: Standardized tool integration protocol

## Installation and Setup

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn package manager
- Google AI API key
- Pinecone API key (for RAG functionality)

### Quick Start
1. Clone the repository
   ```bash
   git clone https://github.com/tusquake/Generative-AI.git
   cd Generative-AI
   ```

2. Install dependencies for each project
   ```bash
   # For basic LLM examples
   cd "How LLM works"
   npm install
   
   # For RAG chatbot
   cd ../gemini-rag-chatbot
   npm install
   
   # For AI agents
   cd ../AI Agent
   npm install
   ```

3. Configure environment variables
   - Set your Google AI API key
   - Set your Pinecone API key (for RAG)
   - Update configuration files as needed

4. Run examples
   ```bash
   # Basic chat
   node "How LLM works/index.js"
   
   # RAG chatbot
   node gemini-rag-chatbot/src/index.js
   
   # AI agent
   node "AI Agent/index.js"
   ```

## Usage Examples

### Basic Chat
```javascript
// Simple conversation with Gemini
const response = await ai.models.generateContent({
  model: "gemini-2.0-flash",
  contents: conversationHistory
});
```

### RAG Implementation
```javascript
// Query with document context
const result = await ragService.query("What is machine learning?");
console.log(result.answer);
console.log("Sources:", result.sources);
```

### Function Calling
```javascript
// Agent with tool access
const response = await ai.models.generateContent({
  model: "gemini-2.5-flash",
  contents: history,
  config: {
    tools: [{ functionDeclarations: [toolSchema] }]
  }
});
```

## Learning Path

### Beginner Level
1. Start with `How LLM works/` to understand basic LLM interaction
2. Explore conversation management and context handling
3. Learn about different model variants and their capabilities

### Intermediate Level
1. Dive into `AI Agent/` for function calling concepts
2. Understand tool integration and parameter validation
3. Learn about agent decision-making processes

### Advanced Level
1. Study the complete RAG implementation in `gemini-rag-chatbot/`
2. Explore vector embeddings and similarity search
3. Understand document processing and chunking strategies
4. Learn about conversation memory and context management

### Expert Level
1. Examine the advanced agent in `Cursor/` for complex task execution
2. Study MCP implementation for standardized tool integration
3. Explore memory management patterns and optimization techniques
4. Understand cross-platform compatibility and error handling

## Future Concepts and Extensions

### Planned Implementations
- **Multi-Modal AI**: Integration of text, image, and audio processing
- **Fine-Tuning**: Custom model training and adaptation
- **Agent Orchestration**: Multi-agent systems and coordination
- **Advanced RAG**: Hybrid search, re-ranking, and query optimization
- **Memory Systems**: Long-term memory and knowledge graphs
- **Evaluation Metrics**: Performance measurement and benchmarking

### Advanced Topics
- **Prompt Engineering**: Advanced techniques for better model performance
- **Chain-of-Thought**: Reasoning patterns and step-by-step problem solving
- **Few-Shot Learning**: Learning from limited examples
- **Reinforcement Learning**: Agent training through interaction and feedback
- **Federated Learning**: Distributed model training across multiple agents


