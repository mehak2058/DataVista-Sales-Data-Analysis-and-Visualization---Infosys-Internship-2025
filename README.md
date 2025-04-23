# Social Media Trends Analysis Web App

A Flask-based web application for analyzing and predicting social media trends and engagement levels.

## Features

- Interactive dashboard with real-time statistics
- Data visualization and analytics
- Engagement prediction
- Platform comparison tools
- Content recommendation system
- Data export functionality

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd social-media-trends
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
SECRET_KEY=your-secret-key
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
social-media-trends/
├── app/
│   ├── static/
│   ├── templates/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── data/
│   └── Viral_Social_Media_Trends.csv
├── requirements.txt
├── app.py
└── README.md
```

## Features in Detail

### Dashboard
- Real-time statistics and metrics
- Platform-wise performance comparison
- Engagement level distribution
- Trending hashtags visualization

### Analytics
- Interactive charts and graphs
- Customizable filters
- Time-based trend analysis
- Platform comparison tools

### Prediction
- Engagement level prediction
- Content optimization recommendations
- Best posting time suggestions
- Hashtag effectiveness analysis

### Export
- Export data in multiple formats (CSV, Excel)
- Custom report generation
- Filtered data export

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

