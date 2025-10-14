# 🎮 GameBot – Advanced AI-Powered Telegram Bot

A **multi-functional AI Telegram bot** that combines **game recommendations**, **AI chat**, **Dota 2 statistics**, and **music sharing** — all powered by **machine learning** and **Ollama local LLM integration**.

---

## 🚀 Features

- 🤖 **AI Chat Integration** – Local **Ollama LLM (llama3.2)** for natural conversation
- 🎯 **Advanced Game Recommendations** – ML-powered algorithms with hybrid filtering
- 📊 **Data-Driven Insights** – Trained on Steam and user-based game datasets
- 🧠 **Dota 2 Analytics** – Player stats, match history, and visual charts
- 🎵 **Music Sharing** – Send tracks with lyrics and album art
- 💬 **Interactive Interface** – Command or conversational mode
- 💾 **Persistent Models** – Pre-trained models stored in `Pkl/` for fast responses

---

## ⚙️ Prerequisites

- **Python 3.7+**
- **Ollama** installed with `llama3.2` model
- **Telegram Bot Token** from [@BotFather](https://t.me/BotFather)
- Required datasets in `Dataset/` folder
- API keys configured in `.env`

---

## 📂 Dataset Requirements

The system requires the following CSV datasets under the `Dataset/` directory:

| File                  | Description                   |
| --------------------- | ----------------------------- |
| `recommendations.csv` | User recommendation data      |
| `games.csv`           | Game metadata and features    |
| `users.csv`           | User profiles and preferences |
| `steam_games.csv`     | Steam platform game data      |

---

## 🧠 Ollama Setup

```bash
# 1. Install Ollama (see https://ollama.ai)
# 2. Pull the required model
ollama pull llama3.2

# 3. Start the Ollama service
ollama serve
```

---

## 🧩 Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd chatbot

# 2. Create directories
mkdir Dataset Pkl music

# 3. Install dependencies
pip install -r requirements.txt
```

### 🔧 Setup Datasets & Train Models

#### 📂 Setup Instructions

1. [Download](https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam) the dataset.
2. Extract the CSV files from the downloaded archive.
3. Place the extracted files inside the `Dataset/` directory of the project:

# Place datasets in Dataset/

```bash
python Scripts/recommendation_system.py
```

### 🌍 Configure Environment Variables

Create a `.env` file in your project root:

```env
TELEGRAM_API=your_telegram_bot_token_here
RAWG_APIKEY=your_rawg_api_key_here
```

---

## 🌱 Environment Variables

| Variable       | Description                       | Required    |
| -------------- | --------------------------------- | ----------- |
| `TELEGRAM_API` | Telegram Bot Token                | ✅          |
| `RAWG_APIKEY`  | RAWG Video Games Database API Key | ⚙️ Optional |

---

## 🏗️ Project Structure

```
chatbot/
├── telegram_bot.py              # Main bot file
├── Scripts/
│   ├── langchain_bot.py         # AI chat & game recs (Ollama + LangChain)
│   ├── recommender.py           # Model loader & rec functions
│   ├── recommendation_system.py # ML recommendation engine
│   ├── DotaProTracker.py        # Dota 2 stats & visuals
│   └── music.py                 # Music & lyrics handler
├── Dataset/                     # Training data
├── Pkl/                         # Trained pickle models
├── music/                       # Audio & album art
├── .env                         # Environment variables
├── requirements.txt             # Dependencies
└── README.md                    # Documentation
```

---

## 🧩 Module Overview

### 🧮 `Scripts/recommendation_system.py`

Core ML engine for collaborative, content-based, and hybrid recommendations.

**Highlights:**

- **Collaborative Filtering:** TruncatedSVD + Cosine Similarity
- **Content-Based Filtering:** CountVectorizer + Scaled numeric/categorical features
- **Hybrid Recommendations:** Combines both models intelligently
- **Model Persistence:** Exports `.pkl` files to `Pkl/`

---

### 🗣️ `Scripts/langchain_bot.py`

AI conversational module using **LangChain + Ollama**.

- Context-aware chat responses
- Detects user intent for game recommendations
- Integrates hybrid recommendation methods

---

### 🎮 `Scripts/recommender.py`

Model interface layer for loading and serving recommendations.

**Functions:**

- `collaborative(query)`
- `content_based(query)`
- `hybrid(query)`

---

### 🧙‍♂️ `Scripts/DotaProTracker.py`

Fetches and visualizes **Dota 2 player stats** via Steam API.

**Features:**

- Player profile lookup
- Match history and analytics
- Performance visualization charts

---

### 🎶 `Scripts/music.py`

Handles music file sharing and lyrics management.

- Provides preloaded songs and album art
- Supports lyric sharing in Telegram chat

---

## 💡 Usage

```bash
# Start Ollama
ollama serve

# Train models (first run only)
python Scripts/recommendation_system.py

# Start the Telegram bot
python telegram_bot.py
```

### 🧾 Commands

| Command       | Description                    |
| ------------- | ------------------------------ |
| `/start`      | Welcome message                |
| `/Dota2_stat` | Get Dota 2 stats with visuals  |
| `/music`      | Share track with lyrics        |
| _any text_    | AI chat or game recommendation |

---

## 🎯 Recommendation Examples

### Collaborative Filtering

```python
recommend_based_on_collaborative("Just Cause™ 3", pt, collab_sim_matrix)
# → ['Just Cause 2', 'Saints Row IV', 'Grand Theft Auto V']
```

### Content-Based Filtering

```python
recommend_based_on_content("BRINK: Agents of Change", title_df, content_sim_df)
# → ['Borderlands 2', 'Team Fortress 2', 'Left 4 Dead 2']
```

### Hybrid Approach

```python
recommend_hybrid("Just Cause™ 3", pt, collab_sim_matrix, title_df, content_sim_df)
# → Combines best of both worlds
```

---

## 🔌 API Integrations

- **Ollama** – Local AI model serving (no external API costs)
- **RAWG API** – Video game metadata

---

## 🧰 Dependencies

```txt
pyTelegramBotAPI>=4.0.0
python-dotenv>=0.19.0
requests>=2.25.0
langchain>=0.1.0
langchain-ollama>=0.1.0
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
scipy>=1.7.0
langdetect>=1.0.9
matplotlib>=3.5.0
pillow>=8.0.0
pickle5>=0.0.11
```

---

## ⚡ Model Performance Summary

| Model             | Highlights                                                                    |
| ----------------- | ----------------------------------------------------------------------------- |
| **Collaborative** | 50 SVD components, cosine similarity, sparse matrix optimization              |
| **Content-Based** | 5000+ feature vectors, multilingual filtering, numeric + categorical features |
| **Hybrid**        | Balances popularity, personalization, and cold-start games                    |

---

## 🛠️ Troubleshooting

| Issue                 | Solution                                      |
| --------------------- | --------------------------------------------- |
| Models missing        | Run `python Scripts/recommendation_system.py` |
| Memory errors         | Reduce dataset or increase RAM                |
| Long training time    | Use sampled data                              |
| Poor recommendations  | Recheck data quality & features               |
| Ollama not connecting | Ensure `ollama serve` is running              |

---

## 🧪 Development

### 🔁 Retrain Models

```bash
# Update datasets then retrain
python Scripts/recommendation_system.py
```

### 🧠 Customize Algorithms

- Adjust SVD components or similarity thresholds
- Add new metadata features
- Modify hybrid weighting

### ⚙️ Performance Optimization

- Model caching
- Sparse matrices
- Feature selection
- Batch inference

---

## 🤝 Contributing

1. Fork this repository
2. Create a new feature branch
3. Implement and test your feature
4. Update documentation
5. Submit a Pull Request

---

## 📜 License

This project was developed **for educational purposes**.

---

## 📬 Contact

For any issues or questions regarding this project, please reach out or create an issue on GitHub.

**Project Maintainer:** Mehdi Gholami  
**GitHub:** [@Mr-Gholam](https://github.com/Mr-Gholam)
