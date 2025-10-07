import readline from 'readline';
import { validateConfig } from './config/config.js';
import RAGService from './services/ragService.js';

const DOCUMENTS_PATH = './documents';

class ChatBot {
  constructor() {
    this.ragService = new RAGService();
    this.rl = null;
  }

  /**
   * Initialize the chatbot
   */
  async initialize() {
    console.log('\n' + '='.repeat(60));
    console.log('  RAG CHATBOT - Gemini + Pinecone');
    console.log('='.repeat(60) + '\n');

    try {
      // Validate configuration
      validateConfig();

      // Initialize RAG service
      await this.ragService.initialize();

      console.log('✓ Chatbot ready!\n');
    } catch (error) {
      console.error('✗ Initialization failed:', error.message);
      process.exit(1);
    }
  }

  /**
   * Index documents
   */
  async indexDocuments() {
    try {
      await this.ragService.indexDocuments(DOCUMENTS_PATH);
    } catch (error) {
      console.error('Failed to index documents:', error.message);
      throw error;
    }
  }

  /**
   * Display menu
   */
  displayMenu() {
    console.log('\n' + '-'.repeat(60));
    console.log('OPTIONS:');
    console.log('  1. Index documents (required before first use)');
    console.log('  2. Start chat');
    console.log('  3. View index statistics');
    console.log('  4. Exit');
    console.log('-'.repeat(60));
  }

  /**
   * Handle user choice
   */
  async handleChoice(choice) {
    switch (choice.trim()) {
      case '1':
        await this.indexDocuments();
        this.showMenu();
        break;
      case '2':
        await this.startChat();
        break;
      case '3':
        await this.showStats();
        this.showMenu();
        break;
      case '4':
        console.log('\nGoodbye! \n');
        process.exit(0);
        break;
      default:
        console.log('\nInvalid choice. Please try again.');
        this.showMenu();
    }
  }

  /**
   * Show statistics
   */
  async showStats() {
    try {
      const stats = await this.ragService.getStats();
      console.log('\nIndex Statistics:');
      console.log(`  - Total vectors: ${stats.totalRecordCount || 0}`);
      console.log(`  - Dimension: ${stats.dimension || 0}`);
      console.log(`  - Namespaces: ${Object.keys(stats.namespaces || {}).length}`);
    } catch (error) {
      console.error('Error fetching stats:', error.message);
    }
  }

  /**
   * Show menu
   */
  showMenu() {
    this.displayMenu();
    this.rl.question('\nSelect an option (1-4): ', async (choice) => {
      await this.handleChoice(choice);
    });
  }

  /**
   * Start interactive chat
   */
  async startChat() {
    console.log('\n' + '='.repeat(60));
    console.log('  CHAT MODE');
    console.log('='.repeat(60));
    console.log('\nCommands:');
    console.log('  - Type your question to get an answer');
    console.log('  - "back" - Return to main menu');
    console.log('  - "clear" - Clear chat history');
    console.log('  - "exit" - Exit chatbot\n');

    this.askQuestion();
  }

  /**
   * Ask question in chat
   */
  askQuestion() {
    this.rl.question('You: ', async (input) => {
      const question = input.trim();

      if (!question) {
        this.askQuestion();
        return;
      }

      // Handle commands
      if (question.toLowerCase() === 'back') {
        this.showMenu();
        return;
      }

      if (question.toLowerCase() === 'exit') {
        console.log('\nGoodbye! 👋\n');
        process.exit(0);
      }

      if (question.toLowerCase() === 'clear') {
        this.ragService.clearHistory();
        console.log('✓ Chat history cleared\n');
        this.askQuestion();
        return;
      }

      // Process question
      try {
        console.log('\nThinking...\n');

        const result = await this.ragService.queryWithHistory(question);

        console.log('Assistant:', result.answer);

        // Show sources
        if (result.sources.length > 0) {
          console.log('\nSources:');
          result.sources.forEach((source, idx) => {
            console.log(`  ${idx + 1}. ${source.source} (Score: ${source.score.toFixed(3)})`);
            console.log(`     "${source.content.substring(0, 100)}..."`);
          });
        }

        console.log();
      } catch (error) {
        console.error('Error:', error.message);
      }

      this.askQuestion();
    });
  }

  /**
   * Run the chatbot
   */
  async run() {
    await this.initialize();

    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    this.showMenu();
  }
}

// Start the chatbot
const chatbot = new ChatBot();
chatbot.run().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});