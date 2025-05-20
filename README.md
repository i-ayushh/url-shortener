# URL Shortener

A simple, fast, and serverless URL Shortener built using AWS.

## 🚀 Tech Stack

- **Frontend**: HTML + JavaScript hosted on AWS S3
- **Backend**: AWS Lambda + API Gateway
- **Database**: Amazon DynamoDB

## 📦 Features

- Shortens long URLs into compact links
- Option to provide a custom short code
- Supports expiry (validity) for short URLs
- Automatically redirects to the original URL

## 🔗 API Endpoints

### POST `/shorten`

Create a short URL.

**Request body:**
```json
{
  "url": "https://example.com/your-very-long-url",
  "custom_code": "mycode",       // Optional
  "expiry": 1716432000            // Optional Unix timestamp
}
```

**Response:**
```json
{
  "short_url": "https://your-api/shorten/mycode"
}
```

---

### GET `/shorten/{code}`

Redirects to the original URL.

If the URL has expired, it will return an error.

## 🛠️ Setup Instructions

1. **Create DynamoDB Table**  
   - Table name: `url_mappings`  
   - Partition key: `short_code` (String)

2. **Deploy Lambda Function**  
   - Upload your Python code with proper IAM role
   - Make sure it has access to DynamoDB

3. **Create API Gateway Routes**  
   - `POST /shorten`
   - `GET /shorten/{code}`
   - Enable CORS for both

4. **Host Frontend**  
   - Upload `index.html` to S3 bucket
   - Enable static website hosting
   - Make bucket public or use CloudFront if needed

5. **Update Frontend Code**  
   - Change the API URL in the JavaScript to your deployed endpoint

## 🧪 Testing Examples

Try these long URLs to see shortening in action:

- https://assets.aboutamazon.com/dims4/default/dd7f211/2147483647/strip/false/crop/960x720+0+0/resize/960x720!/quality/90/?url=https%3A%2F%2Famazon-blogs-brightspot.s3.amazonaws.com%2F66%2Ff3%2Fcb7e8e804a1f991c96593cf465e1%2Faws-logo-white-on-si.jpg
- https://www.example.com/articles/2025/05/how-to-host-aws-s3-static-site-with-cloudfront-and-ssl


## ℹ️ Disclaimer

> For best results, use long URLs. If you try to shorten an already short link, the output might be the same length or longer.

## 👨‍💻 Author

**Ayush Gupta**  
GitHub: [i-ayushh](https://github.com/i-ayushh)
Linkedin: [ayushgupta767](https://www.linkedin.com/in/ayushgupta767/)
