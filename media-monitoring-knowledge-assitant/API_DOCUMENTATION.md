# Media Monitoring Knowledge Assistant API Documentation

## Overview

The Media Monitoring Knowledge Assistant API is a comprehensive solution for document management and semantic search using vector embeddings. Built with FastAPI, it provides high-performance endpoints for uploading, processing, and searching through document collections.

## Base URL

```
http://localhost:8000
```

## API Endpoints

### Health Check Endpoints

#### GET /

**Health Check - Root Endpoint**

Check if the API is running and healthy.

**Response:**

```json
{
  "status": "healthy",
  "message": "Media monitoring API is running",
  "version": "1.0.0"
}
```

#### GET /health

**Detailed Health Check**

Detailed health check endpoint with comprehensive status information.

**Response:**

```json
{
  "status": "healthy",
  "message": "Media monitoring API is running and healthy",
  "version": "1.0.0"
}
```

### Document Management Endpoints

#### POST /upload/

**Upload Document**

Upload a document for processing and indexing. Supports various document formats including PDF, DOC, TXT, and more.

**Request:**

- **Content-Type:** `multipart/form-data`
- **Body:** Form data with file upload

**Parameters:**

- `file` (required): Document file to upload and process

**File Requirements:**

- Maximum file size: 50MB
- Supported formats: PDF, DOC, DOCX, TXT, RTF, and other text-based formats

**Response:**

```json
{
  "filename": "document.pdf",
  "content": {
    "text": "Document content...",
    "metadata": {
      "pages": 5,
      "format": "pdf"
    }
  },
  "message": "Document uploaded and processed successfully",
  "file_size": 1024000
}
```

**Error Responses:**

- `400 Bad Request`: Invalid file format or missing filename
- `413 Request Entity Too Large`: File size exceeds 50MB limit
- `500 Internal Server Error`: Document processing failed

**Example using curl:**

```bash
curl -X POST "http://localhost:8000/upload/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

#### GET /documents/

**List Documents**

Retrieve a list of all indexed documents in the knowledge base with metadata.

**Response:**

```json
{
  "documents": [
    {
      "filename": "document1.pdf",
      "file_size": 1024000,
      "upload_date": "2024-01-15T10:30:00Z",
      "processing_status": "completed",
      "indexed": true
    }
  ],
  "total_count": 1,
  "message": "Documents retrieved successfully"
}
```

### Search Endpoints

#### POST /search/

**Search Documents**

Search through indexed documents using semantic similarity and vector embeddings.

**Request:**

```json
{
  "query": "media monitoring strategies",
  "top_k": 5
}
```

**Parameters:**

- `query` (required): Search query text (1-1000 characters)
- `top_k` (optional): Number of top results to return (1-50, default: 5)

**Response:**

```json
{
  "query": "media monitoring strategies",
  "results": [
    {
      "content": "Media monitoring involves tracking and analyzing...",
      "score": 0.95,
      "metadata": {
        "source": "document1.pdf",
        "page": 3
      }
    }
  ],
  "total_results": 1,
  "processing_time": 0.125
}
```

**Error Responses:**

- `400 Bad Request`: Empty or invalid search query
- `500 Internal Server Error`: Search operation failed

**Example using curl:**

```bash
curl -X POST "http://localhost:8000/search/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "media monitoring strategies",
    "top_k": 5
  }'
