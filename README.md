# Betenda API - Backend API for Language Community

Betenda is a self hosted API for people who want to build a private community dedicated to languages, where users can contribute to the growth of their language through word, sayings, sentences, and poems contributions. Additionally, it offers a Twitter-like feature that allows users to post, read articles, comment, react, and much more.

the client next.js webapp is still in it's infancy and will be made public as fast as possible

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [API Documentation](#api-documentation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Betenda API is a backend API built with Django and Django REST Framework (DRF). It provides a robust and scalable platform for creating a private community centered around languages. Users can contribute to linguistic content like words, sayings, sentences, and poems, fostering the growth of their languages. Moreover, the platform offers a Twitter-like social networking experience, allowing users to share posts, read articles, comment, react, and engage in a wide range of interactions.

## Features

- User authentication and authorization.
- Contribution of words, sayings, sentences, and poems for various languages of your choice.
- Post creation, reading, updating, and deletion.
- Article publication(Admins) and reading.
- Real time notifications.
- Commenting and reacting to posts, articles, poems and sayings.
- Reporting user generated content
- Platform and Campaign Donations for projects that are more invested in the well being and improvement of their local community
- Social networking features (following, notifications, etc.).
- And much more to come, contact me if you have any feature ideas or just submit a pull request!

## Getting Started

### Prerequisites

Before running the Betenda API, ensure you have the following installed:
- Python (version 3.8+)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/k4l3b4/betenda.git
cd betenda
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Set up the database:

```bash
python manage.py makemigrations
```
NOTE: some times django might not recognize the apps and might say no change when trying to makemigrations
run 👇🏾:
```bash
python manage.py makemigrations <appname(s)>
```
Commit the migrations to db:
```bash
python manage.py migrate
```

5. Run the development server:

```bash
python manage.py runserver
```

The API should now be accessible at `http://localhost:8000/api/`.

## API Documentation

Working on it

## Usage

Please contribute to the readme to make it complete enough for readers

## Contributing

We welcome contributions from the community. To contribute to Betenda, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Commit your changes and push the branch to your fork.
4. Open a pull request, describing the changes and the problem it solves.

Please ensure that your code follows the project's coding conventions and includes appropriate tests.

## License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute the code as per the terms of this license.

---

Thank you for your interest in Betenda! If you have any questions or need assistance, please feel free to contact me via my telegram account. We look forward to seeing your contributions!
