# Thesis Bike Lanes CNN

This repository contains the code and data for the thesis titled "Automated Detection of Pavement Damage in Urban Bike Lanes Using Deep Learning: A Case Study of Metropolitan Lima".

In this project, we train YOLO models using data from the RDD2022 dataset, which contains images of roads from various countries.

Additionally, we introduce a new dataset with images from bike lanes in Metropolitan Lima to test the models.

To install the required libraries for running the project, use the following command with a virtual environment:

```bash
pip install -r requirements/model.txt
```

We also provide a model.yml file for running the project using Docker Compose. However, please note that using this approach may prevent the GPU from being fully utilized, and you may not achieve 100% GPU performance.

```bash
docker-compose -f model.yml up --build
```