```

## Data Models

### Request Models

#### SearchRequest

```json
{
  "query": "string (1-1000 chars)",
  "top_k": "integer (1-50, optional, default: 5)"
}
```

#### BatchUploadRequest

```json
{
  "files": ["string (1-10 file paths)"]
}
```

### Response Models

#### HealthResponse

```json
{
  "status": "string",
  "message": "string",
  "version": "string"
}
```

#### UploadResponse

```json
{
  "filename": "string",
  "content": "object",
  "message": "string",
  "file_size": "integer"
}
```

#### SearchResponse

```json
{
  "query": "string",
  "results": [
    {
      "content": "string",
      "score": "float (0.0-1.0)",
      "metadata": "object (optional)"
    }
  ],
  "total_results": "integer",
  "processing_time": "float"
}
```

#### ErrorResponse

```json
{
  "error": "string",
  "message": "string",
  "details": "object (optional)"
}
```

## Error Handling

The API uses standard HTTP status codes and provides consistent error responses:

- **4xx Client Errors**: Bad requests, validation errors, file size limits
- **5xx Server Errors**: Internal processing errors, document processing failures

All errors return a consistent `ErrorResponse` format with:

- `error`: Error type identifier
- `message`: Human-readable error description
- `details`: Additional error context (when available)

## Authentication

Currently, the API does not require authentication. However, for production use, it's recommended to implement:

- API key authentication
- JWT tokens
- OAuth 2.0 integration

## Rate Limiting

The API currently doesn't implement rate limiting. For production use, consider:

- Request rate limiting per IP/user
- File upload size quotas
- Search query frequency limits

## CORS Configuration

The API includes CORS middleware configured to allow cross-origin requests. Current configuration:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Note:** For production, restrict `allow_origins` to specific domains.

## File Processing

### Supported Document Types

- **PDF**: Portable Document Format
- **DOC/DOCX**: Microsoft Word documents
- **TXT**: Plain text files
- **RTF**: Rich Text Format
- **Other text-based formats** supported by LangChain

### Processing Pipeline

1. **File Upload**: Temporary storage in system temp directory
2. **Document Loading**: LangChain document loader processes the file
3. **Content Extraction**: Text and metadata extraction
4. **Vector Embedding**: Google Gemini embeddings generation
5. **Storage**: AstraDB vector store indexing
6. **Cleanup**: Temporary file removal

## Vector Search

### Search Algorithm

The API uses semantic similarity search through vector embeddings:

1. **Query Processing**: Convert search query to vector embedding
2. **Similarity Calculation**: Compute cosine similarity with indexed documents
3. **Ranking**: Sort results by similarity score
4. **Result Formatting**: Return top-k most relevant results

### Performance Considerations

- **Embedding Model**: Google Gemini embedding-001
- **Vector Store**: AstraDB for scalable vector storage
- **Indexing**: Automatic indexing on document upload
- **Caching**: Consider implementing Redis for query result caching

## Development and Testing

### Running the API

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn src.main.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

- **Swagger UI**: `/docs` - Interactive API documentation
- **ReDoc**: `/redoc` - Alternative documentation view
- **OpenAPI JSON**: `/openapi.json` - Raw OpenAPI specification

### Testing Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Upload document
curl -X POST "http://localhost:8000/upload/" \
  -F "file=@test_document.pdf"

# Search documents
curl -X POST "http://localhost:8000/search/" \
  -H "Content-Type: application/json" \
  -d '{"query": "test query", "top_k": 3}'
```

## Monitoring and Logging

### Health Monitoring

- `/health` endpoint for service health checks
- Startup/shutdown event handlers
- Resource cleanup on shutdown

### Logging Recommendations

For production deployment, implement:

- Structured logging (JSON format)
- Log levels (DEBUG, INFO, WARNING, ERROR)
- Log aggregation and monitoring
- Performance metrics collection

## Deployment Considerations

### Environment Variables

```bash
ASTRA_DB_APPLICATION_TOKEN=your_token
ASTRA_DB_API_ENDPOINT=your_endpoint
ASTRA_DB_COLLECTION_NAME=your_collection
GEMINI_API_KEY=your_gemini_key
```

### Production Checklist

- [ ] Enable authentication
- [ ] Configure CORS properly
- [ ] Implement rate limiting
- [ ] Set up monitoring and logging
- [ ] Configure proper error handling
- [ ] Set up health checks
- [ ] Implement backup strategies
- [ ] Configure SSL/TLS
- [ ] Set up load balancing

### Scaling Considerations

- **Horizontal Scaling**: Multiple API instances behind load balancer
- **Database Scaling**: AstraDB auto-scaling capabilities
- **Caching**: Redis for query result caching
- **CDN**: For static file delivery
- **Monitoring**: Prometheus + Grafana for metrics

## Support and Contact

For API support and questions:

- **Email**: support@mediamonitoring.com
- **Documentation**: This document and `/docs` endpoint
- **Issues**: GitHub repository issues

## License

This API is licensed under the MIT License. See the LICENSE file for details.
