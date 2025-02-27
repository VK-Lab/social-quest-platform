# Social Quest Platform

A blockchain-enabled social quest platform built with Flask that lets users complete social media tasks and earn XP rewards. The platform features wallet-based authentication and real-time leaderboards.

## Features

- **Wallet Authentication**: Secure authentication using Ethereum wallet addresses
- **Quest System**: Complete social media tasks to earn XP
- **Real-time Leaderboard**: Track your ranking among other users
- **PostgreSQL Database**: Robust data persistence for user progress and quest data
- **API Documentation**: Interactive Swagger UI for API exploration

## Tech Stack

- **Backend**: Flask with Flask-RESTful
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT-based with wallet address verification
- **API Documentation**: Swagger UI
- **Rate Limiting**: Flask-Limiter for API protection

## API Endpoints

### Authentication
- `POST /api/auth/wallet`: Authenticate with wallet address

### Quests
- `GET /api/quests`: List all available quests
- `POST /api/quests`: Create a new quest
- `POST /api/quests/<quest_id>/complete`: Complete a quest

### User Progress
- `GET /api/user/progress`: Get user's quest completion status
- `GET /api/leaderboard`: View global XP rankings

## API Documentation

Visit `/api/docs` for interactive API documentation using Swagger UI.

## Database Schema

### Users Table
- `id`: Primary key
- `wallet_address`: Ethereum wallet address (unique)
- `xp_total`: Total XP earned
- `created_at`: Account creation timestamp

### Quests Table
- `id`: Primary key
- `title`: Quest title
- `description`: Quest description
- `url`: Social media URL for the quest
- `xp_reward`: XP awarded upon completion
- `required_level`: Minimum level required (default: 0)
- `created_at`: Quest creation timestamp
- `is_active`: Quest availability status

### Quest Progress Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `quest_id`: Foreign key to quests
- `status`: Quest status (in_progress/completed)
- `completed_at`: Completion timestamp
- `created_at`: Progress tracking start timestamp

## Rate Limiting

To ensure fair usage, the API implements the following rate limits:
- Authentication: 5 requests per minute
- Quest listing: 30 requests per minute
- Quest completion: 10 requests per minute
- Leaderboard: 30 requests per minute