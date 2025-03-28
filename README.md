## **Online Course Sharing API**
  This project is a backend API built using Flask and MongoDB Atlas for managing and sharing academic resources between students and professors. It enables secure    file uploads and downloads using JWT authentication and GridFS for file storage in the cloud.

## **Overview**
  The API allows professors to upload course materials (PDF, DOC, PPT) and students to share handwritten notes (PDF, images). It supports role-based access, public   file listing, and secure storage using MongoDB's GridFS. Files are not saved locally and are accessible via secure download links.

## **Features**
  -	Secure registration and login using JWT
  -	Role-based access control (student, professor)
  -	Professors can upload, view, and delete teaching materials
  -	Students can upload, view, and delete class notes
  -	Public file access and download
  -	Files stored in MongoDB Atlas using GridFS
  -	Organized structure with separate route handlers

## **Technology Stack**
  -	Backend Framework: Flask
  -	Database: MongoDB Atlas (Cloud)
  -	Authentication: JWT (via flask-jwt-extended)
  -	File Storage: GridFS (part of PyMongo)
  -	Environment Management: Python-dotenv
  -	Testing Tools: Postman

## **Installation**
  1. Clone the Repository

    git clone https://github.com/janyajaiswal/MidProject.git
    
    cd MidProject


  2. Create and Activate a Virtual Environment (Recommended)


  **For macOS/Linux:**
  
    python -m venv venv
    source venv/bin/activate


  **For Windows:**
  
    python -m venv venv
    venv\Scripts\activate
  
  3. Install Dependencies

    pip install -r requirements.txt

## **Environment Variables**

  Create a .env file in the root directory with the following keys:
  
 <prev> <code> MONGO_URI=mongodb+srv://<username>:<password>@mscs.ywi7l.mongodb.net/?retryWrites=true&w=majority&appName=MSCS
  JWT_SECRET_KEY=your_secret_key </prev> </code>
  
  Replace <username> and <password> with your MongoDB Atlas credentials.

## **API Endpoints**

**Authentication**

  | Method | Endpoint        | Description         |
  |--------|------------------|---------------------|
  | POST   | /auth/register   | Register new user   |
  | POST   | /auth/login      | Login and get JWT   |

  
  Requires body with username, password, and role (student or professor)

**Student Routes**

  | Method | Endpoint                     | Description             |
  |--------|------------------------------|-------------------------|
  | POST   | /student/upload              | Upload handwritten notes |
  | GET    | /student/my-notes            | View uploaded notes      |
  | DELETE | /student/delete/<file_id>    | Delete a specific note   |

  
  Requires valid JWT token with student role

**Professor Routes**

  | Method | Endpoint                          | Description               |
  |--------|-----------------------------------|---------------------------|
  | POST   | /professor/upload                 | Upload course materials   |
  | GET    | /professor/my-materials           | View uploaded materials   |
  | DELETE | /professor/delete/<file_id>       | Delete a specific material |

  Requires valid JWT token with professor role

**Public Routes**

  | Method | Endpoint                      | Description           |
  |--------|-------------------------------|-----------------------|
  | GET    | /public/files                 | List all public files |
  | GET    | /public/file/<file_id>        | Download file by ID   |

  
  Accessible without authentication

## **File Storage with GridFS**
  All uploaded files are stored in MongoDB Atlas using GridFS, which:
  -	Splits large files into smaller chunks
  -	Stores metadata and chunks in fs.files and fs.chunks
  -	Handles files larger than 16MB efficiently
  -	Supports fast and secure retrieval

## **Error Handling**
  Custom error handlers are defined for:
  -	Invalid JWT
  -	Unauthorized access
  -	File not found
  -	Invalid request body
  These are managed centrally in the error_handlers.py file for consistent response formatting.

## **Authors**
  -	Janya Jaiswal
  **CWID:** 878062934
  -	Indrayani Bhosale
  **CWID:** 842614851





