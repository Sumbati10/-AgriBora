</div>

<div align="center">
    <h3>Link : https://agribora-production.up.railway.app// </h3>
</div>

![AgriBora Demo](https://github.com/Sumbati10/-AgriBora/blob/main/demo.png?raw=true)





# 🌾 AgriBora: AI-Powered Smart Farming Assistant


AgriBora is a web-based smart agriculture assistant that empowers farmers with AI-driven tools to make data-informed decisions. It offers features like crop recommendation, fertilizer suggestion, crop disease detection from images, and real-time weather forecasting — all in a simple, intuitive interface.

---
## Overview

AgriBora is an innovative solution that uses advanced technology to help farmers improve productivity and make better decisions. The platform features a Smart Crop Recommendation system powered by machine learning to suggest optimal crops based on soil nutrients, climate, and historical data. It also includes a Plant Disease Identification tool using convolutional neural networks (CNNs) to accurately diagnose plant diseases from uploaded images, enabling timely intervention. Additional features such as real-time Weather Forecasts, tailored Fertilizer Recommendations based on soil quality and crop requirements, and a Smart Farming Guide for crop management further enhance its value. With a user-friendly web app, farmers can easily access these insights and tools to improve farming practices.
## 🔧 Features

- 🌱 **Crop Recommendation** – Suggests the best crop to plant based on soil and climate data.
- 💊 **Fertilizer Recommendation** – Recommends the right fertilizer using soil nutrients and crop type.
- 📷 **Crop Disease Detection** – Uses image recognition to identify crop diseases from uploaded pictures.
- ☁️ **Weather Forecast** – Provides real-time weather updates using OpenWeatherMap API.
- 🔐 **Login/Signup System** – Simulated authentication system (demo mode: `demo / farm123`).
- 🖼️ **Modern UI** – Responsive and friendly interface with background images and custom branding.

---
## Datasets

The **Smart Farming Assistant** project provides three key datasets: the **Crop Recommendation Dataset** (2200 rows) includes soil and environmental factors such as nitrogen, phosphorous, temperature, humidity, and pH to predict the most suitable crops; the **Plant Disease Identification Dataset** contains 70,295 training and 17,572 validation images covering 38 diseases across 14 crops like Apple, Tomato, and Grape, used to train CNN models for disease detection; and the **Fertilizer Recommendation Dataset** offers data on soil quality and crop needs to provide tailored fertilizer suggestions. These datasets can be accessed via the following links: [Crop Recommendation Dataset](https://github.com/ravikant-diwakar/AgriSens/blob/master/Datasets/Crop_recommendation.csv), [Plant Disease Dataset](https://github.com/ravikant-diwakar/AgriSens/tree/master/Datasets), and [Fertilizer Recommendation Dataset](https://github.com/ravikant-diwakar/AgriSens/blob/master/Datasets/Fertilizer_recommendation.csv).

# 📌 Crop Recommendation Model

The **Crop Recommendation Model** utilizes machine learning algorithms to suggest the most suitable crops for farmers based on environmental and soil factors. By analyzing data such as soil nutrients, temperature, humidity, pH, and rainfall, the model provides tailored crop recommendations to ensure optimal growth and productivity. The model uses seven classification algorithms, with **Random Forest** achieving the highest accuracy of 99.55%. This helps farmers make informed decisions on crop selection, ensuring better yields and efficient farming practices.

## Dataset

This dataset consists of **2200 rows** in total.
**Each row has 8 columns representing Nitrogen, Phosphorous, Potassium, Temperature, Humidity, PH, Rainfall and Label**
NPK(Nitrogen, Phosphorous and Potassium) values represent the NPK values in the soil. Temperature, humidity and rainfall are the average values of the sorroundings environment respectively. PH is the PH value present in the soil. **The Label column tells us the type of crop that's best suited to grow based on these conditions.
Label is the value we will be predicting**

