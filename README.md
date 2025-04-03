# Customer Review Sentiment Analyzer

A powerful Streamlit application that leverages OpenAI's GPT-3.5-turbo model to analyze customer reviews and provide sentiment insights. Built with efficiency and scalability in mind, this tool helps businesses understand customer feedback at scale.

## Features

- **Single Review Analysis**: Instantly analyze individual customer reviews
- **Batch Processing**: Upload CSV files for bulk sentiment analysis
- **Sentiment Distribution**: View sentiment breakdowns with detailed metrics
- **Token Usage Tracking**: Smart token consumption monitoring with dynamic AI-generated insights
- **Cost Estimation**: Real-time calculation of API usage costs

## Technical Stack

- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-3.5-turbo
- **Data Processing**: Pandas
- **Token Management**: Tiktoken

## Installation

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Enter your OpenAI API key in the sidebar
3. Choose between:
   - Single review analysis: Enter text directly
   - Batch analysis: Upload a CSV file

## Requirements

See `requirements.txt` for a complete list of dependencies. Key requirements include:
- Python 3.6+
- streamlit==1.44.1
- openai==1.70.0
- pandas==2.2.3
- tiktoken==0.9.0

## Developer

**Mike**  
Emerging AI Architect  
Specializing in Business Transformation  
📧 mike@washere.lol

## Features in Development

- Advanced sentiment analysis metrics
- Custom model integration options
- Export capabilities for analysis results
- Interactive visualization enhancements

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
