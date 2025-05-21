# YouTube Bias Miner

This repository contains the code to the Master's thesis project **Analyzing YouTube Recommendations with the Bias Miner** - _Does an Algorithm Shape the American Mind?_

### Abstract

YouTube as the second most visited website in the world is used as a platform by nearly every American news outlet. YouTube's recommendation algorithm is suspected to influence the opinions of users by leading them down a rabbit hole of increasingly radical video suggestions. This thesis aims to investigate the state of the algorithm in _2025_ by collecting the video recommendations of _89_ YouTube news channels from the US throughout their videos from a _100_ day time span. The recommendations are then analyzed with quantitative methods to investigate whether the algorithm favors any group of channels in its current state. In addition, the recommendations are tested for potentially harmful content. This includes channels that extremist and white supremacist channels as well as channels that can function as a gateway to more extreme forms of content.  In its current state, the algorithm seems to feature more recommendations for left channels which are _24.2%_ of recommendations. Fox News and more right channels are primarily recommended to users who already watch conservative or right-wing videos. Potentially harmful content is rarely recommended by the algorithm with _>1%_ of recommendations falling into that category.

Channels were divided into five classes: left, lean-left, center, lean-right, and right. The following figure shows how recommendations are flowing between the bias classes. The width of the arrows represents the number of recommendations between the classes.
![Sankey Charts](/docs/sankey-charts.jpg)
The _89_ channels were plotted out with a force-layouted graph with the fruchtermann-reingold algorithm.
![Force Layout Graph](/docs/force-graph.jpg)

# Setting Up a Virtual Environment and Installing Dependencies

Follow these steps to set up a Python virtual environment and install dependencies from a `requirements.txt` file:

## 1. Create a Virtual Environment

Run the following command to create a virtual environment in your project directory:

```bash
python -m venv venv
```

This will create a folder named `venv` containing the virtual environment.

## 2. Activate the Virtual Environment

- On **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

## 3. Install Dependencies

Once the virtual environment is activated, install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 4. Verify Installation

You can verify the installed packages using:

```bash
pip list
```

## 5. Create .env file

In the root directory create an `.env` file with the following content. A Youtube API key is required to run the application. You can obtain one from the [Google Developers Console](https://console.developers.google.com/).

```
YOUTUBE_API_KEY=YOUTUBE_API_KEY_GOES_HERE
```
