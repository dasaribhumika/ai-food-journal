# 🚀 Deployment Guide

This guide will help you deploy your AI Food Journal application to various hosting platforms.

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- API keys for OpenAI and GROQ (optional but recommended for full functionality)

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended)

**Streamlit Cloud** is the easiest way to deploy Streamlit applications.

#### Steps:
1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/ai-food-journal.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `yourusername/ai-food-journal`
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Configure Environment Variables:**
   - In your Streamlit Cloud app settings
   - Add secrets:
   ```toml
   OPENAI_API_KEY = "your-openai-api-key"
   GROQ_API_KEY = "your-groq-api-key"
   ```

### Option 2: Heroku

#### Steps:
1. **Create Heroku App:**
   ```bash
   heroku create your-app-name
   ```

2. **Add Buildpacks:**
   ```bash
   heroku buildpacks:add heroku/python
   ```

3. **Create Procfile:**
   ```bash
   echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   ```

4. **Set Environment Variables:**
   ```bash
   heroku config:set OPENAI_API_KEY="your-openai-api-key"
   heroku config:set GROQ_API_KEY="your-groq-api-key"
   ```

5. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Option 3: Railway

#### Steps:
1. **Connect Repository:**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Select the repository

2. **Configure:**
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

3. **Add Environment Variables:**
   - Add `OPENAI_API_KEY` and `GROQ_API_KEY` in Railway dashboard

### Option 4: Local Network Sharing

#### Steps:
1. **Run with Network Access:**
   ```bash
   streamlit run app.py --server.address=0.0.0.0 --server.port=8501
   ```

2. **Access from Other Devices:**
   - Find your local IP: `ifconfig` (Mac/Linux) or `ipconfig` (Windows)
   - Access via: `http://YOUR_IP:8501`

## 🔧 Configuration

### Environment Variables

Create a `.env` file or set environment variables:

```bash
OPENAI_API_KEY=your-openai-api-key-here
GROQ_API_KEY=your-groq-api-key-here
```

### API Keys Setup

1. **OpenAI API Key:**
   - Visit [platform.openai.com](https://platform.openai.com)
   - Create account and get API key
   - Used for food journal insights

2. **GROQ API Key:**
   - Visit [console.groq.com](https://console.groq.com)
   - Create account and get API key
   - Used for task management, goals, meal planning, and self-care insights

## 📁 File Structure for Deployment

```
ai-food-journal/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── DEPLOYMENT.md         # This file
├── utils/                # Utility functions
│   ├── data_utils.py
│   ├── insight_utils.py
│   ├── oura_utils.py
│   ├── task_utils.py
│   ├── goal_utils.py
│   ├── meal_utils.py
│   └── selfcare_utils.py
└── *.json               # Data files (will be created automatically)
```

## 🔒 Security Considerations

1. **API Keys:**
   - Never commit API keys to version control
   - Use environment variables or secrets management
   - Rotate keys regularly

2. **Data Privacy:**
   - All data is stored locally in JSON files
   - Consider encryption for sensitive data
   - Regular backups recommended

3. **Access Control:**
   - Application has no built-in authentication
   - Consider adding authentication for production use

## 🚀 Performance Optimization

1. **Caching:**
   - Streamlit automatically caches expensive operations
   - Use `@st.cache_data` for data loading
   - Use `@st.cache_resource` for model loading

2. **Data Management:**
   - Regular cleanup of old data
   - Archive old entries periodically
   - Monitor file sizes

## 📊 Monitoring

1. **Application Logs:**
   - Monitor Streamlit logs for errors
   - Check API usage and costs
   - Track user engagement

2. **Data Backup:**
   - Regular backups of JSON files
   - Version control for configuration
   - Export functionality for data portability

## 🆘 Troubleshooting

### Common Issues:

1. **Import Errors:**
   - Ensure all dependencies are in `requirements.txt`
   - Check Python version compatibility

2. **API Key Issues:**
   - Verify API keys are correctly set
   - Check API quotas and billing

3. **Port Conflicts:**
   - Change port in deployment command
   - Check if port is already in use

4. **Memory Issues:**
   - Monitor memory usage
   - Optimize data loading
   - Consider data archiving

## 📞 Support

For deployment issues:
1. Check Streamlit documentation
2. Review platform-specific guides
3. Check application logs
4. Verify environment setup

## 🎯 Next Steps

After deployment:
1. Test all features thoroughly
2. Set up monitoring and alerts
3. Configure backups
4. Document any custom configurations
5. Share with users and gather feedback

---

**Happy Deploying! 🚀** 