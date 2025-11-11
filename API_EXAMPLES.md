# LeafDoc API Examples

This document provides practical examples for using the LeafDoc API.

## Table of Contents

1. [Health Check](#health-check)
2. [Predict Disease](#predict-disease)
3. [Get History](#get-history)
4. [Submit Feedback](#submit-feedback)
5. [Python Client](#python-client)
6. [JavaScript/TypeScript Client](#javascripttypescript-client)

## Health Check

### cURL
```bash
curl http://localhost:8000/health
```

### Response
```json
{
  "status": "healthy",
  "app_name": "LeafDoc",
  "model_loaded": false
}
```

## Predict Disease

### cURL (Windows PowerShell)
```powershell
curl -X POST http://localhost:8000/api/predict `
  -F "file=@C:\path\to\leaf-image.jpg"
```

### cURL (Linux/Mac)
```bash
curl -X POST http://localhost:8000/api/predict \
  -F "file=@/path/to/leaf-image.jpg"
```

### Python
```python
import requests

url = "http://localhost:8000/api/predict"

with open("leaf-image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(url, files=files)
    
print(response.json())
```

### Response
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "class": "tomato_early_blight",
  "confidence": 0.95,
  "tips": "Mulch plants, stake for air flow, and remove lower infected leaves.",
  "image_url": "/static/images/123e4567-e89b-12d3-a456-426614174000.jpg",
  "heatmap_url": "/static/heatmaps/123e4567-e89b-12d3-a456-426614174000.jpg",
  "created_at": "2025-11-09T10:30:00.123456"
}
```

## Get History

### Basic Request

```bash
curl http://localhost:8000/api/history
```

### With Pagination

```bash
curl "http://localhost:8000/api/history?page=2&limit=10"
```

### Filter by Label

```bash
curl "http://localhost:8000/api/history?label=tomato"
```

### Filter by Feedback Correctness

```bash
# Only correct predictions
curl "http://localhost:8000/api/history?correct=true"

# Only incorrect predictions
curl "http://localhost:8000/api/history?correct=false"
```

### Filter by Date Range

```bash
curl "http://localhost:8000/api/history?from=2025-11-01T00:00:00&to=2025-11-09T23:59:59"
```

### Combined Filters

```bash
curl "http://localhost:8000/api/history?page=1&limit=20&label=apple&correct=false"
```

### Python
```python
import requests

url = "http://localhost:8000/api/history"

params = {
    "page": 1,
    "limit": 20,
    "label": "tomato",
    "correct": True
}

response = requests.get(url, params=params)
print(response.json())
```

### Response
```json
{
  "items": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "image_url": "/static/images/123e4567-e89b-12d3-a456-426614174000.jpg",
      "pred_label": "tomato_early_blight",
      "pred_conf": 0.95,
      "heatmap_url": "/static/heatmaps/123e4567-e89b-12d3-a456-426614174000.jpg",
      "created_at": "2025-11-09T10:30:00.123456",
      "feedback": {
        "correct": true,
        "true_label": null
      }
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

## Submit Feedback

### Mark as Correct

```bash
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "correct": true
  }'
```

### Mark as Incorrect with Correction

```bash
curl -X POST http://localhost:8000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "correct": false,
    "true_label": "tomato_late_blight"
  }'
```

### Python
```python
import requests

url = "http://localhost:8000/api/feedback"

data = {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "correct": False,
    "true_label": "tomato_late_blight"
}

response = requests.post(url, json=data)
print(response.json())
```

### Response
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "image_url": "/static/images/123e4567-e89b-12d3-a456-426614174000.jpg",
  "pred_label": "tomato_early_blight",
  "pred_conf": 0.95,
  "heatmap_url": "/static/heatmaps/123e4567-e89b-12d3-a456-426614174000.jpg",
  "created_at": "2025-11-09T10:30:00.123456",
  "feedback": {
    "correct": false,
    "true_label": "tomato_late_blight"
  }
}
```

## Python Client

Complete Python client example:

```python
import requests
from pathlib import Path
from typing import Optional, Dict, Any


class LeafDocClient:
    """Client for LeafDoc API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def predict(self, image_path: str) -> Dict[str, Any]:
        """
        Predict disease from image.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Prediction response
        """
        with open(image_path, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{self.api_url}/predict", files=files)
            response.raise_for_status()
            return response.json()
    
    def get_history(
        self,
        page: int = 1,
        limit: int = 20,
        label: Optional[str] = None,
        correct: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Get prediction history.
        
        Args:
            page: Page number
            limit: Items per page
            label: Filter by label
            correct: Filter by correctness
            
        Returns:
            History response with pagination
        """
        params = {"page": page, "limit": limit}
        if label:
            params["label"] = label
        if correct is not None:
            params["correct"] = correct
        
        response = requests.get(f"{self.api_url}/history", params=params)
        response.raise_for_status()
        return response.json()
    
    def submit_feedback(
        self,
        prediction_id: str,
        correct: bool,
        true_label: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit feedback for a prediction.
        
        Args:
            prediction_id: Prediction UUID
            correct: Whether prediction was correct
            true_label: Correct label if prediction was wrong
            
        Returns:
            Updated prediction with feedback
        """
        data = {
            "id": prediction_id,
            "correct": correct,
        }
        if true_label:
            data["true_label"] = true_label
        
        response = requests.post(f"{self.api_url}/feedback", json=data)
        response.raise_for_status()
        return response.json()


# Usage example
if __name__ == "__main__":
    client = LeafDocClient()
    
    # Health check
    health = client.health_check()
    print(f"API Status: {health['status']}")
    
    # Predict
    result = client.predict("leaf-image.jpg")
    print(f"Prediction: {result['class']} ({result['confidence']:.2%})")
    print(f"Tips: {result['tips']}")
    
    # Get history
    history = client.get_history(page=1, limit=10, label="tomato")
    print(f"Found {history['total']} predictions")
    
    # Submit feedback
    feedback = client.submit_feedback(
        prediction_id=result['id'],
        correct=False,
        true_label="tomato_late_blight"
    )
    print(f"Feedback submitted: {feedback['feedback']}")
```

## JavaScript/TypeScript Client

Complete TypeScript client example:

```typescript
// types.ts
export interface PredictResponse {
  id: string;
  class: string;
  confidence: number;
  tips: string;
  image_url: string;
  heatmap_url: string | null;
  created_at: string;
}

export interface HistoryItem {
  id: string;
  image_url: string;
  pred_label: string;
  pred_conf: number;
  heatmap_url: string | null;
  created_at: string;
  feedback: {
    correct: boolean;
    true_label: string | null;
  } | null;
}

export interface HistoryResponse {
  items: HistoryItem[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface FeedbackRequest {
  id: string;
  correct: boolean;
  true_label?: string;
}

// client.ts
export class LeafDocClient {
  private baseUrl: string;
  private apiUrl: string;

  constructor(baseUrl: string = "http://localhost:8000") {
    this.baseUrl = baseUrl;
    this.apiUrl = `${baseUrl}/api`;
  }

  async healthCheck(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) throw new Error("Health check failed");
    return response.json();
  }

  async predict(file: File): Promise<PredictResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${this.apiUrl}/predict`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Prediction failed");
    }

    return response.json();
  }

  async getHistory(params?: {
    page?: number;
    limit?: number;
    label?: string;
    correct?: boolean;
  }): Promise<HistoryResponse> {
    const searchParams = new URLSearchParams();
    
    if (params?.page) searchParams.set("page", params.page.toString());
    if (params?.limit) searchParams.set("limit", params.limit.toString());
    if (params?.label) searchParams.set("label", params.label);
    if (params?.correct !== undefined) {
      searchParams.set("correct", params.correct.toString());
    }

    const url = `${this.apiUrl}/history?${searchParams}`;
    const response = await fetch(url);

    if (!response.ok) throw new Error("Failed to fetch history");
    return response.json();
  }

  async submitFeedback(data: FeedbackRequest): Promise<HistoryItem> {
    const response = await fetch(`${this.apiUrl}/feedback`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Failed to submit feedback");
    }

    return response.json();
  }
}

// Usage example
const client = new LeafDocClient();

// Health check
const health = await client.healthCheck();
console.log("API Status:", health.status);

// Predict
const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement;
const file = fileInput.files?.[0];
if (file) {
  const result = await client.predict(file);
  console.log(`Prediction: ${result.class} (${(result.confidence * 100).toFixed(1)}%)`);
  console.log(`Tips: ${result.tips}`);
}

// Get history
const history = await client.getHistory({ page: 1, limit: 10, label: "tomato" });
console.log(`Found ${history.total} predictions`);

// Submit feedback
await client.submitFeedback({
  id: result.id,
  correct: false,
  true_label: "tomato_late_blight",
});
```

## Error Handling

### Common Error Responses

```json
// 400 Bad Request
{
  "detail": "File must be an image"
}

// 404 Not Found
{
  "detail": "Prediction not found"
}

// 422 Validation Error
{
  "detail": [
    {
      "loc": ["body", "correct"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}

// 500 Internal Server Error
{
  "detail": "Internal server error",
  "request_id": "abc123..."
}
```

### Python Error Handling

```python
import requests
from requests.exceptions import RequestException

try:
    response = requests.post(url, files=files)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    print(f"Response: {e.response.json()}")
except RequestException as e:
    print(f"Request failed: {e}")
```

### JavaScript Error Handling

```typescript
try {
  const result = await client.predict(file);
  console.log(result);
} catch (error) {
  if (error instanceof Error) {
    console.error("Prediction failed:", error.message);
  }
}
```

## Rate Limiting

Currently, the API has no rate limiting. For production deployment, consider:

- Using nginx rate limiting
- Implementing FastAPI rate limiting middleware
- Using API gateway services

## Authentication

Currently, the API has no authentication. For production:

- Add JWT authentication
- Use API keys
- Implement OAuth 2.0

## Webhooks

The API currently doesn't support webhooks. To implement:

1. Add webhook URL configuration
2. Send POST requests on prediction events
3. Include event type and payload

## Batch Processing

For batch predictions, make multiple API calls or implement a batch endpoint:

```python
import asyncio
import aiohttp

async def predict_batch(image_paths):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for path in image_paths:
            task = predict_async(session, path)
            tasks.append(task)
        return await asyncio.gather(*tasks)

async def predict_async(session, image_path):
    with open(image_path, 'rb') as f:
        data = aiohttp.FormData()
        data.add_field('file', f, filename='image.jpg')
        
        async with session.post('http://localhost:8000/api/predict', data=data) as response:
            return await response.json()
```

## Best Practices

1. **Always handle errors** - API calls can fail
2. **Validate files** - Check file type and size before uploading
3. **Use pagination** - Don't fetch all history at once
4. **Cache responses** - Cache static data like tips
5. **Retry on failure** - Implement retry logic with exponential backoff
6. **Monitor usage** - Track API usage and performance
7. **Keep tokens secure** - If authentication is added, protect tokens
8. **Use HTTPS** - In production, always use HTTPS

## Support

For more examples and documentation:
- Interactive API docs: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc
- GitHub repository: [Link to repo]
