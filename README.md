# arxiv-digest

## Introduction

arxiv-digest is a specialized tool designed for AI enthusiasts and researchers. It offers an **automated way** to stay updated with the latest AI research papers from arXiv.

By leveraging the power of Google's advanced language model, **Genimi Pro**, arxiv-digest curates and summarizes the most relevant papers based on **your specific areas of interest**.

## Features

+ **Daily Updates**: Retrieves the latest AI papers from arXiv daily.
+ **Customizable Interests**: Tailor your feed based on your selected AI domains.
+ **Advanced Summarization**: Utilizes Google Genimi Pro and OpenAI's models for concise and insightful summaries.
+ **Automated Workflow**: Fully automated process using GitHub Actions.
+ **Email Notifications**: Receive daily digests directly to your inbox.

## Getting Started

### Prerequisites

+ Basic understanding of **GitHub Actions**.
+ Access to Google Genimi Pro API or OpenAI API. You can access the Genimi API for free at [Build with the Gemini API](https://ai.google.dev/). For OpenAI, visit [OpenAI API Platform](https://platform.openai.com/]).
+ **Gmail** account with an [app password](https://support.google.com/accounts/answer/185833?hl=en) from Google for secure email notifications.

### Setup

1. **Fork this Repository**: Start by forking arxiv-digest to your GitHub account.

2. **Configure Action Repository Secrets**:
   Go to your forked repository on GitHub and navigate to `Settings` > `Secrets and variables` > `Actions` > `Secrets`.
   Based on your choice of API, add the appropriate repository secrets from the following options:

   - **If using Google Genimi Pro**:
        + `GOOGLE_API_KEY`: Your Google API key for accessing Genimi Pro.

   - **If using OpenAI**:
        + `OPENAI_API_KEY`: Your OpenAI API key.
        + `OPENAI_API_BASE`: The base URL for the OpenAI API (Optional).
        + `LLM_MODEL`: The specific OpenAI language model you wish to use for summarization.

   - Additionally, add these secrets applicable for both configurations:
        + `GMAIL_ADDRESS`: Your Gmail address used for sending emails.
        + `GMAIL_PASSWORD`: The app password for your Gmail account. (Refer to Google's guide on creating an app password.)
        + `TO_EMAIL_ADDRESS`: The email address where you wish to receive the daily digests.
3. **Configure Action Repository Variables**:
Similar to step 2, go to your forked repository on GitHub and navigate to Settings > Secrets and variables > Actions > **Variables**.
Add the following repository variables:
    + INTERESTS: Define your areas of interest in AI. This variable will be used to filter and select relevant papers from arXiv.
4. **Activate GitHub Actions**:
Ensure that GitHub Actions are enabled in your repository settings to allow for automated daily runs of the script.

### Usage

Once set up, the system will automatically:

1. Scrape the latest AI papers from arXiv.
2. Generate summaries using Genimi Pro or OpenAI's models based on your configuration..
3. Send a digest email every morning with the latest information.


## Acknowledgments

+ arXiv for use of its open access interoperability.
+ Google Genimi Pro and OpenAI for their advanced language model services.