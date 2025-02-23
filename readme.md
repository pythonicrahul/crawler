# Web Crawler Assignment: Proof of Concept, Release Plan, and Documentation

## 1. Overview
This document outlines the proof of concept, release plan, and production deployment guidelines for the web crawler designed to process billions of URLs using Redis Streams, MongoDB, and Docker containers.

**Technology Stack:**
- **Queue System:** Redis Streams for message queuing and distributed processing.
- **Database:** MongoDB for storing extracted metadata.
- **Crawler:** Requests and Selenium for scraping pages.
- **Containerization:** Docker and Docker Compose for deployment.
- **Programming Language:** Python 3.12

---

## 2. Proof of Concept

**Objective:** Verify that the system can efficiently process URLs from a text file, distribute tasks using Redis Streams, and store extracted metadata in MongoDB.

**Success Criteria:**
- Producer reads URLs from a `.txt` file and pushes them to Redis Streams.
- Worker containers consume URLs from Redis Streams and extract metadata.
- Extracted metadata is saved in MongoDB with minimal latency.

**Benchmark:**
- Each worker should process at least 50 URLs per minute.
- System should scale horizontally with additional worker containers.

**Potential Blockers:**
- CAPTCHA and JavaScript-heavy pages may slow down Selenium.
- Network latency when connecting to Redis or MongoDB.
- Memory usage in Redis when handling billions of URLs.

**Mitigation:**
- Use headless Selenium for better performance.
- Optimize Redis Streams with appropriate retention policies.
- Scale Redis Cluster and MongoDB replicas as the workload increases.

---

## 3. Release Plan

### **Milestones and Timeline**
1. **Week 1-2: Core Functionality | Scaling and Optimization**  
   - Implement producer and worker services using Redis Streams and MongoDB.
   - Test locally using Docker Compose.
   - Optimize Redis Streams for high throughput.
   - Configure MongoDB indexes and optimize inserts.
   - Scale horizontally by adding worker containers.  

2. **Week 3: Testing and Monitoring**  
   - Load test with 1 million URLs.
   - Monitor worker performance and Redis latency.
   - Set up error logging and system monitoring.

3. **Week 4: Deployment and Final Delivery**  
   - Deploy on AWS or Azure using managed Redis and MongoDB.
   - Document deployment instructions and provide final deliverables.

### **Team Responsibilities**
- **Backend Engineer:** Develop producer and worker scripts.
- **DevOps Engineer:** Configure Docker, Redis, and MongoDB.
- **QA Engineer:** Load test the system and ensure data integrity.

---

## 4. Production Deployment

### **Infrastructure Guidelines:**
- **Redis Cluster:** Use at least 3 nodes with horizontal scaling.
- **MongoDB Replica Set:** Ensure high availability with 3 nodes.
- **Docker Containers:** Deploy using Docker Swarm or Kubernetes for orchestration.

### **Monitoring & Maintenance:**
- Monitor Redis latency, stream size, and consumer lag.
- Track MongoDB write latency and disk usage.
- Use tools like Datadog for centralized logging and alerts.

---

## 5. Appendix

### **AI Tools Used:**
- AI assistance was used for code optimization and debugging.

### **Deployment Instructions:**
1. Install Docker and Docker Compose.
2. Build and start all services using:
   ```bash
   docker-compose up --build -d
   ```
3. Monitor logs using:
   ```bash
   docker-compose logs -f
   ```
4. Connect to MongoDB using MongoDB Compass or any client.

### **Final Checklist:**
✅ Redis Streams and MongoDB are accessible inside containers.  
✅ Producer reads URLs from mounted `.txt` file.  
✅ Worker extracts metadata and saves it in MongoDB.  
✅ System scales by adding more worker containers.  

---

This concludes the proof of concept and deployment plan. The system is now ready for production-scale crawling and metadata extraction.

