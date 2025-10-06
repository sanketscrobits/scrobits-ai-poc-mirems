# Media Monitoring Knowledge Assistant API

A comprehensive API for media monitoring and knowledge management using vector search capabilities. Built with FastAPI, LangChain, and AstraDB for high-performance document processing and semantic search.

## 🚀 Features

- **Document Upload & Processing**: Support for multiple document formats (PDF, DOC, TXT, RTF, etc.)
- **Vector Search**: Semantic similarity search using Google Gemini embeddings
- **Scalable Storage**: AstraDB vector store for enterprise-grade document indexing
- **RESTful API**: Clean, well-documented REST endpoints with OpenAPI/Swagger support
- **Error Handling**: Comprehensive error handling with consistent response formats
- **Configuration Management**: Environment-based configuration with sensible defaults
- **Health Monitoring**: Built-in health checks and monitoring endpoints

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   LangChain      │    │   AstraDB       │
│                 │    │   Document       │    │   Vector Store  │
│ • REST API      │───▶│   Processing     │───▶│ • Embeddings    │
│ • Validation    │    │ • Loaders        │    │ • Indexing      │
│ • Error Handling│    │ • Chunking       │    │ • Search        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │
         │              ┌──────────────────┐
         │              │   Google Gemini  │
         │              │   Embeddings     │
         └──────────────┼──────────────────┘
                        │ • Text to Vector │
                        │ • Similarity     │
                        └──────────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- AstraDB account and credentials
- Google Gemini API key
- Virtual environment (recommended)

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd media-monitoring-knowledge-assistant
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:

   ```bash
   # AstraDB Configuration
   ASTRA_DB_APPLICATION_TOKEN=your_astra_db_token
   ASTRA_DB_API_ENDPOINT=your_astra_db_endpoint
   ASTRA_DB_COLLECTION_NAME=your_collection_name

   # Google Gemini Configuration
   GEMINI_API_KEY=your_gemini_api_key

   # Optional API Configuration
   API_HOST=0.0.0.0
   API_PORT=8000
   API_RELOAD=true
   API_LOG_LEVEL=info
   ```

## 🚀 Quick Start

### Option 1: Using the startup script (Recommended)

```bash
python start_api.py
```

### Option 2: Using uvicorn directly

```bash
python -m uvicorn src.main.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Using the main module

```bash
python src/main/main.py
```

The API will be available at:

- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## 📚 API Endpoints

### Health Check

- `GET /` - Basic health check
- `GET /health` - Detailed health status

### Document Management

- `POST /upload/` - Upload and process documents
- `GET /documents/` - List all indexed documents

### Search

- `POST /search/` - Semantic search through documents

## 🔍 Usage Examples

### Health Check

```bash
curl http://localhost:8000/health
```

### Upload Document

```bash
curl -X POST "http://localhost:8000/upload/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

### Search Documents

```bash
curl -X POST "http://localhost:8000/search/" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "media monitoring strategies",
    "top_k": 5
  }'
```

### List Documents

```bash
curl http://localhost:8000/documents/
```

## 🧪 Testing

Run the test script to verify API functionality:

```bash
python test_api.py
```

This will test all endpoints and provide feedback on their status.

## ⚙️ Configuration

The API can be configured through environment variables or the `.env` file:

### API Settings

- `API_HOST` - Server host (default: 0.0.0.0)
- `API_PORT` - Server port (default: 8000)
- `API_RELOAD` - Auto-reload on code changes (default: true)
- `API_LOG_LEVEL` - Logging level (default: info)

### File Upload Settings

- `MAX_FILE_SIZE` - Maximum file size in bytes (default: 50MB)
- `ALLOWED_FILE_TYPES` - Comma-separated list of allowed file extensions
- `TEMP_DIR` - Temporary directory for file uploads

### CORS Settings

- `CORS_ORIGINS` - Comma-separated list of allowed origins
- `CORS_ALLOW_CREDENTIALS` - Allow CORS credentials (default: true)

## 🔧 Development

### Project Structure

```
src/
├── config/                 # Configuration files
│   ├── settings.py        # General settings
│   └── api_settings.py    # API-specific settings
├── core/                  # Core functionality
│   └── base/             # Base classes
├── exceptions/            # Custom exceptions
├── knowledge_base/        # Document storage
├── main/                  # Main application
│   ├── main.py           # FastAPI app and endpoints
│   └── models.py         # Pydantic models
└── vector_store/          # Vector storage components
    ├── document_strategies/    # Document loading strategies
    ├── vector_index_strategies/ # Vector indexing strategies
    └── vectorstore_singletone.py # Vector store singleton
```

### Adding New Endpoints

1. **Define the model** in `src/main/models.py`
2. **Add the endpoint** in `src/main/main.py`
3. **Update documentation** in `API_DOCUMENTATION.md`

### Adding New Document Types

1. **Update allowed file types** in `src/config/api_settings.py`
2. **Ensure LangChain support** for the new format
3. **Test with sample files**

## 📊 Monitoring and Logging

### Health Checks

- `/health` endpoint for service monitoring
- Startup/shutdown event handlers
- Resource cleanup on shutdown

### Logging

- Structured logging with configurable levels
- Performance metrics collection
- Error tracking and reporting

## 🚀 Deployment

### Production Checklist

- [ ] Set up proper authentication
- [ ] Configure CORS origins
- [ ] Implement rate limiting
- [ ] Set up monitoring and alerting
- [ ] Configure SSL/TLS
- [ ] Set up load balancing
- [ ] Implement backup strategies

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "start_api.py"]
```

### Environment Variables for Production

```bash
# Security
API_DEBUG=false
API_RELOAD=false
CORS_ORIGINS=https://yourdomain.com,https://api.yourdomain.com

# Performance
API_LOG_LEVEL=warning
MAX_FILE_SIZE=104857600  # 100MB
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check the `/docs` endpoint for interactive API documentation
- **Issues**: Report bugs and feature requests through GitHub issues
- **Email**: support@mediamonitoring.com

## 🔗 Related Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [AstraDB Documentation](https://docs.datastax.com/en/astra/)
- [Google Gemini API](https://ai.google.dev/docs)

---

**Note**: This API is designed for development and testing. For production use, ensure proper security measures, authentication, and monitoring are in place.
