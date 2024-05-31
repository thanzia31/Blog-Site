

# Blog Page with Machine Learning Integration

![Blog Page Screenshot](Blog-Page/media/images/logo_blogpage_psEudMk.png "Blog Page Screenshot")

## Overview
This project is a feature-rich blog page designed to enhance content verification using machine learning models. The platform integrates separate models for text and image content verification, ensuring the quality and relevance of the posts before they are published. The blog also incorporates robust security measures and various user functionalities to provide an engaging and secure experience.
The platform is mainly used to connect people and share their experiences to help other people.The machine learning model is incorperated to make the website user friendly.

## Machine Learning Models

### Text Verification Model
- **Description:** Verifies the quality, relevance, and adherence of the text content to specified guidelines.
- **Framework:** TensorFlow
- **Functionality:** When a user posts content, the model checks the text for correctness before allowing the post to be published. If the content does not meet the criteria, a message is displayed, prompting the user to revise the content.

### Image Verification Model
- **Description:** Analyzes images to ensure they meet the specified criteria for quality and relevance.
- **Framework:** TensorFlow
- **Functionality:** When a user uploads images, the model verifies the image content before allowing the post to be published. If the images do not meet the criteria, a message is displayed, prompting the user to upload a different image.

## Security Features
- **OTP Verification:** Enhances security by requiring users to verify their email address via a One-Time Password (OTP) during registration. This ensures that the email provided is valid and owned by the user.
- **Email Validation:** Ensures that each user registers with a valid, unique email address. Only one account per email is allowed, preventing duplicate registrations and ensuring accountability.

## Features

### User Registration and Authentication
- **Author Registration:** Users must register themselves as authors before writing their first post. This process includes filling out a registration form and verifying their email address.
- **Email Verification:** Registration is completed only if the email ID is verified. This step helps in preventing spam and ensures that all users are genuine.

### Post Management
- **Create Posts:** Registered authors can write and post content. The text verification model checks the content before it is published.
- **Update Posts:** Authors can update their existing posts to make corrections or improvements. This feature helps in keeping the content accurate and up-to-date.
- **Delete Posts:** Authors can delete their posts if they are no longer relevant or if they wish to remove them for any reason.
- **Like Posts:** Users can like posts to show appreciation and support. This feature helps in promoting popular content and engaging users.
- **View Posts by Category:** Posts are categorized, and users can view posts by categories. This feature makes it easier to find content on specific topics.
- **Search Posts:** Users can search for posts by title, making it easier to find specific content quickly.
- **Read Posts:** Users can read posts without creating an account. However, registration is required to write or like posts. This feature makes the content accessible to a wider audience while encouraging user engagement.

### Profile Management
- **View Profile:** Users can view other authors' profiles, including the number of posts and likes received. This feature helps in understanding the contributions and popularity of different authors.
- **Update Profile:** Users can see and update their profile details, such as their bio, profile picture, and contact information. This feature helps in keeping the user profiles accurate and up-to-date.
- **Liked Posts:** Users can view the posts they have liked. This feature provides a personalized experience and helps users keep track of their favorite content.

### User Interaction
- **Connect with Authors:** Users can connect with authors via email or a provided link. This feature fosters community interaction and allows users to seek further information or collaboration.

## Installation

### Prerequisites
- Python 3.x
- Django
- Required Python libraries (listed in `requirements.txt`)

##### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
2. **Create a virtual environment:**
   ```bash
   python -m venv env
   source  env\Scripts\activate
3. **Install dependencies:**
   ```bash
    pip install -r requirements.txt
4. **Run migrations:**
   ```bash
   python manage.py migrate
5. **Start the development server:**
   ```bash
   python manage.py runserver
6. **Access the blog page:**
    Open your web browser and go to http://127.0.0.1:8000/.





## Contact
- Thanzia
- Email: thanzi2004@gmail.com
